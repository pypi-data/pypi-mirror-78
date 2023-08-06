# ocr2pdf

![version](https://img.shields.io/badge/version-0.1.0-blue)

ocr2pdf is a package that allows you to create a searchable pdf from HOCR/JSON/TSV output and PIL Images

## Prerequisites

Before you begin, ensure you have met the following requirements:

### Docker

* You have installed the latest version of Docker and docker-compose
* You have internet access to pull docker images and packages

### Pypi

* Python 3.6+
* Able to install requirements

## Installing ocr2pdf

To install ocr2pdf, follow these steps:

### Docker

```bash
docker-compose -f docker-compose.yaml build
```

### Pypi

```bash
git clone <this repo>
cd <this repo>
pip install .
```

## Using ocr2pdf

To use ocr2pdf, follow these steps:

### Docker

```bash
docker-compose -f docker-compose.yaml up
```

### Python

```python
import json

from PIL import Image
from ocr2pdf import Ocr2Pdf

o2p = Ocr2Pdf(title="demo", dpi=300)
# Load the OCR'ed images
ims = [Image.open("demo.png")]
# Load the json data from OCR
with open("demo.json", "r") as f:
    data = json.load(f)

# Create the layered PDF
layered_pdf = o2p.merge_json(ims, data)

with open("demo.pdf", mode="w") as f:
    layered_pdf.save(f)
```

### Advanced usage

```python
...

layered_pdf = o2p.merge_json(ims, data)
layered_pdf_multi = layered_pdf + layered_pdf

with open("demo.pdf", mode="w") as f:
    layered_pdf_multi.save(f)
```

You can also combine loaded hocr files (list[str]) or tsv (pd.DataFrame) files to make a searchable pdf

```python
layered_pdf = o2p.merge_hocr(ims, data)
layered_pdf = o2p.merge_df(ims, data)
```

## Contributing to ocr2pdf

To contribute to ocr2pdf, follow these steps:

1. Create a branch: `git checkout -b <branch_name>`.
2. Make your changes and commit them: `git commit -m '<commit_message>'`
3. Push to the original branch: `git push origin <project_name>/<location>`
4. Create the pull request.

## Contact

If you want to contact use you can reach us at andy.challis@capgemini.com or jeremiah.mannings@capgemini.com
