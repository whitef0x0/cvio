import spacy, textacy, nltk
nlp = spacy.load('en')

import string, re, os

'''
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
'''

from . import extract_paragraphs
from . import token_utils
from . import sentence_utils
from . import extract_utils

#import hunspell
import proselint

print("Loaded CoverLetter Heuristics\n")

dir = os.path.dirname(os.path.abspath(__file__))
#hunspell_dic_path = os.path.join(dir, '../../hunspell/en_US-large.dic')
#hunspell_aff_path = os.path.join(dir, '../../hunspell/en_US-large.aff')

#spellchecker = hunspell.HunSpell(hunspell_dic_path, hunspell_aff_path)

def uniquify_list(seq, idfun=None): 
   # order preserving
   if idfun is None:
       def idfun(x): return x
   seen = {}
   result = []
   for item in seq:
       marker = idfun(item)
       # in old Python versions:
       # if seen.has_key(marker)
       # but in new ones:
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
   return result


"""
CV Scoring Functions
"""

def sentence_length(docs):
	totalSentenceLengths = 0
	totalSentences = 0

	for doc in docs:
		for sent in doc.sents:
			totalSentences = totalSentences + 1
			totalSentenceLengths += sentence_utils.length(sent)
	if totalSentences != 0:
		return totalSentenceLengths/totalSentences
	else:
		return 0

def word_count(docs):
	wordCount = 0
	for doc in docs:
		for sent in doc.sents:
			for token in sent:
				if not token.is_punct and not token.is_space:
					wordCount = wordCount + 1
	return wordCount

def proselint_score(paragraphs):
	results = []
	doc_index = 0
	num_errors = 0

	paragraph_index = 0
	for paragraph in paragraphs:
		sentences = [s for s in paragraph.sents]
		sentence_index = 0

		for sent in sentences:
			suggestions = proselint.tools.lint(sent.text)
			results.append({
				'suggestions': suggestions
			})
			num_errors = num_errors + len(suggestions)
			sentence_index = sentence_index + 1

		paragraph_index = paragraph_index + 1
	return (len(results), results)

def lexical_illusions(paragraphs):
	lexical_regex = re.compile('(\\s*)([^\\s]+)', re.I)
	word_regex = re.compile('/\w+/')

	results = []
	doc_index = 0

	paragraph_index = 0
	for paragraph in paragraphs:
		sentences = [s for s in paragraph.sents]
		sentence_index = 0

		for sent in sentences:
			lastMatch = ''
			lexcial_matches = lexical_regex.finditer(sent.text)

			for match in lexcial_matches:
				if (word_regex.match(match.group(2)) is not None) and (match.group(2).lower() == lastMatch):
					results.append(match.group(2))
					lastMatch = match.group(2)
			sentence_index = sentence_index + 1

		paragraph_index = paragraph_index + 1
	return (len(results), results)

def num_exclamation_point(paragraphs):
	exclamation_regex = re.compile('(!{1,})', re.IGNORECASE)
	exclamation_count = 0

	for paragraph in paragraphs:
		exclamation_matches = exclamation_regex.finditer(paragraph.text)
		for match in exclamation_matches:
			exclamation_count = exclamation_count + 1
	return exclamation_count

def ratio_2nd_person_pronouns_to_1st_person_pronouns(paragraphs):
	num_second_person_prons = 0
	num_first_person_prons = 0

	for paragraph in paragraphs:
		for sent in paragraph.sents:
			for token in sent:
				if token_utils.is_first_person_pronoun(token):
					num_first_person_prons = num_first_person_prons + 1
				elif token_utils.is_second_person_pronoun(token):
					num_second_person_prons = num_second_person_prons + 1

	if num_first_person_prons != 0:
		return num_second_person_prons/num_first_person_prons
	else:
		return 0

