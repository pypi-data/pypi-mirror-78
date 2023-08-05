import importlib
import os
from textwrap import dedent
import sys
import types

from aeval import aeval
import jedi
import lsp
import trio


def main():
    trio.run(run)


async def run():
    await trio.serve_tcp(_handler, 6768)


async def _handler(stream: trio.SocketStream):
    print('connected')
    try:
        conn = lsp.Connection('server')
        recvsize = 4096

        while True:
            while True:
                event = conn.next_event()

                if event is lsp.NEED_DATA:
                    data = await stream.receive_some(recvsize)
                    if not data:
                        return
                    conn.receive(data)
                elif isinstance(event, lsp.RequestReceived):
                    ...
                elif isinstance(event, lsp.DataReceived):
                    ...
                elif isinstance(event, lsp.MessageEnd):
                    break

            _, body = conn.get_received_data()
            method = body.get('method', None)
            if method == 'initialize':
                send_data = conn.send_json(dict(
                    id=body['id'],
                    result=dict(capabilities=dict()),
                ))
                await stream.send_all(send_data)
            elif method == 'lyre/eval':
                import sys

                p = body['params']['path']
                proj = jedi.get_default_project(p)
                script = jedi.Script(path=p)

                # FIXME: This is gross and dangerous.
                if not proj.path in sys.path:
                    sys.path.insert(0, proj.path)

                # mod = importlib.import_module(script.get_context().module_name)

                modname = script.get_context().module_name
                mod = sys.modules.get(modname, None)
                if mod is None:
                    mod = sys.modules[modname] = types.ModuleType(
                        modname, 'Synthetic module created by Lyre')
                    mod.__file__ = p
                    # mod.__path__ = os.path.dirname(p)

                # FIXME: Need to source map back to the indented version for
                #        exceptions.
                code = dedent(body['params']['code'])

                response = dict(
                    id=body['id'],
                )
                try:
                    value = await aeval(code, mod.__dict__, None)
                    response['result'] = dict(value=repr(value))
                except BaseException as ex:
                    import traceback
                    traceback.print_exc()
                    response['result'] = dict(
                        error=str(ex),
                        stack=traceback.format_stack(),
                    )

                send_data = conn.send_json(response)
                await stream.send_all(send_data)

            conn.go_next_circle()
    finally:
        print('disconnected')
