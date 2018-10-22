
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

def check_passive(input_str, elem):
	original_txt, data, metrics = analyze_text(input_str,elem)
	passive_loc = loc_of_passive(data)
	if not any(passive_loc):
		return "no passive voice in text", None	
	else:
		return "passive voice at location: ", passive_loc 


@app.route('/passive_voice/v1/<string:lang_id>', methods=['POST'])
def passive_api(lang_id):

	if lang_id == 'en':
		request_body = request.get_json()

		if 'segments' in request_body:

			store_response = []
			for a, item in enumerate(request_body['segments']):
				segment = request_body['segments']
				segment_id = request_body['segments'][a]['segment_id']
				text = request_body['segments'][a]['segment']
				test_passive, passive_loc = check_passive(request_body, a)		
				if passive_loc is not None: 
					store_response.append( { "passive_voice_location": passive_loc, "words" :text })
				else:
					store_response.append({"passive_result": test_passive, "words" :text } )

		return jsonify(store_response) 

	else:
		return "Language not supported"

@app.errorhandler(405)
def not_found(error):
    return make_response(jsonify({'error': 'method not allowed'}), 405)

if __name__ == '__main__':
	app.run(host='0.0.0.0')


















