# python-pdfextract


A python wrapper for [pdf-extract](https://github.com/bitextor/pdf-extract), a Java library for HTML extraction from PDF documents.

## Configuration


Dependencies:

 * jpype
 * chardet

The pdf-extract jar files will get fetched and included automatically when building the package.

## Installation

Checkout the code:

	git clone https://github.com/bitextor/python-pdfextract.git
	cd python-pdfextract


**virtualenv**

	virtualenv env
	source env/bin/activate
    pip install -r requirements.txt
	python setup.py install
	

**Fedora**

    sudo dnf install -y python2-jpype
    sudo python setup.py install

Also you can now directly install without explicitly running `setup.py` or checkout the code:

**pip**

    pip install python-pdfextract # Stable releases
    pip install git+https://github.com/bitextor/python-pdfextract.git # master code
    pip install git+https://github.com/bitextor/python-pdfextract.git@branchname # development "branchname" code


## Usage


Be sure to have set `JAVA_HOME` properly since `jpype` depends on this setting.

    from pdfextract.extract import Extractor
    extractor = Extractor(pdf=your_pdf_data)


An advanced way to create the Extractor is:
    extractor = Extractor(pdf=your_pdf_data, keepBrTags=0, getPermission=0, logFilePath="", verbose=0, configFile="", timeout=0, sentenceJoinPath="", kenlmPath="")

which contains the same arguments as PDFExtract [command line options](https://github.com/bitextor/pdf-extract/#command-line-pdf-extraction).

Then, to extract relevant content:

    extracted_html = extractor.extract()



