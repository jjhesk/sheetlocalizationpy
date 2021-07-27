import os
import time
from typing import Iterable, Any

import pandas as pd

from .Err import TransformError
from .transformers.Android import Android
from .transformers.Jsi18n import Jsi18n
from .transformers.PyLan import PyLan

statement = 'End : {}, IO File {}'


class Reader:
    Transformers = {
        "i18n": Jsi18n,
        "Android": Android,
        "py": PyLan
    }

    def __init__(self):
        self.key = "KEY"
        self.column = "CN"
        self.row_index = 1
        self.transformerEngine = None
        self._output_file_format = None
        self._defaultEncoding = "utf8"
        self._output_key_lowercase = True
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

    def startRow(self, s: int) -> "Reader":
        self.row_index = s
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
        # self._output_file_format = False

    def _getfilename(self) -> str:
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

    def LoopExcel(self, input_file_path: str) -> "Reader":
        if not self.transformerEngine:
            raise TransformError
        if not self._output_file_format:
            self._output_file_format = self.transformerEngine.autoFileName()

        data = pd.read_excel(input_file_path)
        df = pd.DataFrame(data, columns=[self.key, self.column])
        print(f"size {df.size / 2}")
        for index, row in df.iterrows():
            # trim line
            raw_key = str(row[self.key])
            raw_value = str(row[self.column]).translate(str.maketrans('', '', '\n\t\r'))

            if index == 0:
                self.AppendCacheLine(self.transformerEngine.autoGeneratedTag())

            if index > 0:

                if self.transformerEngine.isCommonKey(raw_key):
                    print(f"is common now {index}")
                    continue

                self.AppendCacheLine(
                    self.transformerEngine.transformKeyValue(raw_key, raw_value, index == df.size / 2 - 1)
                )

        self.lines = self.transformerEngine.wrap_file(self.column, self.lines)

        file = self._getfilename()
        self.writeFile("", file)
        file_io = open(file, 'a')
        for line in self.lines:
            file_io.write("{}\n".format(line))
        file_io.close()
        return self

    def LoopMatrix(self, reader: Iterable[Iterable[Any]]) -> "Reader":
        """
        enable the reader to start working
        :param reader:
        :return:
        """
        if not self.transformerEngine:
            raise TransformError
        if not self._output_file_format:
            self._output_file_format = self.transformerEngine.autoFileName()
        self.row_index = 0
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

        self.lines = self.transformerEngine.wrap_file(self.column, self.lines)

        file = self._getfilename()
        self.writeFile("", file)
        file_io = open(file, 'a')
        for line in self.lines:
            file_io.write("{}\n".format(line))
        file_io.close()

        return self

    def LoopTable(self, reader: Iterable[Iterable[Any]]) -> "Reader":
        """
        enable the reader to start working
        :param reader:
        :return:
        """
        if not self.transformerEngine:
            raise TransformError
        if not self._output_file_format:
            self._output_file_format = self.transformerEngine.autoFileName()
        # self.row_index = 1
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

        self.lines = self.transformerEngine.wrap_file(self.column, self.lines)

        file = self._getfilename()
        self.writeFile("", file)
        file_io = open(file, 'a')
        for line in self.lines:
            file_io.write("{}\n".format(line))
        file_io.close()

        return self
