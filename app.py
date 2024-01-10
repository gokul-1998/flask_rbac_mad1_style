from celery.result import AsyncResult
import os
import hashlib
from flask import Flask, redirect, render_template,request, make_response, jsonify, send_file, url_for
from flask_security import SQLAlchemySessionUserDatastore, Security, login_user, logout_user
from flask_security import current_user, auth_required, login_required, roles_required, roles_accepted,hash_password,verify_password
from models import *
from apis import *
from config import Config
import time

from admin_create import admin_create_user

app = Flask(__name__)
api.init_app(app)
app.config.from_object(Config)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./model1.db"

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", 
                                          "hbivnfdisbvljobfgjoihfhrugubdfsbery89w34yt5898he")
app.config["SECURITY_PASSWORD_SALT"] = os.environ.get("SECURITY_PASSWORD_SALT",
                                                       "hbivnfdisbvljobfgjoihfhrugubdfsbery89w34yt5898he")

# authenticatin paramter for url
app.config["`SECURITY_TOKEN_AUTHENTICATION_KEY`"] = "auth_key" # Default: auth_token
# in postman add the key as auth_key and value as the token , this should be in the url
app.config["SECURITY_TOKEN_AUTHENTICATION_HEADER"] = "Authentication-Token" # Default: Authentication-Token"
# in postman add the key as Authentication-Token and value as the token
# app.config[]

db.init_app(app)

user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role) # Not SQLAlchemyUserDatastore
app.security = Security(app, user_datastore)
with app.app_context():
    db.create_all()

    if(db.session.query(Role).count()==0):
        app.security.datastore.create_role(name="admin")
        db.session.commit()
        admin_create_user()


# @app.route('/monthly-report')
# def monthly_report():
#
#     user_id = 4  # Replace with the desired user ID
#
#
#     report_file = generate_monthly_report(user_id)
#     print(f"Report generated: {report_file}")
#     return {"message": "Report generated successfully!"}

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/create_role', methods=['POST', 'GET'])
def create_role():
    if request.method == 'POST':
        role = request.form.get('role_name')
        
        print(role)
        app.security.datastore.create_role(name=role)
        db.session.commit()
        return redirect('/admin_dashboard')

    return render_template('create_role.html')

@app.post('/create-user')
def create_user():
    data=request.get_json()
    # Create and save the user
    fname = data['fname']
    lname=data['lname']
    role = data['roles']
    mobile=data['mobile']
    email=data['email']
    password=data['password']
    is_auth=data['is_auth']
    encoded_password = password.encode('utf-8')
    hashed_password = hashlib.sha256(encoded_password).hexdigest()

    app.security.datastore.create_user(fname=fname, lname=lname, roles=role, mobile=mobile, email=email,
                                       password=hashed_password, authenticated=is_auth)

    db.session.commit()

    return {"message":"Success"}

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        data=request.form
        # Create and save the user
        fname = data['fname']
        lname=data['lname']
        role = "user"
        mobile=data['mobile']
        email=data['email']
        password=data['password']
        # is_auth=data['is_auth']
        encoded_password = password.encode('utf-8')
        hashed_password = hashlib.sha256(encoded_password).hexdigest()

        app.security.datastore.create_user(fname=fname, lname=lname, roles=[role], mobile=mobile, email=email,
                                        password=hashed_password)

        db.session.commit()

        return render_template('signin.html')
    else:
        return render_template('signup.html')


@app.route('/signout')
def signout():
    logout_user()
    return redirect('/signin')



from flask import send_file
@app.route('/download_csv')
def download_csv():
    return send_file(f'./instance/name.csv', as_attachment=True)


@app.get("/cached-data")
def cached_data():
    time.sleep(10)
    return {"cached_data": "sds"}

@app.route("/get-roles")

def get_roles():
    return [x.name for x in db.session.query(Role).all()]


