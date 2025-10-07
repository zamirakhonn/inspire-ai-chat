from flask_restx import Namespace, Resource, fields
from flask import request
from datetime import datetime
from services.ai import generate_reply
from services.history import get_chat_history, add_to_history

ns = Namespace("chat", description="Chat with Inspire AI")

chat_request = ns.model("ChatRequest", {
    "user_id": fields.String(required=True, description="User unique ID or token"),
    "message": fields.String(required=True, description="User message to chatbot")
})

chat_response = ns.model("ChatResponse", {
    "reply": fields.String(description="AI assistant's response"),
    "time": fields.String(description="Response timestamp"),
})

@ns.route("/")
class Chat(Resource):
    @ns.expect(chat_request)
    @ns.marshal_with(chat_response)
    def post(self):
        """Chat with Inspire AI"""
        data = request.get_json()
        user_id = data.get("user_id", "anonymous_user").strip()
        message = data.get("message", "").strip()

        if not message:
            return {"reply": "⚠️ Please send a valid message.", "time": datetime.now().strftime("%H:%M")}

        try:
            # Save user message to history
            add_to_history(user_id, "user", message)

            # Generate assistant reply
            reply = generate_reply(user_id, message)

            # Save AI reply to history
            add_to_history(user_id, "assistant", reply)

            return {"reply": reply, "time": datetime.now().strftime("%H:%M")}
        except Exception as e:
            return {
                "reply": f"⚠️ Internal error: {str(e)}",
                "time": datetime.now().strftime("%H:%M")
            }

    def get(self):
        """Info route"""
        return {
            "reply": "Use POST with JSON: {'user_id': 'your_id', 'message': 'your text'}",
            "time": datetime.now().strftime("%H:%M")
        }
