#   Copyright (C) 2020 David Krasnitsky
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

# import logging
import sys
import re
import timeit

import json

from collections import deque
from enum import Enum
from . import data as siemkit_data
from collections import ChainMap

# ToDo: 1. Timeformats -> Have the time.py to either specify a format to parse, turn into a timestamp,
#  or have the 'auto' string for using the timeparse library.
# ToDo: 2. On the first with() statement where the Event() contains any outputs, start the sessions of all outputs
#  by accessing their __enter__. On the most outter (or same level of initial outputs?),
#  perform the __exit__ on all outputs.
#   -Treat as sessions, thinking about writing to files or having a managed TCP connection.
#   -Connectionless just don't manage anything, they just write on command.
# ToDo: 3. Create a customizable output option. Make CSV files using those customized file types.

# import dateparser  # This can't be good for performance. Need performance? know your formats!


# def get_timestamp(string_time):
#    ts = dateparser.parse(string_time).timestamp() * 1000
#    return str(ts)

# logging.basicConfig(level=logging.DEBUG)

# ToDo: Manual Time Format with Declared fields as time -> Directed for performance
# ToDo: Automatic Time Format detection -> Comfortable but requires an external library + performance penalty.
# ToDo: Consider a syntax sugar for this: for _ in range(3000): _ = send.udp("127.0.0.1", 514, bytes(random_event(event)))  # Random certain aspects of the event.

class CefSeverity(str, Enum):

    UNKNOWN = 'Unknown',
    LOW = 'Low',
    MEDIUM = 'Medium',
    HIGH = 'High',
    VERY_HIGH = 'Very-High'

    def __str__(self):
        return self.value


def filter_fields(events, allowed_fields):
    """
    Filter fields that are not within the `allowed_fields` argument. Yielding events with discarded unknown fields.
    :param events:
    :param allowed_fields:
    :return:
    """
    yield  # event


def validated(events, validator):
    """
    A new comer friendly generator for filtering non-validated events
    :param events: An events collection / iterable
    :param validator: A validation, filter function
    :return: Validated events
    """
    yield


def entities(events, aggregation_base):
    """
    Generate entities out of events, creating time-lines.
    :param events:
    :param aggregation_base:
    :return:
    """
    yield


def generator(amount=-1):
    # ToDo: yield random event data for simulations
    pass


class States:

    def __init__(self, optimized_size=5):
        self.__init_optimized_size = optimized_size
        self.__optimized_size = optimized_size
        self.__states = list((dict() for _ in range(optimized_size)))
        self.__index = 0

    def save(self, state):
        """
        Update initial root state.
            This state is restored either by the `reset(self)` method or by one or more calls from the `restore(self)`.
        :param state: A dictionary
        :return:
        """
        self.__states[0].clear()
        self.__states[0].update(state)

    def reset(self):
        """
        Reset to initial root state
        :return:
        """
        state_zero = self.__states[0]
        self.clear()
        return state_zero

    def store(self, state):
        if self.__index == self.__optimized_size:
            self.__states.append(dict())
            self.__optimized_size += 1

        self.__states[self.__index].clear()
        self.__states[self.__index].update(state)
        self.__index += 1
        return self

    def restore(self):
        if self.__index - 1 <= 0:  # Doesn't update the index, thus protecting the first state.
            return self.__states[0]

        result = self.__states[self.__index - 1]
        self.__index -= 1
        return result

    def clear(self):
        self.__optimized_size = self.__init_optimized_size
        self.__index = 0
        self.__states = list((dict() for _ in range(self.__optimized_size)))
        return self


