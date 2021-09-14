from aiohttp import web
from db import db_context
from views import UserView

app = web.Application()
app.router.add_routes([web.post('/user', UserView), web.get('/user/{user_id}', UserView), ])
app.cleanup_ctx.append(db_context)

web.run_app(app)