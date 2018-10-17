#
# Text_analysis.py
# this file contains the business logic for passive_app.py 
# 
#
import __future__import division
import os
import re
from bs4 import BeautifulSoup
import operator
import nltk
import json 


#### List of dictionaries used for 
"""
KEEP
	tokens
		# tokenize sentences into words and punctuation marks
	data['parts_of_speech']
		# modified in the following -- but also find verb groups
		# tag tokens as part-of-speech
   		# fix symbol and apostrophed verb tags
		# fix some verbs ending in -ing being counted as nouns


	verb_group_count
	verb_group_stack

		# find verb groups
	    data['verb_groups'] = [None] * len(tokens)
	    verb_group_stack = []
	    verb_group_count = 0

"""
# pre-load and pre-compile required variables and methods

# this business right here are the unicode quotation marks 
quotation_re = re.compile(u'[\u00AB\u00BB\u201C\u201D\u201E\u201F\u2033\u2036\u301D\u301E]')
apostrophe_re = re.compile(u'[\u02BC\u2019\u2032]')
punct_error_re = re.compile('^(["\]\)\}]+)(?:[ \n]|$)')
ellipsis_re = re.compile('\.\.\.["\(\)\[\]\{\} ] [A-Z]')
newline_re = re.compile('\n["\(\[\{ ]*[A-Z]')
empty_sent_re = re.compile('^[\n ]*$')
nominalization_re = re.compile('(?:ion|ions|ism|isms|ty|ties|ment|ments|ness|nesses|ance|ances|ence|ences)$')
stopset = set(nltk.corpus.stopwords.words('english'))
stemmer = nltk.PorterStemmer()
tagger = nltk.data.load(nltk.tag._POS_TAGGER)
lemmatizer = nltk.WordNetLemmatizer()
dict_cmu = nltk.corpus.cmudict.dict()
dict_wn = nltk.corpus.wordnet


with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'corpora/fillers')) as f:
    dict_fillers = f.read().splitlines()
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'corpora/irregular-stems')) as f:
    dict_irregular_stems_lines = f.read().splitlines()
    dict_irregular_stems_draft = [line.split(',') for line in dict_irregular_stems_lines]
    dict_irregular_stems = {}
    for stem_old, stem_new in dict_irregular_stems_draft:
        dict_irregular_stems[stem_old] = stem_new



