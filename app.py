"""

routing functions 
"""

from flask import Flask, request, jsonify, make_response
import json 
from app.models import check_passive, find_text, find_segment_id

app = Flask(__name__)

@app.route('/passive_voice/v1/<string:lang_id>', methods=['POST'])
def passive_api(lang_id):

	if lang_id.find("en-") >=0 :
		request_body = request.get_json()

		store_text = list(find_text("text", request_body))
		store_id = find_segment_id(request_body)
		store_response = [] 
		for a in store_text:
			print(check_passive(a))
			if type(check_passive(a)) is str: 
				store_response.append(a)
			else:
				resp=[]
				for b in range(len(check_passive(a))):
					resp.append({"fromPosition": check_passive(a)[b][0], "toPosition": check_passive(a)[b][1] })
					
				store_response.append(resp)

		print("\t", store_response)
		resp_dict = dict(zip(store_id, store_response))
		return jsonify(resp_dict) 
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