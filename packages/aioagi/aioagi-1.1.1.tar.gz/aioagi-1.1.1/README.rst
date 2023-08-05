Aioagi
======

Async agi client/server framework.
The project based on "aiohttp" framework.

Key Features
============

- Supports both client and server side of AGI protocol.
- AGI-server has middlewares and pluggable routing.

Getting started
===============


Server
------

Simple AGI server:

.. code-block:: python

    import asyncio

    from aiohttp.web import Application, AppRunner, TCPSite, Response

    from aioagi import runner
    from aioagi.app import AGIApplication
    from aioagi.log import agi_server_logger
    from aioagi.urldispathcer import AGIView
    from aiohttp.web_runner import GracefulExit


    async def hello(request):
        message = await request.agi.stream_file('hello-world')
        await request.agi.verbose('Hello handler: {}.'.format(request.rel_url.query))
        agi_server_logger.debug(message)


    async def http_hello(request):
        return Response(text="Hello, world")


    class HelloView(AGIView):
        async def sip(self):
            message = await self.request.agi.stream_file('hello-world')
            await self.request.agi.verbose('HelloView handler: {}.'.format(self.request.rel_url.query))
            agi_server_logger.debug(message)


    if __name__ == '__main__':
        app = AGIApplication()
        app.router.add_route('SIP', '/', hello)
        runner.run_app(app)

    # OR
    if __name__ == '__main__':
        apps = []

        app = AGIApplication()
        app.router.add_route('SIP', '/', hello)

        http_app = Application()
        http_app.router.add_route('GET', '/', http_hello)

        loop = asyncio.get_event_loop()

        runners = []
        sites = []
        for _app in [app, http_app]:
            app_runner = AppRunner(_app)
            loop.run_until_complete(app_runner.setup())
            if isinstance(_app, AGIApplication):
                sites.append(runner.AGISite(app_runner, port=8081))
            else:
                sites.append(TCPSite(app_runner, port=8080))

            runners.append(app_runner)

        for site in sites:
            loop.run_until_complete(site.start())

        uris = sorted(str(s.name) for runner in runners for s in runner.sites)
        print("======== Running on {} ========\n"
              "(Press CTRL+C to quit)".format(', '.join(uris)))

        try:
            loop.run_forever()
        except (GracefulExit, KeyboardInterrupt):  # pragma: no cover
            pass

        finally:
            for runner in reversed(runners):
                loop.run_until_complete(runner.cleanup())

        if hasattr(loop, 'shutdown_asyncgens'):
            loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()


Client
------

To set AGI connection as Asterisk:

.. code-block:: python

    import asyncio
    import logging.config

    from aioagi.log import agi_client_logger
    from aioagi.client import AGIClientSession
    from aioagi.parser import AGIMessage, AGICode


    async def test_request(loop):
        headers = {
            'agi_channel': 'SIP/100-00000001',
            'agi_language': 'ru',
            'agi_uniqueid': '1532375920.8',
            'agi_version': '14.0.1',
            'agi_callerid': '100',
            'agi_calleridname': 'test',
            'agi_callingpres': '0',
            'agi_callingani2': '0',
            'agi_callington': '0',
            'agi_callingtns': '0',
            'agi_dnid': '101',
            'agi_rdnis': 'unknown',
            'agi_context': 'from-internal',
            'agi_extension': '101',
            'agi_priority': '1',
            'agi_enhanced': '0.0',
            'agi_accountcode': '',
            'agi_threadid': '139689736754944',
        }
        async with AGIClientSession(headers=headers, loop=loop) as session:
            async with session.sip('agi://localhost:8080/hello/?a=test1&b=var1') as response:
                async for message in response:
                    client_logger.debug(message)
                    await response.send(AGIMessage(AGICode.OK, '0', {}))

            async with session.sip('agi://localhost:8080/hello-view/?a=test2&b=var2') as response:
                async for message in response:
                    client_logger.debug(message)
                    await response.send(AGIMessage(AGICode.OK, '0', {}))

.. note:: Session request headers are set automatically for ``session.sip('agi://localhost:8080/hello/?a=test1&b=var1')`` request:

.. code-block:: bash

    agi_type: SIP
    agi_network: yes
    agi_network_script: hello/
    agi_request: agi://localhost:8080/hello/


AMI
---

.. code-block:: python

    import asyncio

    from aioagi.ami.action import AMIAction
    from aioagi.ami.manager import AMIManager


    async def callback(manager, message):
        print(message)


    async def main(app):
        manager = AMIManager(
            app=app, title='myasterisk',
            host='127.0.0.1',
            port=5038,
            username='username',
            secret='secret',
        )
        manager.register_event('*', callback)
        app['manager'] = manager
        await manager.connect()

        await asyncio.sleep(2)

        message = await manager.send_action(AMIAction({
            'Action': 'Command',
            'Command': 'database show',
        }))
        print(message)
        print(message.body)


    async def cleanup(app):
        app['manager'].close()


    if __name__ == '__main__':
        app = {}
        _loop = asyncio.get_event_loop()
        try:
            _loop.run_until_complete(main(app))
        except KeyboardInterrupt:
            _loop.run_until_complete(cleanup(app))
            _loop.close()


Install
=======

``pip install aioagi``


Thanks
======
* Gael Pasgrimaud - panoramisk_

.. _panoramisk: https://github.com/gawel/panoramisk
