from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    
    @staticmethod
    def create_table():
        db.create_all()
        return "Tables created"
    
    @staticmethod
    def get_users():
        return Users.query.all()
    
    def create_user(self):
        db.session.add(self)
        db.session.commit()
    
    def edit_user(self):
        db.session.commit()
        
    def delete_user(self):
        db.session.delete(self)
        db.session.commit()
        
    def __repr__(self):
        return f"<User {self.name}>"
