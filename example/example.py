# !/usr/bin/env python
# coding: utf-8

from googlesheettranslate.main import lib, Reader

builder = lib().builderCvs(True).builderTransformers("i18n").builderMeta(
    'https://docs.google.com/spreadsheets/d/e/2PACX-1vR9-Nx_JTxmBP9rRTfGapdWWB2CQ4EBDBHwS8ZbIMg_6_yZcaWE7gVMs4vLd8npOnEUjJhpMnE3cPCS/pubhtml',
    'ethcap'
)

builder.builderReader(Reader().setLang("CN")).run(True)
