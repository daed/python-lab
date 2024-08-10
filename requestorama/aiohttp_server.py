import asyncio
from aiohttp import web

async def handle(request):
    return web.Response(text="Hello, world")

try:
    PORT = 8081
    app = web.Application()
    app.router.add_get('/', handle)
    print("aiohttp server start")
    web.run_app(app, port=PORT)
except OSError:
    print("cannot start server, will attempt to continue")
