from jpype import *
import chardet
import threading

lock = threading.Lock()

ByteArrayInputStream        = JClass('java.io.ByteArrayInputStream')
ByteArrayOutputStream       = JClass('java.io.ByteArrayOutputStream')


class Extractor(object):
    extractor = None
    data      = None

    def __init__(self, **kwargs):
        if 'pdf' in kwargs:
            self.data = kwargs['pdf']
        if "keepBrTags" in kwargs:
            self.keepBrTags = int(kwargs['keepBrTags'])
        else:
            self.keepBrTags = 0
        if "getPermission" in kwargs:
            self.getPermission = int(kwargs['getPermission'])
        else:
            self.getPermission = 0
        if "logFilePath" in kwargs:
            self.logFilePath = kwargs['logFilePath']
        else:
            self.logFilePath = ""
        if "verbose" in kwargs:
            self.verbose = int(kwargs['verbose'])
        else:
            self.verbose = 0
        if "configFile" in kwargs:
            self.configFile = kwargs['configFile']
        else:
            self.configFile = ""
        if "timeout" in kwargs:
            self.timeout = JLong(kwargs['timeout'])
        else:
            self.timeout = 0
        if "kenlmPath" in kwargs:
            self.kenlmPath = kwargs['kenlmPath']
            if self.kenlmPath == "":
                self.kenlmPath = None
        else:
            self.kenlmPath = None
        if "sentenceJoinPath" in kwargs:
            self.sentenceJoinPath = kwargs['sentenceJoinPath']
            if self.sentenceJoinPath == "":
                self.sentenceJoinPath = None
        else:
            self.sentenceJoinPath = None
        try:
            # make it thread-safe
            if threading.activeCount() > 1:
                if isThreadAttachedToJVM() == False:
                    attachThreadToJVM()
            lock.acquire()
            self.extractor = JClass("pdfextract.PDFExtract")(self.logFilePath, self.verbose, self.configFile, self.timeout, self.kenlmPath, self.sentenceJoinPath)

        finally:
            lock.release()

    def setData(self,data):
        self.data = data

    def getHTML(self):
        self.reader = ByteArrayInputStream(self.data)
        return str(self.extractor.Extract(self.reader, self.keepBrTags, self.getPermission).toString())
