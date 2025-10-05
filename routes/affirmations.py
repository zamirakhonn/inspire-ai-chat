from flask_restx import Namespace, Resource, fields
from services.db import get_affirmations
from datetime import datetime

ns = Namespace("affirmations", description="Daily affirmations")

affirmation_model = ns.model("AffirmationResponse", {
    "affirmations": fields.List(fields.String),
    "time": fields.String
})

@ns.route("/")
class Affirmations(Resource):
    @ns.marshal_with(affirmation_model)
    def get(self):
        return {"affirmations": get_affirmations(), "time": datetime.now().strftime("%H:%M")}
