import asyncio

from .action import AMIAction
from .message import AMIMessage
from .parser import AMIMessageParser
from ..log import agi_ami_logger


class AMIProtocol(asyncio.Protocol):
    encoding = 'ascii'

    def __init__(self, manager):
        self.manager = manager
        self.responses = {}
        self._message_parser = AMIMessageParser(self.encoding)

        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def connection_lost(self, exc):
        self.manager.connection_lost(exc)

    def data_received(self, data):
        messages = self._message_parser.feed_data(data)
        if not messages:
            return

        for message in messages:
            self.handle_message(message)

    def handle_message(self, message: AMIMessage):
        response = self.responses.get(message.action_id)

        if response is not None:
            if response.add_message(message):
                # completed; dequeue
                self.responses.pop(response.id)

        elif 'Event' in message:
            self.manager.dispatch(message)

    def send(self, action: AMIAction):
        self.responses[action.id] = action

        try:
            self.transport.write(action.as_message(self.encoding))
        except Exception:  # pragma: no cover
            agi_ami_logger.exception('Fail to send %r' % action)
        return action.future
