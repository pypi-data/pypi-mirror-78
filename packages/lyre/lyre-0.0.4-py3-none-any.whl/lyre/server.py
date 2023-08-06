import argparse
import importlib
from pathlib import Path
from textwrap import dedent
import traceback
import sys
import types

from aeval import aeval
import lsp
import trio


_ROOT_MARKER_FILES = [
    'pyproject.toml',
    'setup.py',
    'requirements.txt',
    'MANIFEST.in',
    '.git',
    '.hg',
]


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('-p', '--port', default=6768, type=int)
    args = parser.parse_args()

    trio.run(run, args.port)


async def run(port=6768):
    await trio.serve_tcp(_handler, port)


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
                modname = _module_name_from_filename(Path(p))

                try:
                    mod = importlib.import_module(modname)
                except Exception:
                    mod = sys.modules[modname] = types.ModuleType(
                        modname, 'Synthetic module created by Lyre')
                    mod.__file__ = p

                # FIXME: Need to source map back to the indented version for
                #        exceptions.
                code = dedent(body['params']['code'])

                response = dict(id=body['id'])
                try:
                    value = await aeval(code, mod.__dict__, None)
                    response['result'] = dict(status='ok', value=repr(value))
                except BaseException as ex:
                    etype, ex, tb = sys.exc_info()
                    fmt_exc = traceback.format_exception_only(etype, ex)
                    fmt_tb = traceback.format_tb(tb)

                    response['result'] = dict(
                        status='error',
                        error=fmt_exc[-1],
                        fullError=fmt_exc,
                        traceback=fmt_tb,
                    )

                send_data = conn.send_json(response)
                await stream.send_all(send_data)

            conn.go_next_circle()
    finally:
        print('disconnected')


def _module_name_from_filename(path: Path):
    if path.name == '__init__.py':
        path = path.parent

    for import_path in _candidate_import_paths(path):
        try:
            relpath = path.relative_to(import_path)
        except ValueError:
            continue

        if not relpath.parts:
            continue

        parts = list(relpath.parts)
        parts[-1] = relpath.stem
        return '.'.join(parts)

    # FIXME: Need a custom exception (or a better standard one).
    raise Exception(f'cannot determine module name: {path}')


def _candidate_import_paths(path: Path):
    yield from (Path(path) for path in sys.path)
    project_path = _guess_project_path(path)
    if project_path is not None:
        yield project_path


def _guess_project_path(path: Path):
    for dir_ in path.parents:
        for marker in _ROOT_MARKER_FILES:
            if dir_.joinpath(marker).exists:
                return dir_

    return None