def analyze_text(json_content):

    # create data and metrics dictionaries
    data = dict()
    metrics = dict()

    ### parse text/json string

    # I don't think I wanna use Beautiful soup at all 
    # soup = BeautifulSoup(html)
    # original_text = soup.get_text().rstrip('\n')

    original_text = json.loads(str(json_content))

    # standardize all quotation marks
    text = quotation_re.sub('"', original_text)
    text = apostrophe_re.sub("'", text)

    # tokenize text into sentences
    text_eg_ie = text.replace('e.g.', 'e.---g.').replace('i.e.', 'i.---e.')
    sents_draft = nltk.sent_tokenize(text_eg_ie)
    for idx, sent in enumerate(sents_draft[:]):
        sents_draft[idx] = sents_draft[idx].replace('e.---g.', 'e.g.').replace('i.---e.', 'i.e.')
        if idx > 0:
            punct_error = punct_error_re.findall(sent)
            if punct_error:
                sents_draft[idx-1] += punct_error[0]
                sents_draft[idx] = sents_draft[idx][len(punct_error[0])+1:]

    # separate sentences at ellipsis characters correctly
    sents_draft_2 = []
    for sent in sents_draft:
        idx = 0
        for ellipsis_case in ellipsis_re.finditer(sent):
            sents_draft_2.append(sent[idx:(ellipsis_case.start() + 3)])
            idx = ellipsis_case.start() + 3
        sents_draft_2.append(sent[idx:])

    # separate sentences at newline characters correctly
    sents = []
    for sent in sents_draft_2:
        idx = 0
        for newline_case in newline_re.finditer(sent):
            sents.append(sent[idx:(newline_case.start() + 1)])
            idx = newline_case.start() + 1
        sents.append(sent[idx:])

    # delete empty sentences
    sents = [sent for sent in sents if not empty_sent_re.match(sent)]

    # tokenize sentences into words and punctuation marks
    sents_tokens = [nltk.word_tokenize(sent) for sent in sents]
    tokens = [token for sent in sents_tokens for token in sent]
    data['values'] = tokens
    data['sentence_numbers'] = [(idx+1) for idx, sent in enumerate(sents_tokens) for token in sent]

    # find words
    sents_words = [[token.lower() for token in sent if (token[0].isalnum() or (token in
                    ["'m", "'re", "'ve", "'d", "'ll"]))] for sent in sents_tokens]
    words = []
    word2token_map = []
    for idx, token in enumerate(tokens):
        if token[0].isalnum() or (token in ["'m", "'re", "'ve", "'d", "'ll"]):
            words.append(token.lower())
            word2token_map.append(idx)

    # find word stems
    stems = [stem_better(word) for word in words]
    data['stems'] = [None] * len(tokens)
    for idx, stem in enumerate(stems):
        data['stems'][word2token_map[idx]] = stem

    # tag tokens as part-of-speech
    sents_tokens_tags = tagger.batch_tag(sents_tokens)
    data['parts_of_speech'] = [pos for sent in sents_tokens_tags for (token, pos) in sent]

    # fix symbol and apostrophed verb tags
    for idx, token in enumerate(tokens):
        if not token[0].isalnum():
            if token in ["'m", "'re", "'ve"]:
                data['parts_of_speech'][idx] = 'VBP'
            elif token == "'s":
                if data['parts_of_speech'][idx] != 'POS':
                    data['parts_of_speech'][idx] = 'VBP'
            elif token == "'d":
                data['parts_of_speech'][idx] = 'VBD'
            elif token == "'ll":
                data['parts_of_speech'][idx] = 'MD'
            elif data['parts_of_speech'][idx].isalnum():
                data['parts_of_speech'][idx] = 'SYM'

    # fix some verbs ending in -ing being counted as nouns
    for idx, token in enumerate(tokens):
        if (token[-3:] == 'ing') and (idx < len(tokens)) and (data['parts_of_speech'][idx+1] == 'IN'):
            data['parts_of_speech'][idx] = 'VBG'

    # find verb groups
    data['verb_groups'] = [None] * len(tokens)
    verb_group_stack = []
    verb_group_count = 0
    for idx, token in enumerate(tokens):
        if not verb_group_stack:
            if token in ["be", "am", "'m", "is", "'s", "are", "'re", "was", "were", "will", "'ll", "wo", "have", "'ve", "has", "had"]:
                verb_group_stack.append(idx)
        elif token in ['be', 'been', 'being', 'have', 'had']:
            verb_group_stack.append(idx)
        elif data['parts_of_speech'][idx][:2] == 'VB':
            verb_group_stack.append(idx)
            verb_group_count += 1
            for i in verb_group_stack:
                data['verb_groups'][i] = verb_group_count
            verb_group_stack = []
        elif data['parts_of_speech'][idx][:2] not in ['RB', 'PD']:
            if len(verb_group_stack) > 1:
                verb_group_count += 1
                for i in verb_group_stack:
                    data['verb_groups'][i] = verb_group_count
            verb_group_stack = []

    # find expected word frequencies
    data['expected_word_frequencies'] = [None] * len(tokens)
    unmatched_stems = []
    for idx_word, stem in enumerate(stems):
        idx = word2token_map[idx_word]
        if stem in dict_word_freq.keys():
            data['expected_word_frequencies'][idx] = dict_word_freq[stem]
        else:
            data['expected_word_frequencies'][idx] = 0
            unmatched_stems.append(stem)



    ### compute metrics on parsed data

    # count number of sentences
    metrics['sentence_count'] = len(sents)

    # count number of words
    metrics['word_count'] = len(words)


    # count number of characters in the whole text
    metrics['character_count'] = len(text)


    # find and count passive voice cases
    data['passive_voice_cases'] = [None] * len(tokens)
    passive_voice_count = 0
    for i in range(verb_group_count):
        verb_group_stack = [idx for idx in range(len(tokens)) if data['verb_groups'][idx] == i+1]
        if data['parts_of_speech'][verb_group_stack[-1]] in ['VBN', 'VBD']:
            for j in verb_group_stack[:-1]:
                if tokens[j] in ["am", "'m", "is", "'s", "are", "'re", "was", "were", "be", "been", "being"]:
                    passive_voice_count += 1
                    data['passive_voice_cases'][j] = passive_voice_count
                    data['passive_voice_cases'][verb_group_stack[-1]] = passive_voice_count
                    break
    if metrics['sentence_count']:
        metrics['passive_voice_ratio'] = passive_voice_count / metrics['sentence_count']
    else:
        metrics['passive_voice_ratio'] = 0



    return original_text, data, metrics
