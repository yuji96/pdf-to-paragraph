import sys
from typing import Iterator

import numpy as np
from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams, LTLayoutContainer, LTTextContainer


def parse_page(container) -> Iterator[LTTextContainer]:
    if isinstance(container, LTTextContainer):
        yield container
    if isinstance(container, LTLayoutContainer):
        for obj in container:
            yield from parse_page(obj)


def extract_textbox(pdf_path, width=None, height=None, y_reverse=True):
    for page in extract_pages(pdf_path, laparams=LAParams(all_texts=True)):
        if width is None:
            width = page.width
        if height is None:
            height = page.height
        x_scale = width / page.width
        y_scale = height / page.height

        texts = []
        bboxes = []
        for textbox in parse_page(page):
            texts.append(textbox.get_text())
            bboxes.append(textbox.bbox)
        bboxes = np.array(bboxes) * [x_scale, y_scale, x_scale, y_scale]
        if y_reverse:
            bboxes[:, [1, 3]] = height - bboxes[:, [3, 1]]
        bboxes = bboxes.astype(int)
        yield (texts, bboxes), width, height


if __name__ == "__main__":
    list(extract_textbox(sys.argv[1]))