class EventFormat(dict):

    __aliases = {}

    __default_aliases = {}

    __default_keys = set()

    @classmethod
    def default_keys(cls):
        return set(cls.__default_keys)

    @classmethod
    def default_aliases(cls):
        return dict(cls.__default_keys)

    @staticmethod
    def key_assertion(key):
        return True

    @staticmethod
    def value_assertion(key):
        return True

    """@staticmethod
    def syslog_header2(format_="{:%b %d %H:%M:%S} {} {} "):
        import socket
        from datetime import datetime
        fully_qualified_name = socket.getfqdn()
        ip_address = socket.gethostbyname(fully_qualified_name)
        return format_.format(datetime.now(), ip_address, fully_qualified_name)"""

    @staticmethod
    def syslog_header(time_format="%b %d %H:%M:%S"):
        import socket
        from datetime import datetime
        fully_qualified_name = socket.getfqdn()
        ip_address = socket.gethostbyname(fully_qualified_name)
        return f"{datetime.now().strftime(time_format)} {ip_address} {fully_qualified_name}"
        # return format_.format(datetime.now(), ip_address, fully_qualified_name)

    @staticmethod
    def serializer(headers, data):

        def escape(value, is_header):
            """if type(value) in (int, bool):
                return bytes(str(value), 'utf-8')
            elif type(value) is str:
                value = bytes(value, 'utf-8')"""

            if not isinstance(value, str):
                return bytes(str(value), 'utf-8')
            else:
                value = bytes(value, 'utf-8')

            # Cancelled: Time it vs str.translate()
            # Although fast, this is not efficient. Looking for a better solution.

            value = value.replace(b'\\', rb'\\')  # According to documentations, this is the right behaviour.
            # CommonEventFormatV25.pdf page 7

            if is_header:
                value = (value
                         .replace(b'\n', b' ')
                         .replace(b'\r', b' '))
            else:
                value = (value
                         .replace(b'\n', rb'\n')
                         .replace(b'\r', rb'\r'))

            value = value.replace(b'\t', rb'\t')

            if is_header:
                value = value.replace(b'|', rb'\|')
            else:
                value = value.replace(b'=', rb'\=')

            return value

            """value = value.translate(
                bytes.maketrans(b'\\' rb'\\')
            )"""

            """
            value = value.translate(
                str.maketrans({
                    '\\': r'\\'
                })
            )
            """

        result = bytearray(b'')

        result.extend(b'|'.join((escape(data[header], is_header=True) for header in headers)))

        """for header in headers:
            try:
                #result.extend(b'%s|' % data[header])
            except KeyError:
                pass"""

        result.extend(b'|')

        def generate_extensions(data_):
            for key, value in data_.items():

                if value is str:
                    value = value.strip()

                if (value or value == 0) and (key not in headers):
                    key = key.strip()
                    value = escape(value, is_header=False)
                    yield b'%s=%s' % (bytes(key, 'utf-8'), value)

        # extension = b""
        extension = b' '.join(generate_extensions(data))
        # ^{}:(?P<version>\d)\|(?P<device_vendor>[^\|]+)\|(?P<device_product>[^\|]+)\|(?P<device_version>[^\|]+)\|(?P<signature_id>[^\|]+)\|(?P<signature>[^\|]+)\|(?P<severity>[^\|]+)\|(?P<extensions>.*)
        # ^(?P<headers>.*?){}:(?P<version>\d)\|(?P<device_vendor>[^\|]+)\|(?P<device_product>[^\|]+)\|(?P<device_version>[^\|]+)\|(?P<signature_id>[^\|]+)\|(?P<signature>[^\|]+)\|(?P<severity>[^\|]+)\|(?P<extensions>.*)
        result.extend(extension)

        return result

    @staticmethod
    def deserializer(headers, raw):
        return {}

    @staticmethod
    def to_timestamp():
        pass

    @staticmethod
    def from_timestamp():
        pass

    def __init__(self, format_, version, headers, data=None, raw=b'', aliases=None, fields=None, warnings=False,
                 key_assertion=None, value_assertion=None, deserializer=None, serializer=None, syslog_header=None,
                 timestamp_fields=None, to_timestamp=None, from_timestamp=None, allow_empty_keys=False, outputs=None,
                 tcp=None, udp=None, file=None, size_limit=1024, optimized_state_levels=5):

        """
            format_             - Format name, as will be presented in serialized form (CEF, LEEF, etc.)
            version             - Format Version: 0, 1, 0.1, 1.0, etc. (CEF:0, LEEF:1.0)
            headers             - Header title names, ordered correctly for processing
            data                - Assign values using dictionary object
            raw                 - Unparsed raw event
            aliases             - Aliases dictionary for key access
            fields     - Declare field names for optional enforcement, spelling tests, correctness & other
                                    possible assistance.
                                    [Move to flag -> If declared, only these keys will be allowed.
                                    Exceptions message will tip for close matches]
            warnings            - Warn about bad usage / practices
            key_assertion       - Assertion function to test the key's creation / access correctness
            value_assertion     - Assertion function to test the value's assignment correctness
            deserializer        - Parser function to convert formatted event bytes into an event dictionary
            serializer          - Process function to convert the event dictionary into formatted event bytes
            timestamp_fields    - Declare which fields are timestamps to automatically format or parse them
            to_timestamp        - A function to convert a string into a timestamp
            from_timestamp      - A function to convert a timestamp into a formatted string
            allow_empty_keys    - Produce empty keys: key=<no value>
            output              - An object, or collection of objects, that implement the write() method in order
                                    to serialize changes. e.g. Network Socket, File, etc.
            tcp                 - TCP IP:Port address or collection of addresses to send events to over TCP protocol
            udp                 - UDP IP:Port address or collection of addresses to send events to over UDP protocol
            file                - File path to output an events file
            size_limit          - The event size limit. In order to avoid potential size exploits.
        """

        super().__init__()
        if timestamp_fields is None:
            timestamp_fields = set()

        if data is None:
            data = {}

        if key_assertion is None:
            key_assertion = EventFormat.key_assertion
        self.__key_assertion = key_assertion

        if deserializer is None:
            deserializer = EventFormat.deserializer
        self.__deserializer = deserializer

        if serializer is None:
            serializer = EventFormat.serializer
        self.__serializer = serializer

        if syslog_header is None:
            syslog_header = EventFormat.syslog_header
        self.__syslog_header = syslog_header

        if aliases is None:
            aliases = {}

        if fields is None:
            fields = set()

        # Keep the dictionary outside of the object's scope in order to avoid paradox when setting/getting data.
        EventFormat.__aliases[id(self)] = aliases

        # ToDo: If 'restrict_keys', allow /assert only access to the given keys. -> replaced with 'assert_key' function
        # If given a wrong one, throw missing key/attribute exception.

        self.__format = format_
        self.__version = version
        self.__format_version = bytes("{}:{}|".format(format_, version), 'utf-8')

        # Assumption: If you provide a JSON, and RAW then JSON is static info where RAW is dynamical.
        if data:
            """# Clone external dict to avoid changing anything
            json = dict(json)

            # Test if someone is trying to mess around with us
            if 'version' in json:
                del json['version']
            if 'format' in json:
                del json['format']
            """
            self.update(data)
        if raw:
            self.update(deserializer(headers, raw))

        # self.update(json)

        self.__headers_order = headers  # Important to know the order
        self.__headers_hash_set = set(headers)  # Much faster to test against.
        self.__aliases = aliases
        self.__fields = fields
        self.__fields.update(siemkit_data.words_set(aliases))

        # self.__headers_set = set(headers)

        # After all values are set for the first time, use them as default for the `clear()` command.
        self.__states = States(optimized_size=optimized_state_levels)
        self.__states.store(self)
        #self.__default_state = {}
        #self.__default_state.update(self)

        self.__raw = raw
        self.__detected_changes = True

        self.__timestamp_fields = timestamp_fields
        self.__to_timestamp = to_timestamp
        self.__from_timestamp = from_timestamp

        self.__commit_context = False

        self.__output = None
        self.output(outputs)

    def update_aliases(self, aliases):
        EventFormat.__aliases[id(self)].update(aliases)
        return self

    def assign_aliases(self, aliases):
        EventFormat.__aliases[id(self)] = aliases
        return self

    def output(self, outputs):

        if outputs is not None and not any(
                isinstance(outputs, type_) for type_
                in (list, tuple, set, deque)
        ):
            self.__output = (outputs,)
        else:
            self.__output = outputs

    def __build(self):
        return bytes(self.__format_version + self.__serializer(self.__headers_order, self))

    def raw(self):
        # ToDo: For CEF: Make an aggregation version too + b'cnt='

        if self.__detected_changes:
            self.__raw = self.__build()
            self.__detected_changes = False

        return self.__raw

    def parse(self, raw):
        # ToDo: Check if raw is byte or str
        # ToDo: Support Syslog header
        # ToDo: Parse and update this object
        # ToDo: For CEF: Exam -> Aggregation (cnt += 1) if the new raw value equals to the current one in the object
        # ToDo: Implement a generic aggregation such as described above,
        #   for which each format standard will refer differently
        # ToDo: Aggregate only if data was not sent(aka self.write() <- Have it reset the aggregation to 1)
        pass

    def update(self, d, **f):

        # Force key translation by re-assigning
        for key, value in d.items():
            self[key] = value

        for key, value in f.items():
            self[key] = value

        return self

    def write(self):

        size = 0

        if self.__output:

            payload = bytes(self) + b'\r\n'

            for output in self.__output:
                size += output.write(payload)

        return size

    def __get(self, key, ignore_exception=False):

        self_id = id(self)

        # If attribute has double underscores, treat as a single space.
        if '__' in key:
            key = key.replace('__', ' ')

        if key in EventFormat.__aliases[self_id]:
            key = EventFormat.__aliases[self_id][key]

        if ignore_exception:
            return super().get(key, None)

        return super().__getitem__(key)

    def __getattr__(self, name):

        # We get here when accessing an attribute that doesn't exist

        return self.__get(name, ignore_exception=True)

    def __getitem__(self, key):
        # name = self.__translation.get(key, key) # If translation doesn't exist, use itself.
        # return super().__getitem__(key)
        return self.__get(key)

    def __set(self, key, value):
        # super().__setattr__(key, value) # Value is an object in the heap. We just set a reference here.
        # Do not set attribute, that way we enforce the calling of __getattr__
        self.__detected_changes = True  # Restoring state means editing.
        self.__commit_context = True
        self_id = id(self)
        if key in EventFormat.__aliases[self_id]:
            key = EventFormat.__aliases[self_id][key]
        super().__setitem__(key, value)
        return self

    def __setattr__(self, name, value):

        # Don't update private variables in the dictionary.
        if name.startswith("_EventFormat_"):
            return super().__setattr__(name, value)

        # If attribute has double underscores, treat as a single space.
        if '__' in name:
            name = name.replace('__', ' ')

        self.__set(name, value)

        return self

    def __setitem__(self, key, value):
        return self.__set(key, value)

    def __delete(self, key):
        super().__delitem__(key)

    def __delattr__(self, name):
        self.__delete(name)

    def __delitem__(self, key):
        self.__delete(key)

    def __enter__(self):
        self.__commit_context = True
        self.store()
        return self

    def __exit__(self, type_, value, traceback):
        if traceback:
            raise

        if self.__commit_context:
            if self.__output:
                self.write()

            # We make sure that only the most inner & recent context is committed
            # to allow predicted behaviour
            # self.__commit_context = False

        # ToDo: If a parse() method was activated, use super.clear() instead?
        # ToDo: Or use a different writing style for parsing:

        self.restore()
        # We make sure that only the most inner & recent context is committed
        # to allow predicted behaviour
        self.__commit_context = False

        # Todo: Check: if this is the last context, if so, close all outputs.
        #             for output in self.__output:
        #                   output.close()
        return self

    def abort(self):
        """
        Works only within most inner `with` statement (context manager).
         Aborts output on exit for assigned values.
        :return:
        """
        self.__commit_context = False
        return self

    # Set current values as default
    def save(self):
        """
        Set the current state as root state.
        :return:
        """
        self.__states.save(self)
        return self

    def reset(self):
        """
        Reset current state to the saved root state.
        :return:
        """
        state = self.__states.reset()
        super().clear()
        self.update(state)
        return self  # Return to root state

    def store(self):
        """
        Store current state.
        :return:
        """
        self.__states.store(self)
        return self

    def restore(self):
        """
        Restore previous state.
        :return:
        """
        state = self.__states.restore()
        super().clear()
        self.update(state)
        return self  # Return to previous state

    # Done: Allow clearing all values, for parsing
    # Done: Or/And provide an automatic way for "clearing" when using the 'with' statement and receiving data
    def clear(self):
        # return self.restore()
        return super().clear()

    def __bytes__(self):
        return self.raw()

    def json(self, indent=None):
        return json.dumps(self, indent=indent)

    def syslog(self):
        return bytes(self.__syslog_header(), 'utf-8') + bytes(self)

    def __str__(self):
        # return super().__str__()
        return str(bytes(self), 'utf-8')

    def close(self):  # Close all used resources -> Files, Sockets, etc.
        pass

    def available_keys(self):

        self.__fields.update(self.keys())
        return set(self.__fields)


