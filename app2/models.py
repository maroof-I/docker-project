from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=True)

    @staticmethod
    def get_tasks():
        return Tasks.query.all()

    def create_task(self):
        db.session.add(self)
        db.session.commit()