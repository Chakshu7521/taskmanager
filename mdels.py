from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Column, Integer, String



db = SQLAlchemy()

class User(db.Model):

    __tablename__ = "userdata"

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)

    username = db.Column(db.String(50), unique=True,nullable=False)

    password = db.Column(db.String(80))



    def __init__(self, username,password):

        self.username = username

        self.password = password







class tasks(db.Model):

    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)

    user_id = db.Column(db.Integer)

    taskname = db.Column(db.String(50), unique=True,nullable=False)

    discription = db.Column(db.String(50), unique=True,nullable=False)

    status = db.Column(db.String(50))





    def __init__(self,user_id, taskname,discription,status):

        self.user_id = user_id

        self.taskname = taskname

        self.discription = discription

        self.status = status



    

