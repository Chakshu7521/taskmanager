from flask import Flask,request,flash,redirect,current_app,jsonify

from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine

from models import tasks, db, User

from flask_jwt_extended import create_access_token

from flask_jwt_extended import get_jwt_identity

from flask_jwt_extended import jwt_required

from flask_jwt_extended import JWTManager





app = Flask(__name__)



app.config["JWT_SECRET_KEY"] = "secretsecret"  

jwt = JWTManager(app)





app.config['SQLALCHEMY_DATABASE_URI']  = 'sqlite:///user.db'

engine = create_engine('sqlite:///user.db')

db.init_app(app)

Session = sessionmaker(bind=engine)





@app.route('/')

def hello():

    return 'Hello, World!'



@app.route('/signup', methods=['POST'])

def signup():

    username = request.form.get('username')

    password = request.form.get("password")

    if not request.form['username'] or not request.form['password']:

        return "Please enter all the fields", 'error', 409

    else:

        userdata = User(username,password)

        db.session.add(userdata)

        db.session.commit()

        return "account created successfully"



@app.route('/login', methods=['POST'])

def login():

    username = request.form.get('username')

    password = request.form.get('password')

    detail = User.query.filter_by(username=username).first()

    if detail and detail.password == password :

        access_token =create_access_token(

            identity=username

        ) 

        return access_token, 200

    return redirect("http://127.0.0.1:5000/login")

        

    

@app.route('/addtasks',methods=['POST'])

@jwt_required()

def addtasks():

    current_user = get_jwt_identity()

    user_id = request.form.get('user_id')

    taskname = request.form.get('taskname')

    discription = request.form.get('discription')

    status = request.form.get('status')

    #user_tasks = User.query.filter_by(user_id=user_id).()

    if not request.form['user_id'] or not request.form['taskname']  or not request.form['discription'] or not request.form['status']:

         print("Please enter all the fields", 'error')

    else:

        taskdata = tasks(user_id,taskname,discription,status)

        db.session.add(taskdata)

        db.session.commit()

        return "done"

        #return f"task of the {username} is added"



@app.route('/alltasks',methods=['POST'])

@jwt_required()

def alltasks():

    current_user = get_jwt_identity()

    user_id = request.form.get('user_id')

    user_tasks = tasks.query.filter_by(user_id=user_id).all()

    tasks_list = []



    for task in user_tasks:

        task_dict = {

            'id': task.id,

            'taskname': task.taskname,

            'discription': task.discription,

            'status': task.status

        }

        tasks_list.append(task_dict)



    return jsonify(tasks_list)





@app.route('/Ustatus',methods=['POST'])

@jwt_required()

def Ustatus():

    current_user = get_jwt_identity()

    userid = request.form.get('user_id')

    taskname = request.form.get('taskname')

    status = request.form.get('status')

    detail = tasks.query.filter_by(user_id=userid).first()

    if detail.taskname == taskname:

        detail.status = status

        db.session.commit()

        return detail.status



@app.route('/delete',methods=['POST'])

@jwt_required()

def delete():

    

    user_id = request.form.get('user_id')

    taskname = request.form.get('taskname')

    detail = tasks.query.filter_by(user_id=user_id).first()

    if detail.taskname == taskname:

        db.session.delete(detail)

        db.session.commit()

        return "done"



if __name__ == '__main__':

    with app.app_context():

        db.create_all()

        app.run(debug=True)

        app.run()

