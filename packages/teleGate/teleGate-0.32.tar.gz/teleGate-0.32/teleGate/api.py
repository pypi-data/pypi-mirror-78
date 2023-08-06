import inspect
import traceback
from urllib.parse import unquote_plus
from io import BytesIO

from aiohttp import web

from consts import LVL2MSG, LVL_ALIAS

"""
http://localhost:35001/api_v1/log/test1/4/msg%20msg

http://localhost:35001/index.html
fetch('http://localhost:35001/api_v1/log/test1/1', {
   method: 'POST',
   body: 'some test msg'
}).then(response=>response.text()).then(console.log);
"""


class ApiV1:

    def __init__(self, tg_client, subscribers, app=None, client_max_size=1024**2):
        self._app = app or web.Application(debug=False, client_max_size=client_max_size)
        self._tg_client = tg_client
        self._subscribers = subscribers
        self._prep_route_map()

    def _prep_route_map(self):
        self._route_map = {
            'index': ('get', 'index.html', lambda *_, **__: 'Fuck u, world!'),
            'log_post': ('post', 'api_v1/log/{project}/{lvl}', self.cb_log),
            'log_get': ('get', 'api_v1/log/{project}/{lvl}/{data}', self.cb_log),
            'file_post': ('post', 'api_v1/file/{username}', self.cb_file)
        }

    async def _handler(self, request):
        _, _, cb = self._route_map[request.match_info.route.name]
        params = dict(request.match_info)
        data = params.pop('data', None)
        if request.content_type == 'multipart/form-data':
            post = await request.post()
            data = data or post.get('data')
            file_obj = post.get('file')
            if file_obj is not None:
                params['file'] = BytesIOWithName(file_obj.filename, file_obj.file.read())
        else:
            if request.body_exists:
                data = data or unquote_plus(await request.text())

        # print(f'Requested {request.match_info.route.name}[{cb}] with args {params}')
        try:
            res = ''
            if inspect.iscoroutinefunction(cb):
                res = await cb(data=data, **params)
            elif callable(cb):
                res = cb(data=data, **params)
            return web.Response(status=200, content_type='text/html', text=res or '')
        except Exception:
            return web.Response(status=500, content_type='text/html', text=traceback.format_exc())

    def _make_msg(self, project, lvl, data):
        msg = (
            f'{LVL2MSG[lvl]} `[{project}]`',
            data,
        )
        return '\n'.join(msg)

    async def cb_log(self, project, lvl, data):
        try:
            assert isinstance(project, str) and project
            assert isinstance(lvl, (str, int)) and lvl
            if not isinstance(lvl, int):
                lvl = LVL_ALIAS[lvl.lower()]
            assert isinstance(data, str) and data
            send_to = await self._subscribers.check_pub(project, lvl)
            # print(f'New msg [{project}:{lvl}] for {send_to}')
            if not send_to: return
            is_silent = lvl == 4  # ? hard-coded
            msg = self._make_msg(project, lvl, data)
            for sid in send_to:
                o = await self._tg_client.get_entity(sid)
                await self._tg_client.send_message(o, msg, silent=is_silent)
        except Exception:
            print(
                f'{"-" * 30}\nCant process api-request.\nProject: {project}\nLevel: {lvl}\n{data}\n{traceback.format_exc()}{"-" * 30}')
            raise

    async def cb_file(self, username, data, file=None):
        try:
            assert isinstance(username, (str, int)) and username
            assert isinstance(data, str) and data
            if isinstance(username, int):
                username = str(username)
            o = await self._tg_client.get_entity(username)
            await self._tg_client.send_message(o, data, file=file, silent=True)
        except Exception:
            print(
                f'{"-" * 30}\nCant process api-request.\nFile sending for: {username}\n\n{data}\n{traceback.format_exc()}{"-" * 30}')
            raise

    def _prep_routing(self):
        for name, (method, path, _) in self._route_map.items():
            if not path.startswith('/'): path = '/' + path
            yield web.route(method, path, self._handler, name=name)

    def init(self):
        self._app.add_routes(self._prep_routing())
        return self._app.make_handler()


class BytesIOWithName(BytesIO):

    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