class Cef(EventFormat):

    # REF: About Source/Attacker Destination/Target
    # https://community.microfocus.com/t5/ArcSight-User-Discussions/Attacker-Address-versus-Source-Address/td-p/1582901
    # To manually tie attacker and source fields together, assign aliases when creating an event object.
    # e.g.  Cef(aliases={ "attackerAddress": "src" }) will tie attackerAddress to sourceAddress.
    #  Cef(aliases={ "attackerAddress": "src" }) == Cef(aliases={ "attackerAddress": "sourceAddress"})
    __default_aliases = {
        'deviceAction': 'act',
        'applicationProtocol': 'app',
        'baseEventCount': 'cnt',
        'eventOutcome': 'outcome',
        'deviceAddress': 'dvc',
        'deviceHostName': 'dvchost',
        'deviceMacAddress': 'dvcmac',
        'deviceProcessId': 'dvcpid',
        'destinationAddress': 'dst',
        'deviceTimeZone': 'dtz',
        'destinationHostName': 'dhost',
        'destinationMacAddress': 'dmac',
        'destinationNtDomain': 'dntdom',
        'destinationPort': 'dpt',
        'destinationProcessName': 'dproc',
        'destinationProcessId': 'dpid',
        'destinationUserId': 'duid',
        'destinationUserPrivileges': 'dpriv',
        'destinationUserName': 'duser',
        'endTime': 'end',
        'fileName': 'fname',
        'fileSize': 'fsize',
        'bytesIn': 'in',
        'message': 'msg',
        'bytesOut': 'out',
        'transportProtocol': 'proto',
        'receiptTime': 'rt',
        'deviceReceiptTime': 'rt',
        'managerReceiptTime': 'mrt',
        'requestUrl': 'request',
        'requestURL': 'request',
        'sourceAddress': 'src',
        'sourceHostName': 'shost',
        'sourceMacAddress': 'smac',
        'sourcePort': 'spt',
        'sourceUserPrivileges': 'spriv',
        'sourceUserId': 'suid',
        'sourceUserName': 'suser',
        'sourceNtDomain': 'sntdom',
        'sourceProcessId': 'spid',
        'sourceProcessName': 'sproc',
        'startTime': 'start',
        'deviceEventCategory': 'cat',
        'deviceCustomString1Label': 'cs1Label',
        'deviceCustomString2Label': 'cs2Label',
        'deviceCustomString3Label': 'cs3Label',
        'deviceCustomString4Label': 'cs4Label',
        'deviceCustomString5Label': 'cs5Label',
        'deviceCustomString6Label': 'cs6Label',
        'deviceCustomNumber1Label': 'cn1Label',
        'deviceCustomNumber2Label': 'cn2Label',
        'deviceCustomNumber3Label': 'cn3Label',
        'deviceCustomString1': 'cs1',
        'deviceCustomString2': 'cs2',
        'deviceCustomString3': 'cs3',
        'deviceCustomString4': 'cs4',
        'deviceCustomString5': 'cs5',
        'deviceCustomString6': 'cs6',
        'deviceCustomNumber1': 'cn1',
        'deviceCustomNumber2': 'cn2',
        'deviceCustomNumber3': 'cn3',
        'deviceCustomIPv6Address1': 'c6a1',
        'deviceCustomIPv6Address1Label': 'c6a1Label',
        'deviceCustomIPv6Address2': 'c6a2',
        'deviceCustomIPv6Address2Label': 'c6a2Label',
        'deviceCustomIPv6Address3': 'c6a3',
        'deviceCustomIPv6Address3Label': 'c6a3Label',
        'deviceCustomIPv6Address4': 'c6a4',
        'deviceCustomIPv6Address4Label': 'c6a4Label',
        'deviceCustomFloatingPoint1': 'cfp1',
        'deviceCustomFloatingPoint1Label': 'cfp1Label',
        'deviceCustomFloatingPoint2': 'cfp2',
        'deviceCustomFloatingPoint2Label': 'cfp2Label',
        'deviceCustomFloatingPoint3': 'cfp3',
        'deviceCustomFloatingPoint3Label': 'cfp3Label',
        'deviceCustomFloatingPoint4': 'cfp4',
        'deviceCustomFloatingPoint4Label': 'cfp4Label',
        'agentAddress': 'agt',
        'agentHostName': 'ahost',
        'agentId': 'aid',
        'agentMacAddress': 'amac',
        'agentReceiptTime': 'art',
        'agentType': 'at',
        'agentTimeZone': 'atz',
        'agentVersion': 'av',
        'destinationGeoLatitude': 'dlat',
        'destinationGeoLongitude': 'dlong',
        'sourceGeoLatitude': 'slat',
        'sourceGeoLongitude': 'slong',
        'severity': 'deviceSeverity'
    }

    __default_keys = siemkit_data.words_set(__default_aliases)

    __default_keys.update({
        'attackerAddress',
        'attackerHostName',
        'attackerMacAddress',
        'attackerPort',
        'attackerUserPrivileges',
        'attackerUserId',
        'attackerUserName',
        'attackerNtDomain',
        'attackerProcessId',
        'attackerProcessName',
        'attackerGeoLatitude',
        'attackerGeoLongitude'
        'targetHostName',
        'targetAddress',
        'targetMacAddress',
        'targetNtDomain',
        'targetPort',
        'targetProcessName',
        'targetProcessId',
        'targetUserId',
        'targetUserPrivileges',
        'targetUserName',
        'targetGeoLatitude',
        'targetGeoLongitude',
        'deviceVendor',
        'deviceProduct',
        'deviceVersion',
        'deviceEventClassId',
        'name',
        'deviceSeverity'
    })

    @classmethod
    def default_keys(cls):
        return set(cls.__default_keys)

    @classmethod
    def default_aliases(cls):
        return dict(cls.__default_aliases)

    def __init__(
            self,
            version=0,
            data=None,
            raw=b'',
            aliases=None,
            fields=None,
            key_assertion=None,
            deserializer=None,
            serializer=None,
            timestamp_fields=None,
            to_timestamp=None,
            from_timestamp=None,
            allow_empty_keys=False,
            outputs=None,
            tcp=None,
            udp=None,
            file=None
    ):

        if fields is None:
            fields = set()

        if data is None:
            data = {}

        if aliases is None:
            aliases = {}

        if timestamp_fields is None:
            timestamp_fields = set()

        cef_key_declaration = set()

        cef_json = {
            'deviceVendor': 'CyberSIEM(R) Community',
            'deviceProduct': 'SIEM Kit',
            'deviceVersion': '0',
            'deviceEventClassId': 100,
            # 'name': 'https://github.com/DK26/cef-prototype',  # https://github.com/cybersiem/community
            'name': 'https://github.com/cybersiem/community',
            'deviceSeverity': CefSeverity.UNKNOWN
        }

        cef_json.update(data)

        default_aliases = Cef.default_aliases()
        cef_key_declaration.update(siemkit_data.words_set(aliases))

        aliases.update(default_aliases)


        #for k, v in cef_aliases.items():
        #    cef_key_declaration.add(k)
        #    cef_key_declaration.add(v)

        # Done: Enable self (double) aliases
        for k, v in aliases.items():
            if v in aliases.keys():
                aliases[k] = aliases[v]
            else:
                aliases[k] = v
        # cef_aliases.update(aliases)

        # Other Key Declaration
        # cef_key_declaration.update()

        # if default_aliases is None:
        #    default_aliases = set(cef_key_declaration)

        # Update potential custom key declarations
        cef_key_declaration.update(cef_json.keys())
        cef_key_declaration.update(fields)

        super().__init__(
            format_='CEF',
            version=version,
            headers=(
                'deviceVendor',
                'deviceProduct',
                'deviceVersion',
                'deviceEventClassId',
                'name',
                'deviceSeverity'
            ),
            data=cef_json,
            raw=raw,
            aliases=aliases,
            fields=cef_key_declaration,
            key_assertion=key_assertion,
            deserializer=deserializer,
            serializer=serializer,
            timestamp_fields=timestamp_fields,
            to_timestamp=to_timestamp,
            from_timestamp=from_timestamp,
            allow_empty_keys=False,
            outputs=outputs,  # DIY
            tcp=tcp,  # Batteries included
            udp=udp,  # Batteries included
            file=file  # Batteries included
        )


