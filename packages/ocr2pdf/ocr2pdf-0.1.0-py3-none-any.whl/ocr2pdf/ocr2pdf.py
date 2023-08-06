import re
import logging
import warnings
from typing import Dict, List

from PIL import Image
from reportlab.pdfgen.canvas import Canvas
from lxml import etree, html
import pandas as pd

from .utils import LayeredPDF, MemoryWrapper, load_invisible_font, Ocr2PdfException, CustomPDFInfo

log = logging.getLogger(__name__)


class Ocr2Pdf(object):
    def __init__(self, title: str = "demo", dpi: int = 300):
        self.title = title
        self._dpi_scale = 72 / dpi
        self._font_size = 8
        self._output = MemoryWrapper()
        load_invisible_font()
        self._make_pdf()

    def _make_pdf(self):

        self._pdf = Canvas(self._output, pageCompression=1)
        self._pdf._doc.info = CustomPDFInfo()
        self._pdf._doc.info.creator = self.__class__.__name__
        self._pdf._doc.info.title = self.title

    def merge_hocr(self, images: List[Image.Image], data: List[str]) -> LayeredPDF:
        """Create a searchable PDF from HOCR loaded output and PIL Images

        Args:
            images (List[PIL.Image]): (List[PIL.Image]): OCR'ed images
            data (List[str]): List of loaded HOCR files as strings

        Returns:
            LayeredPDF: Final PDF output
        """
        p1 = re.compile(r"bbox((\s+\d+){4})")
        p2 = re.compile(r"baseline((\s+[\d\.\-]+){2})")

        # Convert Hocr to JSON
        tmp_data = []
        for i, hocrfile in enumerate(data):
            tmp_page = {"page": i + 1, "output": []}
            hocr = etree.fromstring(hocrfile, html.XHTMLParser())
            for line in hocr.xpath('//*[@class="ocr_line"]'):
                xpath_elements = './/*[@class="ocrx_word"]'
                for word in line.xpath(xpath_elements):
                    # In HOCR bbox is defined as upper-left corner (x0, y0) and the lower-right corner (x1, y1)
                    box = p1.search(word.attrib["title"]).group(1).split()
                    box = [float(i) for i in box]
                    tmp_page["output"].append(
                        {
                            "bounding_box": [box[0], box[1], box[2] - box[0], box[3] - box[1]],  # Convert to x, y, w, h
                            "text": word.text_content(),
                        }
                    )
            tmp_data.append(tmp_page)
        return self.merge_json(images, tmp_data)

    def merge_df(self, images: List[Image.Image], data: pd.DataFrame) -> LayeredPDF:
        """Create a searchable PDF from OCR tsv output and PIL Images

        Args:
            images (List[PIL.Image]): OCR'ed images
            data (pd.DataFrame): OCR tsv output loaded as pd.DataFrame

        Returns:
            LayeredPDF: Final PDF output
        """
        # Convert df to JSON
        tmp_data = []
        for page in sorted(data["page_num"].unique()):
            tmp_page = {"page": page, "output": []}
            subset = data[data["page_num"] == page]
            for i, record in subset.iterrows():
                tmp_page["output"].append(
                    {
                        "bounding_box": [
                            record["left"],
                            record["top"],
                            record["width"],
                            record["height"],
                        ],  # Convert to x, y, w, h
                        "text": record["text"],
                    }
                )
            tmp_data.append(tmp_page)
        return self.merge_json(images, tmp_data)

    def merge_json(self, images: List[Image.Image], data: List[Dict]) -> LayeredPDF:
        """Create a searchable PDF from OCR JSON output and PIL Images

        Args:
            images (List[PIL.Image]): OCR'ed images
            data (List[Dict]): OCR JSON output

        Returns:
            LayeredPDF: Final PDF output
        """
        if min(len(images), len(data)) == 0:
            raise Ocr2PdfException("Length of data or images is 0")
        if len(images) != len(data):
            warnings.warn(f"Length of array mismatch, will use only length {max(len(data), len(images))}")
        for i, (image, dat) in enumerate(zip(images, data)):
            log.info(f"Processing image and data - page {i+1}")
            width, height = image.size
            self._pdf.setPageSize((width * self._dpi_scale, height * self._dpi_scale))
            self._pdf.drawInlineImage(image, 0, 0, width=width * self._dpi_scale, height=height * self._dpi_scale)
            self._add_text_layer(image, dat["output"])
            log.info(f"Completed page {i+1}")
            self._pdf.showPage()
        self._pdf.save()
        self._make_pdf()
        return LayeredPDF(self._output)

    def _add_text_layer(self, image: Image.Image, data: Dict):
        """Draw an invisible text layer onto PDF page from OCR data

        Args:
            image (PIL.Image): OCR'ed image
            data (Dict): Final PDF output for this image
        """
        width, height = image.size
        for word in data:
            rawtext = str(word["text"].strip() + " ")
            if rawtext.strip() == "":
                log.info("Skipping null word")
                continue
            font_width = self._pdf.stringWidth(rawtext, "invisible", self._font_size)
            if font_width <= 0:
                log.info("Skipping word of no visible length")
                continue
            box = word["bounding_box"]
            text = self._pdf.beginText()
            text.setTextRenderMode(3)  # double invisible
            text.setFont("invisible", self._font_size)
            # [SE243] - These boxes were occasionally represented as string or floats
            #           so applying integer conversion, however may change if we
            #           change coordinates to percentages rather than pixels.
            box_width, box_x, box_y = (
                int(box[2]) * self._dpi_scale,
                int(box[0]) * self._dpi_scale,
                (height - int(box[1]) - (int(box[3]) * 0.75)) * self._dpi_scale,
            )
            log.info(
                f"Adding text to region: rawtext={rawtext}, box_x={box_x:.2f}, box_y={box_y:.2f}, box_width={box_width:.2f}, box_font={self._font_size}"
            )
            text.setTextOrigin(box_x, box_y)
            text.setHorizScale(100.0 * box_width / font_width)
            text.textLine(rawtext)
            self._pdf.drawText(text)
