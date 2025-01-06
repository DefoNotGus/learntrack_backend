from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from models import db, UserResource, ClassroomResource, AttendanceResource, ContentResource

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

# Create the API
api = Api(app)

# Add resources
api.add_resource(UserResource, '/api/users')
api.add_resource(ClassroomResource, '/api/classrooms')
api.add_resource(AttendanceResource, '/api/attendance')
api.add_resource(ContentResource, '/api/content')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)