class Leef(EventFormat):
    pass


def test():
    m = re.compile('')
    cef_event = "CEF:0|Fake\|Vendor|Fake Product|Device Version|Class ID|Name|Severity|src=127.0.0.1 dst=1.1.1.1 shost=homeland"

    # headers, result = AbstractEventFormat.serializer("CEF", cef_event)

    leef_event = "LEEF:1.0|Fake\|Vendor|Fake Product|Product Version|Event ID|src=127.0.0.1 dst=1.1.1.1"

    # headers, result = AbstractEventFormat.deserializer("LEEF", leef_event)

    event = Cef(version=0,
                aliases={
                    'name': 'really',
                    'msg': 'baby'
                },
                data={
                    'name': 'testing | hmm',
                    'msg': 'original\nnice!=1111 \d \t test'
                })

    print(event.json())
    event.name = 'My Event'
    event.this_must__space__out = 'Nice!'
    print(event.json())
    print(event.name)
    print(event.really)
    print(event['really'])
    print(event['name'])
    print(event.this_must__space__out)
    print(event['this_must space out'])

    event.clear()
    print(event.json())

    event.hello = 'world'

    print(event.json())
    event.store()

    event.hello = 'nice!'
    event.src = "127.0.0.1"

    print(event.json())
    event.restore()
    print(event.json())

    # Automatically restore value to default once leaving context
    with event:
        event.src = '1.1.1.1'
        print(event.json())

    # 'event' is restored to default
    print(event.json())

    import json
    print(json.dumps(event, indent=None))

    print(event)
    print(bytes(event))


