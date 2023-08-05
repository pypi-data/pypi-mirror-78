from ..parser import AGIPayloadParser


class AMIMessage(dict):
    """Handle both Responses and Events with the same api:

    ..
        >>> resp = AMIMessage({'Response': 'Follows'}, 'Response body')
        >>> event = AMIMessage({'Event': 'MeetmeEnd', 'Meetme': '4242'})

    Responses:

    .. code-block:: python

        >>> bool(resp.success)
        True
        >>> resp
        <Message Response='Follows' body='Response body'>
        >>> print(resp.body)
        Response body
        >>> for line in resp.iter_lines():
        ...     print(line)
        Response body

    Events:

    .. code-block:: python

        >>> print(event['Meetme'])
        4242

    """

    success_responses = ['Success', 'Follows', 'Goodbye']

    def __init__(self, *args, body, **kwargs):
        self.body = body
        super(AMIMessage, self).__init__(*args, **kwargs)

    def __repr__(self):
        message = ' '.join(['%s=%r' % i for i in sorted(self.items())])
        return f'<AMIMessage {message}, body={len(self.body)}>'

    @property
    def action_id(self):
        return self.get('ActionID')

    @property
    def success(self):
        """return True if a response status is Success or Follows:

        .. code-block:: python

            >>> resp = AMIMessage({'Response': 'Success'})
            >>> print(resp.success)
            True
            >>> resp['Response'] = 'Failed'
            >>> resp.success
            False
        """
        if 'Event' in self:
            return True
        if self['Response'] in self.success_responses:
            return True
        return False

    def iter_lines(self):
        """Iter over response body"""
        for line in self.body.split('\n'):
            yield line

    def agi_result(self):
        """Get parsed result of AGI command"""
        if 'Result' in self:
            return AGIPayloadParser.parse_message(self['Result'].encode().split(b'\n'))[1]
        else:
            raise ValueError('No result in %r' % self)

    def get_dict(self, key, sep='='):
        """Convert a multi values header to a case-insensitive dict:

        .. code-block:: python

            >>> resp = AMIMessage({
            ...     'Response': 'Success',
            ...     'ChanVariable': [
            ...         'FROM_DID=', 'SIPURI=sip:42@10.10.10.1:4242'],
            ... })
            >>> print(resp['ChanVariable'])
            ['FROM_DID=', 'SIPURI=sip:42@10.10.10.1:4242']
            >>> value = resp.get_dict('ChanVariable')
            >>> print(value['SIPURI'])
            sip:42@10.10.10.1:4242
        """
        values = self.get(key, None)
        if not isinstance(values, list):
            raise TypeError("{0} must be a list. got {1}".format(key, values))

        result = {}
        for item in values:
            if sep not in item:
                continue
            k, v = item.split(sep, 1)
            result[k.strip()] = v.strip()
        return result
