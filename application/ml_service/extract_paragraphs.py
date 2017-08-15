"""
Extract Paragraphs From a Spacy Document
"""
from __future__ import absolute_import
import spacy
nlp = spacy.load('en')

from . import token_utils
from . import extract_utils

##Public Methods

#Get Applicants Signature from CV
def get_signature(docs):

	i = len(docs)
	while i > 1:
		i = i - 1
		prev_sentence = [s for s in docs[i-1].sents]
		curr_sentence = [s for s in docs[i].sents]

		#Check that prev sentence is a farewell
		if len(curr_sentence) == 1 and len(prev_sentence) == 1 and len(prev_sentence[0]) == 2 and prev_sentence[0][1].is_punct:

			#Check that every token in current sentence is a proper noun
			is_all_proper_nouns = False
			for token in curr_sentence[0]:
				if token_utils.is_proper_noun(token):
					is_all_proper_nouns = True
				else:
					is_all_proper_nouns = False

			if(is_all_proper_nouns):
				return curr_sentence[0], i

	return False, False

#Get Farewell Line from CV
def get_farewell(docs):

	_, index = get_signature(docs)

	if index and index > 0:
		farewell_sentence = [s for s in docs[index-1].sents][0]

		if farewell_sentence:
			return farewell_sentence, index-1
	return False, False

#Get Greeting Line from CV (if it exists)
def get_greeting(docs):
	x = 0
	for doc in docs:
		curr_paragraph = [s for s in doc.sents]
		curr_sentence = curr_paragraph[0]

		if len(curr_paragraph) == 1:
			#Check that every token in current sentence is a proper noun except last
			is_all_proper_nouns = False
			for i, token in enumerate(curr_sentence):
				if token_utils.is_proper_noun(token):
					is_all_proper_nouns = True
				elif i == len(curr_sentence)-1:
					is_all_proper_nouns = is_all_proper_nouns
				else:
					is_all_proper_nouns = False

			if(is_all_proper_nouns and token_utils.is_greeting(curr_sentence[0])):
				return curr_sentence, x
		x = x + 1
	return False, False

#Get Opening Paragraph
def get_opening_paragraph(docs):
	for i, doc in enumerate(docs):
		curr_paragraph = [s for s in doc.sents]
		allSentencesValid = False
		for sentence in curr_paragraph:
			if extract_utils.string_is_sentence(sentence):
				allSentencesValid = True
			else:
				allSentencesValid = False
				break;
		if allSentencesValid:
			return docs[i], i
	return False, False

#Get Final Paragraph
def get_final_paragraph(docs):
	_, start = get_opening_paragraph(docs)
	for i, doc in enumerate(docs[::-1]):
		curr_paragraph = [s for s in doc.sents]
		if extract_utils.string_is_sentence(curr_paragraph[0]):
			return docs[len(docs)-i-1], len(docs)-i-1
	return False, False

def get_middle_paragraphs(docs):
	_, start_index = get_opening_paragraph(docs)

	_, end_index = get_final_paragraph(docs)

	if end_index is not False and start_index is not False:
		return docs[start_index+1:end_index]
	else:
		return False

def get_all_paragraphs(docs):
	_, start_index = get_opening_paragraph(docs)

	_, end_index = get_final_paragraph(docs)

	if end_index is not False and start_index is not False:
		return docs[start_index:end_index+1]
	else:
		return False

def get_total_num_sentences(docs):
	num_sentences = 0

	_, start_index = get_opening_paragraph(docs)

	_, end_index = get_final_paragraph(docs)

	if end_index is False or start_index is False:
		return False

	for i in range(start_index, end_index+1):
		num_sentences += __get_num_sentences_of_paragraph(docs[i])

	return num_sentences

def get_num_of_paragraphs(docs):
	_, start_index = get_opening_paragraph(docs)

	_, end_index = get_final_paragraph(docs)

	if end_index is False or start_index is False:
		return False

	return end_index - start_index + 1

##Private Methods
def __get_num_sentences_of_paragraph(paragraph):
	sentences = [s for s in paragraph.sents]
	return len(sentences)