def too_wordy_score(paragraphs):
	f = open(os.path.join(dir, './wordy_words.txt'), "r")
	wordy_words = f.read().splitlines()
	escaped_wordy_words = [re.escape(word) for word in wordy_words]

	wordy_regex = re.compile('\\b(' + '|'.join(escaped_wordy_words) + ')\\b', re.IGNORECASE)
	f.close()

	results = []

	paragraph_index = 0
	for paragraph in paragraphs:
		sentences = [s for s in paragraph.sents]
		sentence_index = 0

		for sent in sentences:
			wordy_matches = wordy_regex.finditer(sent.text)
			for match in wordy_matches:
				results.append(match.group(0))
			sentence_index = sentence_index + 1

		paragraph_index = paragraph_index + 1
	return (len(results), results)

def cliches_score(paragraphs):
	f = open(os.path.join(dir, './cliches.txt'), "r")
	cliches = f.read().splitlines()
	escaped_cliches = [re.escape(cliche) for cliche in cliches]

	cliche_regex = re.compile('\\b(' + '|'.join(escaped_cliches) + ')\\b', re.IGNORECASE)
	f.close()

	results = []
	doc_index = 0

	paragraph_index = 0
	for paragraph in paragraphs:
		sentences = [s for s in paragraph.sents]
		sentence_index = 0

		for sent in sentences:
			cliche_matches = cliche_regex.finditer(sent.text)
			for match in cliche_matches:
				results.append(match.group(0))
			sentence_index = sentence_index + 1

		paragraph_index = paragraph_index + 1
	return (len(results), results)

def repeated_phrases_score(docs):
	span_list = list(textacy.extract.ngrams(docs, 3, filter_stops=False, filter_nums=True, min_freq=2))
	repeated_phrases = uniquify_list([span.text for span in span_list])
	return (len(repeated_phrases), repeated_phrases)
'''
def spelling_mistake_score(paragraphs):

	spellingMistakes = []
	for paragraph in paragraphs:
		sentences = [s for s in paragraph.sents]
		for sent in sentences:
			for token in sent:
				if token.pos_ != 'PROPN' and not token.ent_type and not token.is_punct and not token.like_url and not token.like_email and not token.like_num and not token.is_stop and not token.is_space and token.is_alpha:
					if not spellchecker.spell(token.text):
						spellingMistakes.append({
							'word': token.text
						})
	return len(spellingMistakes), spellingMistakes
'''
def sentence_length_score(docs):
	sentencesWithCorrectLengths = 0
	numSentences = 0

	totalSentenceLength = 0
	avgSentenceLength = 0

	for doc in docs:
		for sent in doc.sents:
			numSentences = numSentences + 1
			totalSentenceLength = totalSentenceLength + sentence_utils.get_length(sent)
			if sentence_utils.is_correct_length(sent):
				sentencesWithCorrectLengths = sentencesWithCorrectLengths + 1
	if numSentences != 0:
		avgSentenceLength = totalSentenceLength/numSentences
		percentageSentencesOfCorrectLength = sentencesWithCorrectLengths/numSentences

		return percentageSentencesOfCorrectLength, avgSentenceLength
	else:
		return False, False

def valid_number_of_paragraphs(paragraphs):
	numParagraphs = len(paragraphs)
	if(numParagraphs >= 3 and numParagraphs <= 6):
		return True
	return False

def valid_word_count(docs):
	wordCount = 0
	for doc in docs:
		for sent in doc.sents:
			for token in sent:
				if not token.is_punct and not token.is_space:
					wordCount = wordCount + 1

	if wordCount <= 430 and wordCount >= 275:
		return True
	else:
		return False

def has_contact_details(docs):
	paragraphs = extract_paragraphs.get_all_paragraphs(docs)
	for paragraph in paragraphs:
		if extract_utils.has_email_addresses(paragraph.text) or extract_utils.has_phone_numbers(paragraph.text):
			return True
	return False

