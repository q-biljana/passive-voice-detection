
from flask import Flask, request, jsonify
import os
import json 

### here: a function to flag -- what language you want import THAT module
from text_analysis_en import analyze_text


app = Flask(__name__)

#{"segments":[{"segment_id":4025439,"segment":"Skip to main content"}]}

test_json = '{"segments":[{"segment_id":4025439,"segment":"The molecular energies were calculated"}]}'

#print (test_json)
#print (test_json[1][0])
#print (test_json["segments"]["segment_id"] )

original_txt, data, metrics = analyze_text(test_json)
print ("analyzed data: ", data )

def loc_of_passive():	
	passive_loc = []
	for i in range(len(data['passive_voice_cases'])): 
		if data['passive_voice_cases'][i] is not None: 
			passive_loc.append(i)
	return passive_loc 

# return location of passive voice 
print ("passive voice at : ", loc_of_passive())