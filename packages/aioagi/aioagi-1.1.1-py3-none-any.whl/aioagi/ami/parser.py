from typing import List
from urllib.parse import unquote

from aioagi.ami.message import AMIMessage


class AMIMessageParser:
    sep = b'\r\n\r\n'
    eol = '\r\n'
    has_body = ('Response: Follows', 'Response: Fail')
    quoted_keys = ['result']
    success_responses = ['Success', 'Follows', 'Goodbye']

    def __init__(self, encoding):
        self.encoding = encoding

        self._tail = b''
        self._sep_len = len(self.sep)

    def feed_data(self, data) -> List[AMIMessage]:
        messages = []
        if self._tail:
            data, self._tail = self._tail + data, b''

        data_len = len(data)
        start_pos = 0

        while start_pos < data_len:
            pos = data.find(self.sep, start_pos)
            if pos >= start_pos:
                # line found
                try:
                    messages.append(self.parse_message(data[start_pos:pos]))
                finally:
                    start_pos = pos + self._sep_len

            else:
                self._tail = data[start_pos:]
                break

        return messages

    def parse_message(self, data: bytearray):
        data = data.decode(self.encoding)
        lines = data.split(self.eol)

        headers = {}
        body = ''
        if lines[0].startswith(self.has_body):
            body = lines.pop()
            while not body and lines:
                body = lines.pop()

        for line in lines:
            if ': ' not in line:
                continue

            key, value = line.split(': ', 1)
            value = value.strip()
            if key.lower() in self.quoted_keys:
                value = unquote(value)

            if key in headers:
                if not isinstance(headers[key], list):
                    headers[key] = [headers[key]]

                headers[key].append(value)
            else:
                headers[key] = value

        return AMIMessage(headers, body=body)
