from pathlib import Path

from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams, LTLayoutContainer, LTText


def parse_page(container):
    if isinstance(container, LTText):
        yield container
    if isinstance(container, LTLayoutContainer):
        for obj in container:
            yield from parse_page(obj)


parent = Path(__file__).resolve().parent
for page in extract_pages(parent / "A1-1.pdf", laparams=LAParams(all_texts=True)):
    boxes = list(parse_page(page))
    for box in boxes:
        print(box.bbox)
        print(box.get_text().replace("\n", ""))
        print("-" * 30)
        print()
