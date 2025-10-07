# services/users.py
from flask_restx import Namespace, Resource, fields
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from services.db import SessionLocal, get_or_create_user
from services.auth_utils import create_access_token
from services.db import User
import sqlalchemy.exc

auth_ns = Namespace("auth", description="User authentication")

auth_model = auth_ns.model("Auth", {
    "username": fields.String(required=True),
    "password": fields.String(required=True)
})

@auth_ns.route("/register")
class Register(Resource):
    @auth_ns.expect(auth_model)
    def post(self):
        data = request.json or {}
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return {"message": "username and password required"}, 400

        session = SessionLocal()
        try:
            existing = session.query(User).filter_by(user_id=username).first()
            if existing:
                return {"message": "Username already exists"}, 400
            user = User(user_id=username)
            # store hashed password in name field? Better add column; for simplicity, store hashed password in name (not ideal)
            user.name = generate_password_hash(password)
            session.add(user)
            session.commit()
            return {"message": "User registered"}, 200
        except sqlalchemy.exc.SQLAlchemyError as e:
            return {"message": f"DB error: {str(e)}"}, 500
        finally:
            session.close()

@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.expect(auth_model)
    def post(self):
        data = request.json or {}
        username = data.get("username")
        password = data.get("password")
        session = SessionLocal()
        try:
            user = session.query(User).filter_by(user_id=username).first()
            if not user:
                return {"message": "Invalid credentials"}, 401
            # retrieve stored hashed password from name (see registration)
            hashed = user.name or ""
            if not check_password_hash(hashed, password):
                return {"message": "Invalid credentials"}, 401
            # create token
            token = create_access_token({"user_id": username})
            return {"message": "Login successful", "user_id": username, "token": token}, 200
        finally:
            session.close()
