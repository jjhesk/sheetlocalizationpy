# !/usr/bin/env python
# coding: utf-8
import os

from googlesheettranslate.main import GoogleTranslationSheet

ROOT = os.path.join(os.path.dirname(__file__))

builder = GoogleTranslationSheet().builderOutputTarget(ROOT).builderMeta(
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vR9-Nx_JTxmBP9rRTfGapdWWB2CQ4EBDBHwS8ZbIMg_6_yZcaWE7gVMs4vLd8npOnEUjJhpMnE3cPCS/pubhtml?gid=1872832543&single=true"
)
builder.GetReader().overrideFileFormat("_{}.json", True)
builder.run(True, "CN")
builder.run(True, "EN")
builder.run(True, "ZH")
builder.run(True, "JP")
builder.run(True, "TH")
