from app.config import Config
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from app.models import db
from app import views
from app import factory
import app

API_ROOT = '/api/v1/'

app = factory.create_app(app_name=__name__, celery=app.celery)

app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

app.add_url_rule(API_ROOT + 'users/', view_func=views.UsersView.as_view('users_get'),
                 methods=['GET', ], defaults={'user_id': None})
app.add_url_rule(API_ROOT + 'users/<int:user_id>', view_func=views.UsersView.as_view('user_get'), methods=['GET', ])
app.add_url_rule(API_ROOT + 'users/', view_func=views.UsersView.as_view('users_post'), methods=['POST', ])

app.add_url_rule(API_ROOT + 'ads/', view_func=views.AdsView.as_view('ads_get'), methods=['GET', ])
app.add_url_rule(API_ROOT + 'ads/', view_func=views.AdsView.as_view('ads_post'), methods=['POST', ])
app.add_url_rule(API_ROOT + 'ads/<int:ad_id>', view_func=views.AdsView.as_view('ads_patch'), methods=['PATCH', ])
app.add_url_rule(API_ROOT + 'ads/<int:ad_id>', view_func=views.AdsView.as_view('ads_delete'), methods=['DELETE', ])

app.add_url_rule(API_ROOT + 'sendmail/', view_func=views.SendmailView.as_view('sendmail_post'),
                 methods=['POST', ])
app.add_url_rule(API_ROOT + 'sendmail/<string:task_id>', view_func=views.SendmailView.as_view('sendmail_get'),
                 methods=['GET', ])


if __name__ == '__main__':
    app.run(host='0.0.0.0')
