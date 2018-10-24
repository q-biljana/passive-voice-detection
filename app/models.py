"""
	Contains the Passive class that performs the actions associated with passive voice check
		- finds the location of the text in the request
		- calls on NLP functions that 
"""

from app.text_analysis_en import analyze_text


def check_passive(input_str):
	"""
		imports NLP function analyze_text which checks for passive voice  
	"""
	original_txt, data, metrics = analyze_text(input_str)
	passive_loc = loc_of_passive(data)
	if not any(passive_loc):
		return "no passive voice in text"
	else:
		return "passive voice at location: ", passive_loc 


def find(key, dictionary):
	"""
		finds a specific key (string) in a nested dictionary 
	"""
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

def loc_of_passive(dictionary):
	"""
		returns the location of passive voice when present in tokenized segment
	"""
	passive_loc = []
	for i in range(len(dictionary['passive_voice_cases'])): 
		if dictionary['passive_voice_cases'][i] is not None: 
			passive_loc.append(1)
		else:
			passive_loc.append(None)
	return passive_loc 





