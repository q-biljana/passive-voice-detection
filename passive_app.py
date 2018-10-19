
from flask import Flask, request, jsonify
import os
import json 

### here: a function to flag -- what language you want import THAT module
from text_analysis_en import analyze_text


app = Flask(__name__)

#{"segments":[{"segment_id":4025439,"segment":"Skip to main content"}]}

test_json = '{"segments":[{"segment_id":4025439,"segment":"Skip to main content"}]}'

print (test_json)
print (test_json[1][0])
#print (test_json["segments"]["segment_id"] )