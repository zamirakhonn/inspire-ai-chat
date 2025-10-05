from flask_restx import Namespace, Resource, fields
from services.db import add_diary_entry, get_diary
from datetime import datetime
from flask import session

ns = Namespace("diary", description="Parent diary entries")

diary_model = ns.model("DiaryEntry", {
    "entry": fields.String(required=True),
    "date": fields.String
})

@ns.route("/")
class Diary(Resource):
    @ns.expect(diary_model)
    def post(self):
        user_id = session.get("user_id", "demo_user")
        entry = self.api.payload.get("entry")
        add_diary_entry(user_id, {"entry": entry, "date": datetime.now().strftime("%Y-%m-%d")})
        return {"message": "Diary entry added."}

    def get(self):
        user_id = session.get("user_id", "demo_user")
        return {"diary": get_diary(user_id)}
