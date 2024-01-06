import hashlib
def admin_create_user():
    from app import app, db
    # Create and save the user
    fname = "MrBean"
    lname="Teddy"
    role = ["admin"]
    mobile=1234567890
    email="app.mrbean@gmail.com"
    password="admin123"
    is_auth=1
    encoded_password = password.encode('utf-8')
    hashed_password = hashlib.sha256(encoded_password).hexdigest()

    app.security.datastore.create_user(fname=fname, lname=lname, roles=role, mobile=mobile, email=email,
                                       password=hashed_password, authenticated=is_auth)

    db.session.commit()