import json
from pathlib import Path

from extract_bbox import extract_textbox

data_name = "NLP-2023"

data_dir = Path(__file__).resolve().parents[1] / "data" / data_name
assert data_dir.exists()
pdf_dir = data_dir / "pdf_dir"
img_dir = data_dir / "paper_img"
task_dir = data_dir / "tasks"
task_dir.mkdir(exist_ok=True)


for imgs_per_paper in sorted(img_dir.iterdir()):
    paper_id = imgs_per_paper.name
    images = []
    pred_results = []
    for page_id, (img, (textboxes, pdf_w, pdf_h)) in enumerate(
        zip(
            sorted(imgs_per_paper.iterdir()),
            extract_textbox(pdf_dir / f"{paper_id}.pdf"),
        )
    ):
        images.append(
            f"/data/local-files/?d=data/{data_name}/paper_img/{paper_id}/{img.name}"
        )
        for texts, bbox in zip(*textboxes):
            pred_results.append(
                {
                    "type": "rectanglelabels",
                    "from_name": f"labels-{page_id}",
                    "to_name": f"image-{page_id}",
                    "value": {
                        "x": bbox[0] / pdf_w * 100,
                        "y": bbox[1] / pdf_h * 100,
                        "width": (bbox[2] - bbox[0]) / pdf_w * 100,
                        "height": (bbox[3] - bbox[1]) / pdf_h * 100,
                        "rectanglelabels": ["none"],
                        "score": page_id,  # ページ番号として使う
                    },
                    "meta": {"text": [texts]},
                }
            )

    task = {
        "id": paper_id,
        "data": {"images": images},
        "predictions": [{"model_version": "pdf", "result": pred_results}],
    }
    task_dir.joinpath(paper_id).with_suffix(".json").write_text(
        json.dumps(task, indent=2)
    )
