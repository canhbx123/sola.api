import logging

from flask import Flask
from flask_cors import CORS
from common.config import WEB_CONFIG
from views.api.company_attachment_view import CompanyAttachmentView
from views.api.dependent_view import DependentView
from views.api.holiday_view import HolidayView
from views.api.jobtitle_view import JobTitleView
from views.api.user_view import UserView
from views.api.department_view import DepartmentView
from views.api.role_view import RoleView
from views.api.company_view import CompanyView
from views.api.relationship_view import RelationshipView
from views.api.job_view import JobView
from views.api.attendance_view import AttendanceView
from views.api.notification_view import NotificationView
from views.api.expense_view import ExpenseView
from setting import cache
import time

from views.api.workday_view import WorkDayView

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config.update(WEB_CONFIG)
cache.init_app(app)

UserView.register(app, route_base='/api/user')
DepartmentView.register(app, route_base='/api/department')
RoleView.register(app, route_base='/api/role')
CompanyView.register(app, route_base='/api/company')
CompanyAttachmentView.register(app, route_base='/api/company/attachment')
RelationshipView.register(app, route_base='/api/relationship')
JobView.register(app, route_base='/api/job')
JobTitleView.register(app, route_base='/api/jobtitle')
DependentView.register(app, route_base='/api/dependent')
AttendanceView.register(app, route_base='/api/attendance')
NotificationView.register(app, route_base='/api/notification')
HolidayView.register(app, route_base='/api/holiday')
WorkDayView.register(app, route_base='/api/workdays')
ExpenseView.register(app, route_base='/api/expense')

file_handler = logging.FileHandler('web.log')
file_handler.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)

if __name__ == '__main__':
    app.run()
