import time
import threading
import psutil
import pythoncom
import win32com.client
# from win32com.server.util import wrap
from datetime import datetime
from . import Event


class QuoteServer():

    MAX_REGISTERED_TOPICS = 1024

    def __init__(self, sampling=1):
        if not "daqKingCon.exe" in (p.name() for p in psutil.process_iter()):
            raise('請先登入康和金好康')

        self._topic = {}
        self.OnQuoteUpdate = Event()
        self.available = threading.Event()
        self._thread = threading.Thread(target=self.start, kwargs={'sampling' : sampling})
        self._run = True
        self._thread.start()
        self.available.wait()

    def start(self, sampling=0.5):
        self._rtd = win32com.client.Dispatch(dispatch='xqrtd.rtdservercsc')
        self.available.set()

        while self._run:
            if self._topic:
                (ids, values), count = self._rtd.RefreshData(self.MAX_REGISTERED_TOPICS)
                for id_, value in zip(ids, values):
                    if id_ is None and value is None:
                        # This is probably the end of message
                        continue
                    assert id_ in self._topic.keys(), "Topic ID {} is not registered.".format(id_)

                    commodity, topic = self._topic[id_]
                    self.OnQuoteUpdate.notify(commodity, topic, value)
            time.sleep(sampling)

    def stop(self):
        self._run = False
        self._thread.join()

    def register_topic(self, commodity, topic):
        available_ids = set(range(self.MAX_REGISTERED_TOPICS)) - set(self._topic.keys())
        id_ = available_ids.pop()
        self._topic[id_] = (commodity, topic)
        self._rtd.ConnectData(id_, ("{}-{}".format(commodity, topic),), True)

    def unregister_topic(self, commodity, topic):
        found = False
        for id_, (c, t) in self._topic.items():
            if (c, t)==(commodity, topic):
                found = True
                break
        
        if found:
            self._rtd.DisconnectData(id_)
            self._topic.pop(id_, None)
    
    def code_convert(self, commodity, commodity_type='F', strike_price=0, expire_date=datetime.now(), after_hour=False):
        if commodity_type=='S':
            topic = "{C}.TW".format(C=commodity)
        elif commodity_type=='F':
            topic = "FI{C}{A}{M:02}.TF".format(C=commodity,
                                               A='N' if after_hour else '',
                                               M=expire_date.month)
        elif commodity_type=='C' or commodity_type=='P':
            topic = "{C}{A}{M:02}{T:1}{S:05}.TF".format(C=commodity,
                                                        A='N' if after_hour else '',
                                                        T=commodity_type,
                                                        S=strike_price,
                                                        M=expire_date.month)
        return topic


