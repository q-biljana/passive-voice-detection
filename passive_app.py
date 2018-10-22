
from flask import Flask, request, jsonify, make_response
import json 

### here: a function to flag -- what language you want import THAT module
from text_analysis_en import analyze_text


app = Flask(__name__)

#test_json= '{"segments":[{"segment_id":4025439,"segment":"Skip to main content"}]}'
test_json = '{"segments":[{"segment_id":4025439,"segment":"The molecular energies were calculated"}]}'

#print (test_json)
#print (test_json[1][0])
#print (test_json["segments"]["segment_id"] )

original_txt, data, metrics = analyze_text(test_json)
#print ("analyzed data: ", data )

def loc_of_passive(data):	
	passive_loc = []
	for i in range(len(data['passive_voice_cases'])): 
		if data['passive_voice_cases'][i] is not None: 
			passive_loc.append(i)
	return passive_loc 

# return location of passive voice 
#print ("passive voice at : ", loc_of_passive(data))

"""
	at the moment analyze the input, 
	and return the location of passive voice 
"""

def check_passive(input):
	original_txt, data, metrics = analyze_text(input)
	passive_loc = loc_of_passive(data)
	#print(len(passive_loc))
	if not passive_loc:
		return "no passive voice"
	else:
		return "passive voice at location: ", passive_loc 

result = check_passive(test_json)
print (result)
#@app.route('/passive_voice/v1/<string:lang>', methods=['POST'])
@app.route('/passive_voice/v1/en', methods=['POST'])
def passive_api():
	user_content = request.json.get("segment")
	output_data = check_passive(user_content)
	response = jsonify({'passive_response': output_data})

@app.errorhandler(405)
def not_found(error):
    return make_response(jsonify({'error': 'method not allowed'}), 405)

if __name__ == '__main__':
	app.run(host='0.0.0.0')


















