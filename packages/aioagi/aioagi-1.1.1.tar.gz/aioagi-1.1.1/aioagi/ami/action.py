import asyncio

from . import utils


class AMIAction(dict):
    """Dict like object to handle actions.
    Generate action IDs for you:

    ..
        >>> utils.IdGenerator.reset('myuuid')

    .. code-block:: python

        >>> action = AMIAction({'Action': 'Status'})
        >>> print(action) # doctest: +NORMALIZE_WHITESPACE
        Action: Status
        ActionID: action/myuuid/1/1

        >>> action = AMIAction({'Action': 'SIPnotify',
        ...                  'Variable': ['1', '2']})
        >>> print(action) # doctest: +NORMALIZE_WHITESPACE
        Action: SIPnotify
        ActionID: action/myuuid/1/2
        Variable: 1
        Variable: 2
    """
    EOL = '\r\n'
    action_id_generator = utils.IdGenerator('action')

    def __init__(self, *args, as_list=False, **kwargs):
        self.as_list = as_list
        super(AMIAction, self).__init__(*args, **kwargs)

        if 'ActionID' not in self:
            self['ActionID'] = self.action_id_generator()

        self.responses = []
        self.future = asyncio.Future()

    def __str__(self):
        action = []
        for k, v in sorted(self.items()):
            if isinstance(v, (list, tuple)):
                action.extend(['%s: %s' % (k, i) for i in v])
            else:
                action.append('%s: %s' % (k, v))
        action.append(self.EOL)
        return self.EOL.join(action)

    @property
    def id(self):
        return self['ActionID']

    def as_message(self, encoding='ascii'):
        return str(self).encode(encoding)

    @property
    def multi(self):
        resp = self.responses[0]
        msg = resp.get('Message', '').lower()
        if resp.get('SubEvent') == 'Start':
            return True
        elif resp.get('EventList') == 'start':
            return True
        elif 'will follow' in msg:
            return True
        elif msg == 'added interface to queue':
            return False
        elif msg.startswith('added') and msg.endswith('to queue'):
            return True
        elif msg == 'originate successfully queued':
            return False
        elif msg.endswith('successfully queued') and getattr(self, 'async') != 'false':
            return True
        elif self.as_list:
            return True
        return False

    @property
    def completed(self):
        resp = self.responses[-1]
        if resp.get('Event', '').endswith('Complete'):
            return True
        elif resp.get('SubEvent') in ('End', 'Exec'):
            return True
        elif resp.get('Response') in ('Success', 'Error', 'Fail', 'Failure'):
            return True
        elif not self.multi:
            return True
        return False

    def add_message(self, message):
        self.responses.append(message)
        multi = self.multi
        if self.completed and not self.future.done():
            if multi and len(self.responses) > 1:
                self.future.set_result(self.responses)
            elif not multi:
                self.future.set_result(self.responses[0])
            else:
                return False
            return True
