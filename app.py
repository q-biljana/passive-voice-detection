"""

routing functions 
"""

from flask import Flask, request, jsonify, make_response
import json 
from app.models import check_passive, find

app = Flask(__name__)

@app.route('/passive_voice/v1/<string:lang_id>', methods=['POST'])
def passive_api(lang_id):


	if lang_id == 'en':
		request_body = request.get_json()
		store_text = list(find("text", request_body))

		store_response = [check_passive(a) for a in store_text]
		return jsonify(store_response)
	else:
		return "Language not supported"


@app.errorhandler(500)
def internal_error(error):
	return "500 error; bad request"

@app.errorhandler(405)
def not_found(error):
    return make_response(jsonify({'error': 'method not allowed'}), 405)

if __name__ == '__main__':
	app.run(host='0.0.0.0')