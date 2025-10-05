from flask_restx import Namespace, Resource, fields
from flask import session
from services.ai import generate_response
from services.history import get_chat_history, add_to_history
from datetime import datetime

ns = Namespace("chat", description="Chat with Inspire AI")

chat_request = ns.model("ChatRequest", {
    "message": fields.String(required=True)
})

chat_response = ns.model("ChatResponse", {
    "reply": fields.String,
    "time": fields.String
})

@ns.route("/")
class Chat(Resource):
    @ns.expect(chat_request)
    @ns.marshal_with(chat_response)
    def post(self):
        user_id = session.get("user_id", "demo_user")  # Placeholder
        message = self.api.payload.get("message", "").strip()
        if not message:
            return {"reply": "⚠️ Send a message.", "time": datetime.now().strftime("%H:%M")}

        add_to_history(user_id, "user", message)
        try:
            answer = generate_response(message, get_chat_history(user_id))
            add_to_history(user_id, "assistant", answer)
            return {"reply": answer, "time": datetime.now().strftime("%H:%M")}
        except Exception as e:
            return {"reply": f"⚠️ Error: {str(e)}", "time": datetime.now().strftime("%H:%M")}

    def get(self):
        return {"reply": "Use POST with JSON {'message':'your text'}", "time": datetime.now().strftime("%H:%M")}
