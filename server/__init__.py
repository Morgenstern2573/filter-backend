import flask
import json
from . import db
from flask import Flask, request


def create_app():
    app = Flask(__name__)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin',
                             'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        #response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    @app.route('/', methods=("GET",))
    def index():
        dbc = db.get_db()
        courses = request.args.get('course_list')
        if courses is not None:
            courses = courses.split(",")
            courses.remove("")
            course_data = []
            courses_not_found = []
            for course in courses:
                value = dbc.execute(
                    'SELECT * FROM timetable WHERE course_code = ?', (course,)).fetchone()
                if value is not None:
                    course_data.append(value)
                else:
                    courses_not_found.append(course)
            code_list = []
            times = []
            for item in course_data:
                code_list.append(item['course_code'])
                times.append(json.loads(item['loctime']))
            return json.dumps({'status': 'ok', 'codes': code_list, 'times': times, 'not_found': courses_not_found})
        else:
            return json.dumps({'status': 'error', 'message': 'no courses provided'})
    app.teardown_appcontext(db.close_db)
    return app
