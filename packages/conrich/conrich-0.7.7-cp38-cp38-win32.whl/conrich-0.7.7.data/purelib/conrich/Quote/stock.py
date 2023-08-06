# -*- coding: utf-8 -*-
import os, sys
dir_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dir_path)
from . import QuoteServer


class StockQuote(QuoteServer):

    _format = "{}.TW-{}"
