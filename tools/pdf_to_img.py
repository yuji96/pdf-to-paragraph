from pathlib import Path

from pdf2image import convert_from_path

max_files = 5
pdf_dir = Path("data/NLP-2023/pdf_dir")
img_dir = pdf_dir.parent / "paper_img"
assert pdf_dir.exists()
img_dir.mkdir(exist_ok=True)

pdf_pathes = sorted(pdf_dir.glob("*.pdf"))[:max_files]
for pdf_path in pdf_pathes:
    images = convert_from_path(pdf_path, dpi=100)
    for i, image in enumerate(images):
        paper_dir = img_dir / f"{pdf_path.stem}"
        paper_dir.mkdir(exist_ok=True)
        image.save(paper_dir / f"{i}.png")