def dev_1():
    from telnetlib import Telnet

    with Telnet('172.16.106.3', 9514) as session:  # What if a session is loosing connection
        # for any reason? Add retries?

        event = Cef(outputs=session)

        with event:
            # event.name = "Development"
            event.sourceAddress = "127.0.0.1"
            event.destinationAddress = "192.168.0.1"
            event.sourceUserName = "Dave"
            event.message = 'CreateOffense'

            event.deviceCustomNumber1Label = 'Test Iteration'
            # This creates a new sub-state while keeping previous values.
            for number in range(10):
                with event:
                    event.deviceCustomNumber1 = number
                    print(event)
                    print(event.json(indent=4))
            # Done: Solve: However, leaving inner context still sends an extra event by outter context
            # Done: __enter__ -> flag to serialize, __exit__ check if flagged. If so, serialize, then turn off flag
            # Done: But.. what If we do want that extra event? Then use a new inner context manager.

        with event:
            event.src = "192.168.0.1"
            event.destinationAddress = "127.0.0.1"
            print(event)
            print(event.json(indent=4))

    """

        with Cef(tcp=(172.16.106.3', 9514)) as event:

            with event:
                event.sourceAddress = "127.0.0.1"
                event.sourceUserName = "Dave"
                event.message = "CreateOffense"

            with event:
                event.src = "192.168.0.1"
                print(event)

    """


