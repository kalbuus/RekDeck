import asyncio
import json
import queue
from websockets import serve
from threading import Thread

from deck_area import CONFIG_PATH

class WsServer:
    def __init__(self, host="0.0.0.0", port=8765, app=None):
        self.host = host
        self.port = port
        self.app = app
        self._server = None
        self._clients = set()
        self._loop = None
        self._thread = None
        self._running = False
        self.event_queue = queue.Queue()

    async def _handler(self, websocket, path):
        self._clients.add(websocket)
        try:
            try:
                with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                    area_state_cmd = {'cmd': 'area_state', 'data': json.load(f)}
            except:
                area_state_cmd = {'cmd': 'area_state', 'data': {}}
            await websocket.send(json.dumps(area_state_cmd))
            async for message in websocket:
                try:
                    data = json.loads(message)
                except Exception:
                    await websocket.send(json.dumps({'error': 'invalid json'}))
                    continue
                cmd = data.get('cmd')
                
        finally:
            self._clients.remove(websocket)
    
    async def broadcast(self):
        while True:
            if not self.event_queue.empty():
                event = self.event_queue.get()
                for ws in self._clients.copy():
                    try:
                        await ws.send(event)
                    except:
                        self._clients.remove(ws)
            await asyncio.sleep(0.1)

    async def _start_async(self):
        async with serve(self._handler, self.host, self.port):
            self._running = True
            await self.broadcast()

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
