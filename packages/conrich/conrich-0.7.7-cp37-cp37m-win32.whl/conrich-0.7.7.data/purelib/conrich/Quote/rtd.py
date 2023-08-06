import functools

import pythoncom
import win32com.client
from win32com import universal
from win32com.client import gencache
from win32com.server.util import wrap


EXCEL_TLB_GUID = '{00020813-0000-0000-C000-000000000046}'
EXCEL_TLB_LCID = 0
EXCEL_TLB_MAJOR = 1
EXCEL_TLB_MINOR = 9

gencache.EnsureModule(EXCEL_TLB_GUID, EXCEL_TLB_LCID, EXCEL_TLB_MAJOR, EXCEL_TLB_MINOR)

universal.RegisterInterfaces(EXCEL_TLB_GUID,
                             EXCEL_TLB_LCID, EXCEL_TLB_MAJOR, EXCEL_TLB_MINOR,
                             ['IRtdServer', 'IRTDUpdateEvent'])


# noinspection PyProtectedMember
class ObjectWrapperCOM:
    """
    This object can act as a wrapper for an object dispatched using win32com.client.Dispatch
    Sometimes the object written by 3rd party is not well constructed that win32com will not be able to obtain
    type information etc in order to cast the object to a certain interface. win32com.client.CastTo will fail.

    This wrapper class will enable the object to call its methods in this case, even if we do not know what exactly
    the wrapped object is.
    """
    LCID = 0x0

    def __init__(self, obj):
        self._impl = obj  # type: win32com.client.CDispatch

    def __getattr__(self, item):
        flags, dispid = self._impl._find_dispatch_type_(item)
        if dispid is None:
            raise AttributeError("{} is not a valid property or method for this object.".format(item))
        return functools.partial(self._impl._oleobj_.Invoke, dispid, self.LCID, flags, True)


# noinspection PyPep8Naming
class RTDUpdateEvent:
    """
    Implements interface IRTDUpdateEvent from COM imports
    """
    _com_interfaces_ = ['IRTDUpdateEvent']
    _public_methods_ = ['Disconnect', 'UpdateNotify']
    _public_attrs_ = ['HeartbeatInterval']

    # Implementation of IRTDUpdateEvent.
    HeartbeatInterval = -1

    def __init__(self, event_driven=True):
        self.ready = False
        self._event_driven = event_driven

    def UpdateNotify(self):
        if self._event_driven:
            self.ready = True

    def Disconnect(self):
        pass


class RTDClient:
    """
    Implements a Real-Time-Data (RTD) client for accessing COM data sources that provide an IRtdServer interface.
    """

    MAX_REGISTERED_TOPICS = 1024

    def __init__(self, class_id):
        """
        :param classid: can either be class ID or program ID
        """
        self._class_id = class_id
        self._rtd = None
        self._update_event = None

        self._topic_to_id = {}
        self._id_to_topic = {}
        self._topic_values = {}
        self._last_topic_id = 0

    def connect(self, event_driven=True):
        """
        Connects to the RTD server.

        Set event_driven to false if you to disable update notifications.
        In this case you'll need to call refresh_data manually.
        """

        dispatch = win32com.client.Dispatch(self._class_id)
        self._update_event = RTDUpdateEvent(event_driven)
        try:
            self._rtd = win32com.client.CastTo(dispatch, 'IRtdServer')
        except TypeError:
            # Automated makepy failed...no detailed construction available for the class
            self._rtd = ObjectWrapperCOM(dispatch)

        self._rtd.ServerStart(wrap(self._update_event))

    def update(self):
        """
        Check if there is data waiting and call RefreshData if necessary. Returns True if new data has been received.
        Note that you should call this following a call to pythoncom.PumpWaitingMessages(). If you neglect to
        pump the message loop you'll never receive UpdateNotify callbacks.
        """
        # noinspection PyUnresolvedReferences
        pythoncom.PumpWaitingMessages()
        if self._update_event.ready:
            self._update_event.ready = False
            self.refresh_data()
            return True
        else:
            return False

    def refresh_data(self):
        """
        Grabs new data from the RTD server.
        """

        (ids, values), count = self._rtd.RefreshData(self.MAX_REGISTERED_TOPICS)
        for id_, value in zip(ids, values):
            if id_ is None and value is None:
                # This is probably the end of message
                continue
            assert id_ in self._id_to_topic, "Topic ID {} is not registered.".format(id_)
            topic = self._id_to_topic[id_]
            self._topic_values[topic] = value

    def get(self, topic: tuple):
        """
        Gets the value of a registered topic. Returns None if no value is available. Throws an exception if
        the topic isn't registered.
        """
        assert topic in self._topic_to_id, 'Topic %s not registered.' % (topic,)
        return self._topic_values.get(topic)

    def register_topic(self, topic):
        """
        Registers a topic with the RTD server. The topic's value will be updated in subsequent data refreshes.
        """
        if topic not in self._topic_to_id:
            id_ = self._last_topic_id
            self._last_topic_id += 1

            self._topic_to_id[topic] = id_
            self._id_to_topic[id_] = topic

            self._rtd.ConnectData(id_, (topic,), True)

    def unregister_topic(self, topic):
        """
        Un-register topic so that it will not get updated.
        :param topic:
        :return:
        """
        assert topic in self._topic_to_id, 'Topic %s not registered.' % (topic,)
        self._rtd.DisconnectData(self._topic_to_id[topic])

    def disconnect(self):
        """
        Closes RTD server connection.
        :return:
        """
        self._rtd.ServerTerminate()