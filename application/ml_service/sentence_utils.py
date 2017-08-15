"""
Utility Functions for Spacy Sentences
"""
from __future__ import absolute_import

import spacy, textacy
nlp = spacy.load('en')

from nltk.sentiment.vader import SentimentIntensityAnalyzer

def get_sentiment_score(sent):
	sid = SentimentIntensityAnalyzer()
	ss = sid.polarity_scores(sent)
	return ss;

def get_narrative_voice(sent):
	firstPersonPronouns = ["I", "we", "me", "us", "my", "mine", "ours"]
	secondPersonPronouns = ["you", "your", "yours"]
	thirdPersonPronouns = ["he", "she", "it", "they", "him", "hers", "them", "their", "his", "its", "theirs"]

	narrativeVoice = "";

	for tok in sent:
		if nlp.vocab.strings['PRON'] == tok.pos:
			if tok.orth_ in firstPersonPronouns and (narrativeVoice == "first" or narrativeVoice == ""):
				narrativeVoice = "first"
			elif tok.orth_ in secondPersonPronouns and (narrativeVoice == "second" or narrativeVoice == ""):
				narrativeVoice = "second"
			elif tok.orth_ in thirdPersonPronouns and (narrativeVoice == "third" or narrativeVoice == ""):
				narrativeVoice = "third"
			else:
				return "mixed"

	return narrativeVoice;

def get_tense(sentence):
	headToken = sentence.root
	tense = __traverse_tree_find_head_verb(headToken, 0)
	return tense

def is_relevant_to_paragraph(curr_sentence, paragraph):
	similarityScore = 0

	sentences = [s for s in paragraph.sents]
	for sent in sentences:
		if curr_sentence.text != sent.text and not curr_sentence.similarity(sent) == 1:
			similarityScore = curr_sentence.similarity(sent)

	similarityScore = similarityScore/len(sentences)
	return similarityScore > 0.25

def is_correct_length(sent):
	numWords = sum(1 for token in sent if not token.is_punct and not token.is_space)
	if numWords >= 11 and numWords <= 17:
		return True
	else:
		return False

def get_length(sent):
	numWords = sum(1 for token in sent if not token.is_punct and not token.is_space)
	return numWords

"""
Private Module Functions
"""

def __determine_verb_tense(verb):
	if verb.pos_ == "MD":
		return "future"
	elif verb.pos_ in ["VBP", "VBZ","VBG"]:
		return "present"
	else:
		return "past"

def __traverse_tree_find_head_verb(headToken, level):
	if headToken.pos_ == 'VERB':
		return __determine_verb_tense(headToken)

	numChildren = sum(1 for x in headToken.children)
	if numChildren == 0:
		return False
	else:
		for child in headToken.children:
			result = __traverse_tree_find_head_verb(child, level+1)
			if result != False:
				return result