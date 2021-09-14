from aiohttp import web
from db import Users, Ads
import aiohttp_sqlalchemy as ahsa
from sqlalchemy import select, insert


class UserView(web.View, ahsa.SAMixin):
    async def get(self):
        user_id = self.request.match_info['user_id']
        print(user_id)
        db_session = self.get_sa_session()
        # async with db_session.begin() as conn:
        if user_id is not None:
            user = await db_session.execute(select(Users).where(Users.id == int(user_id)))
            user = user.fetchone()
            if not user:
                response = (
                    {
                        'error': 'User not found'
                    }
                )
                return web.json_response(response)
            user = user[0]
            return web.json_response(
                {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email
                }
            )
        else:
            users = []
            users_list = await db_session.execute(select(Users))
            for user in users_list.scalars():
                users.append(
                    {
                        'id': user.id,
                        'name': user.name,
                        'email': user.email
                    }
                )
            return web.json_response(users)

    async def post(self):
        db_session = self.get_sa_session()
        user_data = await self.request.json()
        print(user_data)
        new_user = Users(**user_data)
        db_session.add(new_user)
        await db_session.commit()
        await db_session.refresh(new_user)
        return web.json_response({
            'id': new_user.id,
            'name': new_user.name,
            'email': new_user.email
        })