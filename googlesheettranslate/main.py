import csv
import os
import time
from typing import Iterable, Any

import requests
from bs4 import BeautifulSoup

from .Err import TransformError
from .transformers.Jsi18n import Jsi18n

statement = 'End : {}, IO File {}'


class Reader:
    Transformers = {
        "i18n": Jsi18n
    }

    def __init__(self):
        self.key = "KEY"
        self.column = "CN"
        self.row_index = 1
        self.transformerEngine = None
        self._output_file_format = None
        self._defaultEncoding = "utf8"
        self._output_key_lowercase = False
        self.__debug = False
        self.lines = list()
        self.target = ""
        self.useEngine("")

    def setDebug(self, debug: bool) -> "Reader":
        self.__debug = debug
        return self

    def setKey(self, _key: str) -> "Reader":
        """
        specification for the KEY column
        :param _key: KEY column in string
        :return:
        """
        self.key = _key
        return self

    def overrideFileFormat(self, format_file: str, forceLowercase: bool) -> "Reader":
        """
        overrider for the file format
        :param format_file:
        :param forceLowercase:
        :return:
        """
        self._output_file_format = format_file
        self._output_key_lowercase = forceLowercase
        return self

    def setLang(self, tag: str) -> "Reader":
        """
        specification for the Language column
        :param tag: it can be the short form of the language column key
        :return:
        """
        self.column = tag
        return self

    def setTarget(self, f: str) -> "Reader":
        """
        to save the translation at the specific file folder target
        :param f:
        :return:
        """
        self.target = f
        return self

    def useEngine(self, tag: str) -> "Reader":
        """
        using the engine for the reader to get up
        :param tag:
        :return:
        """
        if tag in self.Transformers:
            self.transformerEngine = self.Transformers[tag]()
        else:
            self.transformerEngine = self.Transformers["i18n"]()
        return self

    def AppendCacheLine(self, info: str):
        """
        for debug purpose the rendering result on each line
        :param info: the line string
        :return:
        """
        if self.__debug:
            print(info)
        self.lines.append(info)

    def newSheet(self):
        """
        to remove the cache and start the newline
        :return:
        """
        self.lines = list()

    def Loop(self, reader: Iterable[Iterable[Any]]):
        """
        enable the reader to start working
        :param reader:
        :return:
        """
        if not self.transformerEngine:
            raise TransformError
        if not self._output_file_format:
            self._output_file_format = self.transformerEngine.autoFileName()

        count = 0
        column_key = 0
        column_val = 0
        raw_key = ""
        raw_value = ""
        # print("{} - now".format(len(reader)))
        for row in reader:
            col = 0

            for rawcc in row:

                if count == self.row_index:
                    name = rawcc.strip()

                    if name == self.key:
                        column_key = col

                    if name == self.column:
                        print("checked - {}".format(name))
                        column_val = col

                if count > self.row_index:
                    name = rawcc.strip()
                    if col is column_key:
                        raw_key = name

                    if col is column_val:
                        raw_value = name

                col = col + 1

            if count == 0:
                self.AppendCacheLine(self.transformerEngine.autoGeneratedTag())

            if count > 0:
                self.AppendCacheLine(
                    self.transformerEngine.transformKeyValue(raw_key, raw_value, count == len(reader) - 1)
                )

            count = count + 1

        self.lines = self.transformerEngine.wrap_file("", self.lines)

        file = self.getFileNameInternal()
        self.writeFile("", file)
        file_io = open(file, 'a')
        for line in self.lines:
            file_io.write("{}\n".format(line))
        file_io.close()

        return self

    def getFileNameInternal(self) -> str:
        if self._output_key_lowercase:
            keyname = self.column.lower()
        else:
            keyname = self.column
        return os.path.join(self.target, self._output_file_format.format(keyname))

    def writeFile(self, content, filename):
        fo = open(filename, "w")
        fo.write(content)
        fo.close()
        print(statement.format(time.ctime(), filename))

    def SortAskOut(self):
        """
        self.writeFile("", self.exchange_data_output)
        with opens(self.downline_batch) as lines:
            for line in lines:
                num = line.translate(str.maketrans('', '', ' \n\t\r'))
                self.NewSort().TradeSortByNumber(num)
                file_object = open(self.exchange_data_output, 'a')
                if len(self.list_downline_people) > 0:
                    file_object.write("[{}]:\n".format(num))
                    file_object.write('\n'.join(self.list_downline_people))
                else:
                    file_object.write("[{}]: NO MEMBERS \n".format(num))
                file_object.close()"""


