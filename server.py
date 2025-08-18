import flask
from flask import Response, jsonify, request
from flask.views import MethodView

from sqlalchemy.exc import IntegrityError
from models import Advertisement, Session
from errors import HttpError
from schema import CreateAdvertisement, UpdateAdvertisement, validate_json

app = flask.Flask("first_flask_app")

@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response: Response):
    request.session.close()
    return response

@app.errorhandler(HttpError)
def error_handler(error: HttpError) -> Response:
    http_response = jsonify({"error": error.message})
    http_response.status_code = error.code
    return http_response

def get_adv_by_id(adv_id: int) -> Advertisement:
    adv = request.session.get(Advertisement, adv_id)
    if adv is None:
        raise HttpError(404 , "Advertisement is not found")
    return adv

def add_adv(advertisement: Advertisement):
    try:
        request.session.add(advertisement)
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, "Advertisement is already exists")

class AdvertisementView(MethodView):

    def get(self, adv_id: int):
        advertisement = get_adv_by_id(adv_id)
        return jsonify(advertisement.dict)


    def post(self):
        json_data = validate_json(request.json, CreateAdvertisement)
        advertisement = Advertisement (
            title = json_data["title"],
            description = json_data["description"],
            owner = json_data["owner"]
        )
        add_adv(advertisement)
        return jsonify(advertisement.id_dict)


    def patch(self, adv_id: int):
        json_data = validate_json(request.json, UpdateAdvertisement)
        adv = get_adv_by_id(adv_id)
        if "title" in json_data:
            adv.title = json_data["title"]
        if "description" in json_data:
            adv.description = json_data["description"]
        request.session.commit()
        return jsonify(adv.id_dict)


    def delete(self, adv_id: int):
        adv = get_adv_by_id(adv_id)
        request.session.delete(adv)
        request.session.commit()
        return jsonify({"message": "Advertisement deleted"})

adv_view = AdvertisementView.as_view('advertisement_view')

app.add_url_rule(
    "/api/v1/advertisements",
    view_func=adv_view,
    methods=["POST"]
)
app.add_url_rule(
    "/api/v1/advertisements/<int:adv_id>",
    view_func=adv_view,
    methods=["GET", "PATCH", "DELETE"]
)

app.run(debug=True)
