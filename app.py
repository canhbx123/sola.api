from flask import Flask
from flask_cors import CORS
from common.config import WEB_CONFIG
from views.api.user_view import UserView
from views.api.department_view import DepartmentView
from views.api.role_view import RoleView
from views.api.company_view import CompanyView
from views.api.relationship_view import RelationshipView
from views.api.job_view import JobView
from views.api.time_recort_view import TimeRecordView
from setting import cache
import time

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config.update(WEB_CONFIG)
cache.init_app(app)

UserView.register(app, route_base='/api/user')
DepartmentView.register(app, route_base='/api/department')
RoleView.register(app, route_base='/api/role')
CompanyView.register(app, route_base='/api/company')
RelationshipView.register(app, route_base='/api/relationship')
JobView.register(app, route_base='/api/job')
TimeRecordView.register(app, route_base='/api/time-record')


@app.route('/')
def index():
    time.sleep(10)
    return ''


@app.route('/rq2')
def rq2():
    return 'rq2'


if __name__ == '__main__':
    app.run()
