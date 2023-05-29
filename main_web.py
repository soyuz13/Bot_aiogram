from aiohttp.web import run_app, Response, get
from aiohttp.web_app import Application


async def hello(request):
    return Response(text="Hello, world")

app = Application()
app.add_routes([get('/', hello)])

run_app(app, host='176.124.192.33', port=88)