def has_greeting(docs):
	_, greeting_exists = extract_paragraphs.get_greeting(docs)

	if greeting_exists is not False:
		return True
	return False

def has_farewell(docs):
	_, farewell_exists = extract_paragraphs.get_farewell(docs)

	if farewell_exists is not False:
		return True
	return False

def has_signature(docs):
	_, signature_exists = extract_paragraphs.get_signature(docs)

	if signature_exists is not False:
		return True
	return False

def active_verb_percentage(docs):
	passiveVerbs = 0
	activeVerbs = 0
	totalVerbs = 0

	for doc in docs:
		for sent in doc.sents:
			for token in sent:
				if token.pos_ == 'VERB':
					totalVerbs = totalVerbs + 1
					children = token.children
					for child in children:
						if child.dep_ == 'auxpass' or child.dep_ == 'nsubjpass' or child.dep_ == 'csubjpass':
							passiveVerbs = passiveVerbs + 1
							break
	activeVerbs = totalVerbs - passiveVerbs
	#print("ActiveVerbs: {0} PassiveVerbs: {1}".format(activeVerbs, passiveVerbs))
	if totalVerbs != 0:
		return activeVerbs/totalVerbs
	else:
		return 0

def adjective_percentage(docs):
	totalTokens = 0
	totalAdjectives = 0
	for doc in docs:
		for sent in doc.sents:
			for token in sent:
				if not token.is_punct:
					totalTokens = totalTokens + 1
				if token_utils.is_adjective(token):
					totalAdjectives = totalAdjectives + 1
	if totalTokens != 0:
		#print('Adjective percentage: {0}%'.format(100*totalAdjectives/totalTokens))
		return totalAdjectives/totalTokens
	else:
		return 0

def verb_percentage(docs):
	totalTokens = 0
	totalVerbs = 0
	for doc in docs:
		for sent in doc.sents:
			for token in sent:
				if not token.is_punct:
					totalTokens = totalTokens + 1
				if token.pos_ == 'VERB':
					totalVerbs = totalVerbs + 1
	if totalTokens != 0:
		#print('Verb percentage: {0}%'.format(100*totalVerbs/totalTokens))
		return totalVerbs/totalTokens
	else:
		return 0

def action_word_percentage(docs):
	f = open(os.path.join(dir, 'action_words.csv'), "r")
	action_words = f.read().splitlines()

	totalVerbs = 0
	totalActionWords = 0
	for doc in docs:
		for sent in doc.sents:
			for token in sent:
				if token.pos_ == 'VERB':
					totalVerbs = totalVerbs + 1
					if token.lower_ in action_words:
						totalActionWords = totalActionWords + 1
	f.close()

	if totalVerbs != 0:
		#print('Action Verb Percentage: {0}%'.format(100*totalActionWords/totalVerbs))
		return totalActionWords/totalVerbs
	else:
		return 0

def contains_offensive_words(docs):
	f = open(os.path.join(dir, './offensive_words.txt'), "r")
	offensive_words = f.read().splitlines()

	totalTokens = 0
	totalActionWords = 0
	offensiveWords = []
	for doc in docs:
		for sent in doc.sents:
			for token in sent:
				if token.lower_ in offensive_words:
					offensiveWords.append(token)
	f.close()

	if len(offensiveWords) != 0:
		#print('There are {0} offensive words in this CV'.format(len(offensiveWords)))
		return True, offensiveWords
	else:
		#print('There an no offensive words in this CV')
		return False, None

