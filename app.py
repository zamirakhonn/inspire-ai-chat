from flask import Flask, request
from flask_restx import Api, Resource, fields
from dotenv import load_dotenv
import os

from services import users, ai

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecretkey")

# Initialize Flask-RESTX
api = Api(app, version="1.0", title="Inspire AI API",
          description="API для общения с Inspire AI 🌿",
          doc="/swagger")  # Swagger UI at /swagger

# ----------------- Auth Namespace -----------------
auth_ns = api.namespace("auth", description="User authentication")
auth_model = api.model("Auth", {
    "username": fields.String(required=True),
    "password": fields.String(required=True)
})

@auth_ns.route("/register")
class Register(Resource):
    @auth_ns.expect(auth_model)
    def post(self):
        data = request.json
        if users.register_user(data["username"], data["password"]):
            return {"message": "User registered successfully."}, 200
        return {"message": "Username already exists."}, 400

@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.expect(auth_model)
    def post(self):
        data = request.json
        if users.check_credentials(data["username"], data["password"]):
            return {"message": "Login successful.", "user_id": data["username"]}, 200
        return {"message": "Invalid credentials"}, 401

# ----------------- Chat Namespace -----------------
chat_ns = api.namespace("chat", description="Chat with Inspire AI")
chat_model = api.model("ChatRequest", {
    "user_id": fields.String(required=True, description="User ID from login"),
    "message": fields.String(required=True, description="User message to AI")
})
chat_response = api.model("ChatResponse", {
    "reply": fields.String(description="AI reply"),
    "time": fields.String(description="Timestamp")
})

@chat_ns.route("/")
class Chat(Resource):
    @chat_ns.expect(chat_model)
    @chat_ns.marshal_with(chat_response)
    def post(self):
        data = request.json
        user_id = data.get("user_id")
        message = data.get("message", "").strip()
        if not user_id or not message:
            return {"reply": "⚠️ Provide user_id and message.", "time": "-"}, 400
        return ai.generate_reply(user_id, message)

# Add namespaces
api.add_namespace(auth_ns)
api.add_namespace(chat_ns)

# ----------------- Run App -----------------
if __name__ == "__main__":
    app.run(debug=True, port=5001)