def dev_2():
    from time import sleep
    from telnetlib import Telnet

    # What if a session is loosing connection for any reason? Add retries?
    ip, port = sys.argv[1:3]
    print(f"{ip}:{port}")

    with Telnet(ip, int(port)) as session:
        event = Cef(outputs=session)

        with event:
            # event.name = "Development"
            event.sourceAddress = "127.0.0.1"
            event.destinationAddress = "192.168.0.1"
            event.sourceUserName = "Dave"
            event.message = 'CreateOffense'
            event.deviceAddress = "172.31.0.1"
            # print(event.syslog())
            print(event)

        with event:
            # event.name = "Development"
            event.sourceAddress = "127.0.0.1"
            event.destinationAddress = "192.168.0.1"
            event.sourceUserName = "Dave"
            event.message = 'CreateOffense2'
            event.deviceAddress = "172.31.0.1"
            print(event)

        sleep(1)

        with event:
            # event.name = "Development"
            event.sourceAddress = "192.168.0.1"
            event.destinationAddress = "127.0.0.1"
            event.sourceUserName = "Dave"
            event.message = 'CreateOffense3'
            event.deviceAddress = "172.31.0.1"
            print(event)
            # payload = event.syslog()
            # print(payload)
            # session.write(payload + b'\r\n')


