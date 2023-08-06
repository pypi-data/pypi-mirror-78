# -*- coding: utf-8 -*-
import os, sys
dir_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dir_path)
from datetime import datetime
from . import QuoteServer


class FuturesQuote(QuoteServer):

    _format = "{}.TF-{}"

    def code_convert(self, commodity, commodity_type='F', strike_price=0, expire_date=datetime.now(), after_hour=False):
        if commodity_type=='F':
            topic = "FI{C}{A}{M:02}".format(C=commodity,
                                            A='N' if after_hour else '',
                                            M=expire_date.month)
        else:
            topic = "{C}{A}{M:02}{T:1}{S:05}".format(C=commodity,
                                                     A='N' if after_hour else '',
                                                     T=commodity_type,
                                                     S=strike_price,
                                                     M=expire_date.month)
        return topic




