import tarfile
from fnmatch import fnmatch
import shutil
from os.path import basename, exists, dirname, abspath, join
import os
import subprocess
#from distutils.core import setup
from setuptools import setup

try:
    from urllib import urlretrieve
except:
    from urllib.request import urlretrieve

__version__ = '3.1.0'
DATAPATH = join(abspath(dirname((__file__))), 'src/pdfextract/data')

def download_or_compile_jars(datapath):
    if not exists(datapath+"/PDFExtract.jar") or not exists(datapath+"/PDFExtract.json"):
        wd = os.getcwd()
        if not exists(datapath+"/pdf-extract"):
            subprocess.check_call(["git","clone","https://github.com/bitextor/pdf-extract.git","--recursive",datapath+"/pdf-extract"])
        os.chdir(datapath+"/pdf-extract/cld3-Java")
        subprocess.check_call(["ant", "jar"])
        subprocess.check_call(["mvn", "install:install-file","-Dfile=cld3-java.jar","-DgroupId=cld3-java","-DartifactId=cld3-java","-Dversion=1.0","-Dpackaging=jar"])
        os.chdir(datapath+"/pdf-extract")
        subprocess.check_call(["git", "pull"])
        subprocess.check_call(["git", "submodule", "update", "--init", "--recursive"])
        subprocess.check_call(["mvn", "package"])
        os.chdir(wd)
        shutil.move(datapath+'/pdf-extract/target/PDFExtract-2.0.jar', datapath+"/PDFExtract.jar")
        shutil.move(datapath+'/pdf-extract/target/PDFExtract.json', datapath+"/PDFExtract.json")
            
            

download_or_compile_jars(datapath=DATAPATH)

setup(
    name='python-pdfextract',
    version=__version__,
    packages=['pdfextract', 'pdfextract.extract'],
    package_dir={'': 'src'},
    package_data={
        'pdfextract': [
            'data/PDFExtract.jar',
            'data/PDFExtract.json'
        ],
    },
    install_requires=[
        'JPype1',
        'chardet',
    ],
    author='Misja Hoebe, Leopoldo Pla',
    author_email='misja.hoebe@gmail.com, lpla@dlsi.ua.es',
    maintainer='Matthew Russell, Leopoldo Pla',
    maintainer_email='ptwobrussell@gmail.com, lpla@dlsi.ua.es',
    url='https://github.com/bitextor/python-pdfextract/',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Natural Language :: English',
    ],
    keywords='pdfextract',
    license='Apache 2.0',
    description='Python interface to pdf-extract, HTML Extraction from PDF pages'
)