def dev_3():

    class Printer:
        @classmethod
        def write(cls, bytes_):
            print(str(bytes_, 'utf-8').rstrip())
            return len(bytes_)

    printer = Printer()

    event = Cef()
    event.output(outputs=printer)

    event.name = "DK26 test"
    #event.save()

    first_state = event
    print(f"First: {first_state}")

    with event:
        event.deviceVendor = 'test'
        event.deviceProduct = 'another'
        event.deviceCustomNumber1Label = "Loop Iteration"

        for i in range(10):
            with event:
                event.deviceCustomNumber1 = i

    with event:
        event.deviceVendor = 'someone-else'
        event.deviceProduct = 'something-else'
        # Notice we do not need to zero the 'deviceCustomString1Label'!

    final_state = event
    print(f"Final: {final_state}")
    print(f"Restored Successfully: {final_state == first_state}")


if __name__ == "__main__":
    # test()
    dev_3()

    # Test

#  """
#             with event:
#                 while has_events:
#                     event.parse(...) # Includes clear in the process
#
#                     <do something with event>
#
#         """
#         # Or:
#         """
#             while has_events:
#                 event.parse(...) # Includes clear in the process
#                 with event:
#                     my_data = event.sourceAddress
#                     # Clear on exit
#         """
#         # Or:
#         """
#             while has_events:
#                 with event.parse(...) as parsed_event:
#                     my_data = parsed_event.sourceAddress
#                     # Clear on exit
#         """
#         # Or:
#         """
#             with event:
#                 while has_events:
#                     event.parse(...) # Includes clear in the process
#                     my_data = event.sourceAddress
#         """
#         # Or:
#         """
#             event = Cef(listen=('TCP', 514))
#             with event.listen() as incoming_event:
#                 my_data = event.sourceAddress
#
#         """
#         # Or: # Favorite! Better example ->
#         """
#             event = Cef()
#             event.clear() # Reset all values
#             event.save() # Save current cleared state. Restoring it will now just clear it.
#
#             with event:
#                 while has_events:
#                     event.parse(...) # Automatically super().clear()
#                     my_data = event.sourceAddress
#                     <Do something with or to 'event'>
#         """
#         # Or: # Favorite! Lesser example -> both event.__exit__ and event.parse() call the super().clear(),
#         #   however if any input is assigned, can be easily forwarded.
#         """
#             event = Cef()
#             event.clear() # Reset all values
#             event.save() # Save current cleared state. Restoring it will now just clear it.
#
#             while has_events:
#                 with event:
#                     event.parse(...)
#                     my_data = event.sourceAddress
#         """
#         # Or: # Favorite! Lesser example -> both event.__exit__ and event.parse() call the super().clear(),
#         # however if input is assigned, can be forwarded.
#         """
#             event = Cef()
#
#             # Prep for parsing efficiently
#             event.clear() # Reset all values
#             event.save() # Save current cleared state. Restoring it will now just clear it.
#
#             with Cef(tcp=('172.16.106.3', 9514)) as event:
#
#                 while has_events:
#
#                     # On every iteration, an event is processed and then forward on __exit__
#                     with event:
#                         event.parse(...)
#                         my_data = event.sourceAddress
#                         event.sourceAddress = <Optional calculation and rrealignment
#
#
#         """