@app.route('/signin', methods=['POST', 'GET'])
def signin():
    message = request.args.get('message')
    if request.method == 'POST':
        data = request.form
        email = data['email']
        print(email)
        user = db.session.query(User).filter_by(email=email).first()
        print(user)
        if user is None:
            return redirect(url_for('signin', message="User not found!"))
        else:
            password = data['password']
            encoded_password = password.encode('utf-8')
            hashed_password = hashlib.sha256(encoded_password).hexdigest()
            if not verify_password(hashed_password, user.password):
                print("true")
                return redirect(url_for('signup', message="Incorrect Password!"))
            


        result = login_user(user) 
        if user.get_roles[0] == 'admin':
            return redirect('/admin_dashboard')
        elif user.get_roles[0] == 'manager':
            return redirect('/manager_dashboard')
        else:
            return redirect('/user_dashboard')

        

    return render_template('signin.html',message=message)

@app.get("/signout")
# @login_required
def logout():
    logout_user()
    return make_response({"message":"User Logged Out Successfully!"},200)

user=current_user
@app.route('/admin_dashboard')
@roles_required('admin')
def admin_dashboard():
    roles=db.session.query(Role).all()
    print(roles)
    
    return render_template('admin_dashboard.html',roles=roles,user=user)

@app.route('/delete_role/<id>')
def delete_role(id):
    role=db.session.query(Role).filter_by(id=id).first()
    db.session.delete(role)
    db.session.commit()
    return redirect('/admin_dashboard')

@app.route('/manager_dashboard')
@roles_required('manager')
def manager_dashboard():
    return render_template('manager_dashboard.html',user=user)

@app.route('/user_dashboard')
@roles_required('user')
def user_dashboard():
    return render_template('user_dashboard.html',user=user)




@app.route("/get-user")
@auth_required('token')

def get_user():
    return {"email": current_user.email,
             "id": current_user.id,
             "role": [role.name for role in current_user.roles]}

@app.route("/get-users")
@auth_required('token')
@roles_required('admin')

def get_users():
    return [{"email": user.email,
             "id": user.id,
             "role": [role.name for role in user.roles]} for user in db.session.query(User).all()]

# @app.get('/ds')
# def ds():
#     from models import Cart
#     item = db.session.query(Cart).first()
#     print(item.__dict__)
#     print(item.cart_product.__dict__)
#
#     return "hello"


@app.route('/get-user-details')
@login_required #Only after the route otherwise wont work
def get_user_details():
    return {"username": current_user.username,
             "id": current_user.id,
             "role": [role.name for role in current_user.roles]}


@app.route('/get-authenticated-data')
@auth_required('token')
# to allow admin and user to access the route
@roles_required('manager')
def get_authenticated_data():
    return {"username": current_user.username,
             "id": current_user.id,
             "role": [role.name for role in current_user.roles],
             "message": "Only can access if you pass token"}



@app.route('/multiple-roles')
@roles_accepted('admin', 'manager')

def multiple_roles():
    return {"username": current_user.username,
             "id": current_user.id,
             "role": [role.name for role in current_user.roles],
             "message": "Only can access if you are a manager or admin"}

@app.route('/get-user-token')
def get_user_token():
    return {"token": current_user.get_auth_token()}


@app.route('/user-role-data')
@roles_required('user')
def user_role_date():
    return {"username": current_user.username,
             "id": current_user.id,
             "role": [role.name for role in current_user.roles],
             "message": "Only can access if you are a user"}




@app.route('/gen_csv')
def gen_csv():
    from tasks import bla
    task=bla.delay()
    return jsonify({"task-id": task.id})

@app.route('/task')
def taskgy():

    task=monthly_report.delay()
    return jsonify({"task-id": task.id})

@app.get('/get_csv/<task_id>')
def get_csv(task_id):
    res = AsyncResult(task_id)
    print(res)
    if res.ready():
        filename = res.result
        return send_file(filename, as_attachment=True)
    else:
        return jsonify({"message": "Task Pending"}), 404
 



@app.post('/add-to-desktop')
def add_to_desktop():
    data=request.get_json()
    app_name = data['name']
    icon_path = data['icon']
    app_route = data['url']

    shortcut_path= f'/Users/shriprasad/Desktop/{app_name}'
    # Creating the desktop shortcut
    make_shortcut(app_name,shortcut_path,icon=icon_path, terminal=False)

    return {"Message":"Shortcut Created Successfully!"}

if __name__ == "__main__":
    app.run(debug=True,port=5003)