from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource
from flask import request

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)

class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    present = db.Column(db.Boolean, default=False)

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)

class UserResource(Resource):
    def get(self):
        users = User.query.all()
        return [{'id': user.id, 'username': user.username, 'role': user.role} for user in users]

    def post(self):
        data = request.get_json()
        new_user = User(username=data['username'], role=data['role'])
        db.session.add(new_user)
        db.session.commit()
        return {'id': new_user.id}, 201

class ClassroomResource(Resource):
    def get(self):
        classrooms = Classroom.query.all()
        return [{'id': classroom.id, 'name': classroom.name} for classroom in classrooms]

    def post(self):
        data = request.get_json()
        new_classroom = Classroom(name=data['name'])
        db.session.add(new_classroom)
        db.session.commit()
        return {'id': new_classroom.id}, 201

class AttendanceResource(Resource):
    def get(self):
        attendance_records = Attendance.query.all()
        return [{'id': record.id, 'user_id': record.user_id, 'classroom_id': record.classroom_id, 'date': str(record.date), 'present': record.present} for record in attendance_records]

    def post(self):
        data = request.get_json()
        new_attendance = Attendance(user_id=data['user_id'], classroom_id=data['classroom_id'], date=data['date'], present=data['present'])
        db.session.add(new_attendance)
        db.session.commit()
        return {'id': new_attendance.id}, 201

class ContentResource(Resource):
    def get(self):
        contents = Content.query.all()
        return [{'id': content.id, 'title': content.title, 'body': content.body, 'classroom_id': content.classroom_id} for content in contents]

    def post(self):
        data = request.get_json()
        new_content = Content(title=data['title'], body=data['body'], classroom_id=data['classroom_id'])
        db.session.add(new_content)
        db.session.commit()
        return {'id': new_content.id}, 201