def acronym_entity_percentage(docs):
	totalEntities = 0
	totalAcronyms = 0
	for doc in docs:
		currIOB = ''
		for sent in doc.sents:
			for token in sent:
				if token.ent_iob_ == 'B' and (currIOB == '' or currIOB == 'O'):
					totalEntities = totalEntities + 1
					#print(token.text)
					currIOB = 'B'
				elif token.ent_iob_ == 'I' and (currIOB == 'B' or currIOB == 'I'):
					currIOB = 'I'
					#print(token.text)
				else:
					curIOB = ''
				if textacy.text_utils.is_acronym(token.text) and not (token.ent_iob == 'I' or token.ent_iob_ == 'B'):
					totalAcronyms = totalAcronyms + 1
					totalEntities = totalEntities + 1
				elif textacy.text_utils.is_acronym(token.text):
					totalAcronyms = totalAcronyms + 1
	if totalEntities != 0:
		return totalAcronyms/totalEntities
	else:
		return 0

#Calculate percentage of sentences that are positive
def positivity_score(docs, paragraphs):
	totalNumNegSentences = 0
	totalNumSentences = extract_paragraphs.get_total_num_sentences(docs)

	for paragraph in paragraphs:
		for sent in paragraph.sents:
			if sentence_utils.get_sentiment_score(sent.text)['neg'] > sentence_utils.get_sentiment_score(sent.text)['pos']:
				totalNumNegSentences += 1

	sentencePositivityScore = (totalNumSentences - totalNumNegSentences) / totalNumSentences
	return sentencePositivityScore

#Calculate percentage of sentences written in a 'first-person' narrative voice
def narrative_voice_score(docs, paragraphs):
	totalNumWrongNarrativeVoiceSentences = 0
	totalNumSentences = extract_paragraphs.get_total_num_sentences(docs)

	for paragraph in paragraphs:
		sentences = [s for s in paragraph.sents]
		for sent in sentences:
			if not sentence_utils.get_narrative_voice(sent) == 'first;':
				totalNumWrongNarrativeVoiceSentences += 1

	narrativeVoiceScore = (totalNumSentences - totalNumWrongNarrativeVoiceSentences) / totalNumSentences
	return narrativeVoiceScore

#Calculate percentage of sentences with past tense
def past_tense_score(docs, paragraphs):
	totalNumSentences = extract_paragraphs.get_total_num_sentences(docs)

	totalPastTenseSentences = 0
	for paragraph in paragraphs:
		for sent in paragraph.sents:
			if sentence_utils.get_tense(sent) == 'past':
				totalPastTenseSentences = totalPastTenseSentences + 1

	sentencePastTensePercentage = totalPastTenseSentences / totalNumSentences
	return sentencePastTensePercentage

#Calculate sentence relevancy score
def relevancy_score(docs, paragraphs):
	totalNumSentences = extract_paragraphs.get_total_num_sentences(docs)
	totalNumIrrelevantSentences = 0

	for paragraph in paragraphs:
		for sent in paragraph.sents:
			if not sentence_utils.is_relevant_to_paragraph(sent, paragraph):
				totalNumIrrelevantSentences += 1

	sentenceRelevantScore = (totalNumSentences - totalNumIrrelevantSentences) / totalNumSentences
	return sentenceRelevantScore

"""
Setup Functions
"""

def setup_cv(file):
	with open(file) as f:
		content = f.readlines()
		string_content = f.read()

	entire_doc = nlp(string_content)

	trimmed_file = []
	#Remove newlines
	for line in content:
		if line != '\n':
			trimmed_file.append(line.rstrip())

	docs = []
	for line in trimmed_file:
		decoded_line = nlp(line)
		docs.append(decoded_line)
	f.close()
	paragraphs = extract_paragraphs.get_all_paragraphs(docs)

	return (docs, paragraphs, entire_doc)

def setup_cv_text(content):
	trimmed_file = []

	entire_doc = nlp(content)

	#Remove newlines
	lines = content.splitlines()
	for line in lines:
		if line != '\n' and line != '':
			trimmed_file.append(line.rstrip())

	docs = []
	for line in trimmed_file:
		decoded_line = nlp(line)
		docs.append(decoded_line)

	paragraphs = extract_paragraphs.get_all_paragraphs(docs)
	return (docs, paragraphs, entire_doc)