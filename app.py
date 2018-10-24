
from flask import Flask, request, jsonify, make_response
import json 
from text_analysis_en import analyze_text


app = Flask(__name__)

def loc_of_passive(data):	
	passive_loc = []
	for i in range(len(data['passive_voice_cases'])): 
		if data['passive_voice_cases'][i] is not None: 
			passive_loc.append(1)
		else:
			passive_loc.append(None)
	return passive_loc 

def check_passive(input_str):
	original_txt, data, metrics = analyze_text(input_str)
	passive_loc = loc_of_passive(data)
	if not any(passive_loc):
		return "no passive voice in text"
	else:
		return "passive voice at location: ", passive_loc 

def find(key, dictionary):
    for k, v in dictionary.items():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in find(key, d):
                    yield result


@app.route('/passive_voice/v1/<string:lang_id>', methods=['POST'])
def passive_api(lang_id):

	if lang_id == 'en':
		request_body = request.get_json()


		print(request_body)
		store_text = list(find('text', request_body))
		print(store_text)
		print (type(store_text[0]))
		store_response = [check_passive(a) for a in store_text]

		print (store_response)
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


















