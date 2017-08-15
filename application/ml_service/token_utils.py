"""
Set of small utility functions that take Spacy tokens as input.
"""

import spacy
nlp = spacy.load('en')

def is_greeting(token):
	greeting_list = ["Dear", "dear", "hi", "hey", "To whom it may concern", "Hi", "Hey"]
	if ( is_interjection_or_adjective(token) or is_noun(token) ) and token.text in greeting_list:
		return True
	else:
		return False

def is_first_person_pronoun(token):
	if token.pos_ == 'PRON': 
		first_person_pronouns = ["I", "me", "myself", "mine", "my", "mine", "me", "we", "us", "ourselves", "ours", "our"]
		if token.lower_ in first_person_pronouns:
			return True
	return False

def is_second_person_pronoun(token):
	if token.pos_ == 'PRON': 
		second_person_pronouns = ["you", "yourself", "yours", "your", "yourselves"]
		if token.lower_ in second_person_pronouns:
			return True
	return False

def is_proper_noun_singular(token):
	if(nlp.vocab.strings['NNP'] == token.tag): return True
	return False

def is_proper_noun(token):
	if(nlp.vocab.strings['PROPN'] == token.pos): return True
	return False

def is_interjection_or_adjective(token):
	if(nlp.vocab.strings['UH'] == token.tag):
		return True
	elif(nlp.vocab.strings['JJ'] == token.tag):
		return True
	else:
		return False

def is_noun(token):
	if(nlp.vocab.strings['NN'] == token.tag): return True
	if(nlp.vocab.strings['NNS'] == token.tag): return True
	if(nlp.vocab.strings['NNP'] == token.tag): return True
	if(nlp.vocab.strings['NNPS'] == token.tag): return True
	return False

def is_adjective(token):
	if(nlp.vocab.strings['JJ'] == token.tag): return True
	if(nlp.vocab.strings['JJR'] == token.tag): return True
	if(nlp.vocab.strings['JJS'] == token.tag): return True
	return False

def is_noun_singular(token):
	if(nlp.vocab.strings['NNS'] == token.tag): return True
	if(nlp.vocab.strings['NNPS'] == token.tag): return True
	return False

