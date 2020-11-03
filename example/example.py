# !/usr/bin/env python
# coding: utf-8
import os

from googlesheettranslate.main import GoogleTranslationSheet

ROOT = os.path.join(os.path.dirname(__file__))
sheetID = "fjosijfijsoeif"
gid = "fjsoaiejfoijseoifjo"
builder = GoogleTranslationSheet().builderOutputTarget(ROOT).builderMeta(
    "https://docs.google.com/spreadsheets/d/e/{}/pubhtml?gid={}&single=true".format(sheetID, gid)
)
# builder.GetReader().overrideFileFormat("_{}.json", True)
builder.builderTransformers("Android")
builder.run(True, "CN")
builder.run(True, "EN")
builder.builderTransformers("i18n")
builder.run(True, "CN")
builder.run(True, "EN")
