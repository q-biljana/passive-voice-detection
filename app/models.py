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
	test_s = "".join(original_txt)

	passive_loc = loc_of_passive(original_txt, tokens, data)
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

def loc_of_passive(org_txt, tokens, dictionary):
	"""
		returns the location of passive voice when present in tokenized segment
	"""
	passive_loc = []
	#return a list of indexes for passive voice
	c = [(i,n) for i, n in enumerate(dictionary['passive_voice_cases']) if n is not None]
	# return the words that are passive
	words = [ (tokens[a], num) for a, num in c]

	unique = []
	for word, num in words:
		#if first occurance
		if word not in unique:
			start_ix = org_txt.find(word) 
			end_ix = start_ix + len(word)
			unique.append(word)
			passive_loc.append((start_ix, end_ix))
		# if not first occurance
		else:
			count = unique.count(word)+1
			start_ix, end_ix = find_nth(org_txt, word,count)
			unique.append(word)
			passive_loc.append((start_ix, end_ix))

	return passive_loc


def find_nth(haystack, needle, n):
	# find the n'th iteration of substring "needle" in string "haystack" 
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start, start +len(needle)

def position_of_char(s,txt):
	#txt.find(s)
	a = re.search(r'\b'+s+'\b', txt)
	return int(a.start()), int(a.end())



