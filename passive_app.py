
from flask import Flask, request, jsonify, make_response
import json 
from text_analysis_en import analyze_text


app = Flask(__name__)

#test_json= {"segments":[{"segment_id":4025439,"segment":"Skip to main content"}]}
#test_json = '{"segments":[{"segment_id":4025439,"segment":"The molecular energies were calculated"}]}'

def loc_of_passive(data):	
	passive_loc = []
	for i in range(len(data['passive_voice_cases'])): 
		if data['passive_voice_cases'][i] is not None: 
			passive_loc.append(i)
	return passive_loc 

def check_passive(input_str):
	original_txt, data, metrics = analyze_text(input_str)
	passive_loc = loc_of_passive(data)
	#print(len(passive_loc))
	if not passive_loc:
		return "no passive voice", None
	else:
		return "passive voice at location: ", passive_loc 


@app.route('/passive_voice/v1/<string:lang_id>', methods=['POST'])
#debug @app.route('/passive_voice/v1/en', methods=['POST'])
def passive_api(lang_id):

	if lang_id == 'en':
		test = request.get_json()
		#debug print(test)

		if 'segments' in test:
			print ("\t debug ")
			segment = test['segments']
			segment_id = test['segments'][0]['segment_id']
			text = test['segments'][0]['segment']
			test_passive, passive_loc = check_passive(test)		


			if passive_loc: 
				return  jsonify( {"passive_result": test_passive, "passive_location": passive_loc, "segment_id" : segment_id, "words" :text } )
			else:
				return  jsonify( {"passive_result": test_passive, "segment_id" : segment_id, "words" :text } )

	else:
		return "Language not supported"

@app.errorhandler(405)
def not_found(error):
    return make_response(jsonify({'error': 'method not allowed'}), 405)

if __name__ == '__main__':
	app.run(host='0.0.0.0')


















