from setuptools import find_packages, setup

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setup(
    name="ocr2pdf",
    version="0.1.0",
    description="Combines OCR output with images to make searchable pdf",
    long_description="# Coming Soon",
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages("src", exclude=["tests", "api", "api.*"]),
    install_requires=["lxml", "pandas", "Pillow", "pypdf2", "reportlab"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
    ],
    keywords=["searchable pdf"],
    zip_safe=True,
    python_requires=">=3.6",
)
