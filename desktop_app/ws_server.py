import asyncio
import json
from websockets import serve
from threading import Thread

class WsServer:
    def __init__(self, host='127.0.0.1', port=6789, app=None):
        self.host = host
        self.port = port
        self.app = app
        self._server = None
        self._clients = set()
        self._loop = None
        self._thread = None
        self._running = False

    async def _handler(self, websocket, path):
        self._clients.add(websocket)
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                except Exception:
                    await websocket.send(json.dumps({'error': 'invalid json'}))
                    continue
                # Простая команда get_selected
                cmd = data.get('cmd')
                if cmd == 'get_selected':
                    info = None
                    if self.app:
                        btn = self.app.get_last_selected_button()
                        if btn:
                            info = {
                                'id': getattr(btn, 'button_id', None),
                                'hue': btn.hue,
                                'grid_x': btn.grid_x,
                                'grid_y': btn.grid_y,
                                'grid_w': btn.grid_w,
                                'grid_h': btn.grid_h,
                                'emoji': getattr(btn, 'emoji', None)
                            }
                    await websocket.send(json.dumps({'cmd': 'get_selected', 'data': info}))
                else:
                    await websocket.send(json.dumps({'error': 'unknown cmd'}))
        finally:
            self._clients.remove(websocket)

    async def _start_async(self):
        async with serve(self._handler, self.host, self.port):
            self._running = True
            await asyncio.Future()  # run forever

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        def thread_target():
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            try:
                self._loop.run_until_complete(self._start_async())
            finally:
                self._loop.run_until_complete(self._loop.shutdown_asyncgens())
                self._loop.close()
        self._thread = Thread(target=thread_target, daemon=True)
        self._thread.start()

    def stop(self):
        if not self._loop:
            return
        self._loop.call_soon_threadsafe(self._loop.stop)
        self._running = False
        if self._thread:
            self._thread.join(timeout=1)

    def send_to_all(self, message: dict):
        if not self._clients or not self._loop:
            return
        payload = json.dumps(message)
        async def _send_all():
            for c in list(self._clients):
                try:
                    await c.send(payload)
                except Exception:
                    pass
        asyncio.run_coroutine_threadsafe(_send_all(), self._loop)
