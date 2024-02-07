import json
from pathlib import Path

data_name = "NLP-2023"
data_dir = Path(__file__).resolve().parents[1] / "data" / data_name
assert data_dir.exists()
task_dir = data_dir / "tasks"
task_dir.mkdir(exist_ok=True)

for paper in sorted(data_dir.glob("paper_img/*")):
    task = {
        "id": paper.name,
        "data": {
            "images": [
                f"/data/local-files/?d=data/{data_name}/paper_img/{paper.name}/{img.name}"
                for img in sorted(paper.iterdir())
            ]
        },
    }
    task_dir.joinpath(paper.name).with_suffix(".json").write_text(
        json.dumps(task, indent=2)
    )
