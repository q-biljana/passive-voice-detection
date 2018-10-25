"""
	Contains the Passive class that performs the actions associated with passive voice check
		- finds the location of the text in the request
		- calls on NLP functions that 
"""

import re
from app.text_analysis_en import analyze_text


def check_passive(input_str):
	"""
		imports NLP function analyze_text which checks for passive voice  
	"""
	original_txt, data, metrics, tokens = analyze_text(input_str)
	print("check_passive, original txt" , original_txt)
	print("and tokens, ", tokens)
	test_s = "".join(original_txt)
	#print ("dummy approach -- ", test_s)
	#print (list(test_s)[:12])

	passive_loc = loc_of_passive(original_txt, data)
	if not any(passive_loc):
		return "no passive voice in text"
	else:
		return "passive voice at location: ", passive_loc #, beginning, end

def find_segment_id(dictionary): 
	"""	
		finds each segment id in request  
	"""
	store_id = []
	for a in range(len(dictionary['bulkText'])):
		for k,v in dictionary['bulkText'][a].items():
			store_id.append(k)
	return store_id


def find_text(key, dictionary):
	"""
		finds a specific key (string) in a nested dictionary 
	"""
	for k, v in dictionary.items():
		if k == key:
			yield v
		elif isinstance(v, dict):
			for result in find_text(key, v):
				yield result
		elif isinstance(v, list):
			for d in v:
				for result in find_text(key, d):
					yield result

def loc_of_passive(org_txt, dictionary):
	"""
		returns the location of passive voice when present in tokenized segment
	"""
	passive_loc = []
	print("yo. ", dictionary['passive_voice_cases'])
	#return a list of indexes for passive voice
	c = [i for i, n in enumerate(dictionary['passive_voice_cases']) if n is not None]
	# return the words that are passive
	print("original text ", org_txt)
	words = [ org_txt[a] for a in c]
	sentence = " ".join(words)
	print(sentence)

	for word in words:
		start_index = sentence.find(word) #original text
		end_index = start_index + len(word)
		print (start_index, end_index)
		passive_loc.append((start_index, end_index))
	print (passive_loc)
	return passive_loc

	#for i in range(len(dictionary['passive_voice_cases'])): 



	# 	if dictionary['passive_voice_cases'][i] is not None: 
	# 		passive_loc.append(1)
	# 	else:
	# 		passive_loc.append(None)
	# return passive_loc 

def position_of_char(s,txt):
	#txt.find(s)
	a = re.search(r'\b'+s+'\b', txt)
	return int(a.start()), int(a.end())



