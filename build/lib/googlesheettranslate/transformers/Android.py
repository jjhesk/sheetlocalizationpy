from .corehelper import *
from .itransformer import InterfaceTransform


# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility


class Android(InterfaceTransform):
    def __init__(self):
        self.name = "AndroidTransformer"

    def __eq__(self, profile):
        return self.id == profile.id  # I made it up the id property.

    def __lt__(self, profile):
        return self.id < profile.id

    def __hash__(self):
        return hash(self.id)

    """ implementation of interface transformation """

    def autoGeneratedTag(self) -> str:
        return "<!-- AUTO-GENERATED - DO NOT EDIT THE LINES BELOW-->"

    def autoFileName(self) -> str:
        return "values-{}.xml"

    def transformComment(self, comment: str) -> str:
        """comment replace"""
        return "<!-- {} -->".format(comment)

    # You can manually specify the number of replacements by changing the 4th argument
    def transformKeyValue(self, key: str, value: str, isLast: bool = False) -> str:
        if key.find(" ", 0) > -1:
            return self.transformComment(key)

        if len(key) == 0:
            return ""

        normalizedValue = RegexBoxNewLine(value)
        normalizedValue = RegexBoxSingleQued(normalizedValue)
        normalizedValue = RegexBoxDoubleQuoteReverse(normalizedValue)
        normalizedValue = RegexBoxAt2String(normalizedValue)
        normalizedValue = RegexBoxSDF(normalizedValue)
        normalizedValue = RegexBoxAmp(normalizedValue)
        normalizedValue = RegexBoxu0A00(normalizedValue)
        normalizedValue = RegexBoxCodeDot3(normalizedValue)
        normalizedValue = RegexBoxCodeDot3(normalizedValue)
        normalizedValue = RegexBoxBR(normalizedValue)
        normalizedValue = RegexLinkCase(normalizedValue)

        line_template = '<string name="{}">{}</string>'
        line = line_template.format(key, normalizedValue)

        # currPos = line.find("%#$", 0)

        return line

    def wrap_file(self, input: str, newValues: list) -> list:

        return [
                   '<?xml version="1.0" encoding="utf-8"?>',
                   '<resources>'
               ] + newValues + [
                   '</resources>'
               ]
