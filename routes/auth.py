from flask_restx import Namespace, Resource, fields

ns = Namespace("auth", description="Authentication endpoints")

login_model = ns.model("Login", {
    "username": fields.String(required=True),
    "password": fields.String(required=True)
})

# Simple placeholder, no real DB auth
users = {}

@ns.route("/register")
class Register(Resource):
    @ns.expect(login_model)
    def post(self):
        data = ns.payload
        users[data["username"]] = data["password"]
        return {"message": "User registered successfully."}

@ns.route("/login")
class Login(Resource):
    @ns.expect(login_model)
    def post(self):
        data = ns.payload
        if users.get(data["username"]) == data["password"]:
            # In real app, return JWT token
            return {"message": "Login successful.", "user_id": data["username"]}
        return {"message": "Invalid credentials"}, 401