class GoogleTranslationSheet:
    """
    featured translation service does not need to use creditentials
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:79.0) Gecko/20100101 Firefox/79.0',
        'Accept-Language': 'en-US,en;q=0.5',
        'X-Requested-With': 'XMLHttpRequest'
    }
    proxies = {
        "http": "socks5://127.0.0.1:1086",
        "https": "socks5://127.0.0.1:1086",
    }

    def __init__(self):
        self.exportedSheetUrl = ""
        self.html = ""
        self.tab = ""
        self.engine_name = ""
        self.target_folder = ""
        self.tab_content = dict()
        self.saveToCvs = True
        self.reader_debug = False
        self._readerEngine = Reader()

    def builderCvs(self, enabled: bool) -> "lib":
        """
        enable CVS file save to the local path
        :param enabled:
        :return:
        """
        self.saveToCvs = enabled
        return self

    def builderOutputTarget(self, tar: str) -> "lib":
        """
        save files at the specific target folder
        :param tar:
        :return:
        """
        self.target_folder = tar
        return self

    def builderTransformers(self, engine_name: str) -> "lib":
        """
        using the transform engine from the specification tool
        :param engine_name:
        :return:
        """
        self.engine_name = engine_name
        return self

    def builderReaderDebug(self, de: bool) -> "lib":
        """
        given the extra log detail to the reader
        :param de: yes or no
        :return:
        """
        self.reader_debug = de
        return self

    def builderReader(self, module_reader: Reader) -> "lib":
        """
        building reader module by external instance
        :param module_reader:
        :return:
        """
        self._readerEngine = module_reader
        return self

    def builderMeta(self, url: str, tabname: str = "") -> "lib":
        """
        this is the required for the basic meta information for loading google sheet
        :param url:
        :param tabname:
        :return:
        """
        self.exportedSheetUrl = url
        self.tab = tabname
        return self

    def GetReader(self) -> Reader:
        """
        make modification setting for the internal Reader instance
        :return:
        """
        return self._readerEngine

    def getFileNameInternal(self, index: int) -> str:
        """
        get the naming for the cvs file
        :param index:
        :return:
        """
        return os.path.join(self.target_folder, "data{}.cvs".format(str(index)))

    def run(self, proxies=False, Lang="CN"):
        """
        run up the engine for given parameters
        :param proxies: whether the connection is using VPN or no
        :param Lang: the language column that matched to the sheet
        :return:
        """
        self._readerEngine.newSheet()
        self._readerEngine.setLang(Lang)
        if proxies == True:
            self.html = requests.get(self.exportedSheetUrl, headers=self.headers, proxies=self.proxies).text
        else:
            self.html = requests.get(self.exportedSheetUrl, headers=self.headers).text

        soup = BeautifulSoup(self.html, "lxml")
        tables = soup.find_all("table")
        index = 0
        for table in tables:
            cvs_file = self.getFileNameInternal(index)
            self.tab_content = [[td.text for td in row.find_all("td")] for row in table.find_all("tr")]
            if self.saveToCvs:
                with open(cvs_file, "w") as f:
                    wr = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
                    wr.writerows(self.tab_content)

            self._readerEngine.setDebug(self.reader_debug).setTarget(self.target_folder).useEngine(
                self.engine_name).Loop(self.tab_content)

            index = index + 1
