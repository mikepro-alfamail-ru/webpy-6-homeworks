from flask.views import MethodView
from flask import jsonify, request
import bcrypt
from app.models import Users, db
from app.config import SALT


class UsersView(MethodView):

    def get(self, user_id=None):
        if user_id is not None:
            user = Users.query.get(user_id)
            if not user:
                response = jsonify(
                    {
                        'error': 'User not found'
                    }
                )
                response.status_code = 404
                return response
            return jsonify(
                {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email
                }
            )
        else:
            users = []
            for user in Users.query.all():
                users.append(
                    {
                        'id': user.id,
                        'name': user.name,
                        'email': user.email
                    }
                )
            return jsonify({'users': users})

    def post(self):
        user = Users(**request.json)
        db.session.add(user)
        db.session.commit()
        return jsonify(
            {
                'status': 'created',
                'id': user.id
            }
        )
