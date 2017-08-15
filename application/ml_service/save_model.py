'''
Generates model and saves it to a json file
'''

from . import score
from . import extract_paragraphs

import nltk, spacy, textacy
nlp = spacy.load('en')

import os, glob, random

dir = os.path.dirname(os.path.abspath(__file__))
good_path = os.path.join(dir, '../../../data/cv/good/')
bad_path = os.path.join(dir, '../../../data/cv/good/')

goodCVs = []
badCVs = []

'''Given two dicts, merge them into a new dict as a shallow copy.'''
def merge_two_dicts(x, y):
	z = x.copy()
	z.update(y)
	return z

def cv_features(docs):
	features = {}

	#Classifier Accuracy:
	proper_pronoun_count = 0
	personal_pronoun_count = 0
	relative_pronoun_count = 0
	animate_count = 0
	inanimate_count = 0

	paragraphs = extract_paragraphs.get_all_paragraphs(docs)
	if paragraphs:
		for paragraph in paragraphs:
			proper_pronouns = textacy.extract.named_entities(paragraph, include_types=["ORG", "PERSON", "LOC", "PRODUCT"])
			for pronoun in proper_pronouns:
				if pronoun.__getitem__(0).ent_type_ == "PERSON":
					animate_count = animate_count + 1
				else:
					inanimate_count = inanimate_count + 1
				proper_pronoun_count = proper_pronoun_count + 1

			relative_pronoun_phrases = textacy.extract.pos_regex_matches(paragraph, r'<DET>? <NUM>* (<ADJ> <PUNCT>? <CONJ>?)* (<PROPN> <PART>?)+')
			
			relative_pronoun_count = relative_pronoun_count + sum(1 for pronoun_phrase in relative_pronoun_phrases)

			for sent in paragraph.sents:
				for token in sent:
					if token.tag_ == 'PRP':
						personal_pronoun_count = personal_pronoun_count + 1

	features["word_count"] = score.word_count(docs)
	features["active_verb_percentage"] = score.active_verb_percentage(docs)
	features['relative_pronoun_count'] = relative_pronoun_count
	features['animate_count'] = animate_count
	features['inanimate_count'] = inanimate_count
	
	return features

#Read all good resumes
for filename in glob.glob(os.path.join(good_path, '*.txt')):
	currCV, _, _ = score.setup_cv(filename)

	text = extract_paragraphs.get_all_paragraphs(currCV)

	if text is not False:
		goodCVs.append(currCV)

#Read all bad resumes
for filename in glob.glob(os.path.join(bad_path, '*.txt')):
	currCV, _, _ = score.setup_cv(filename)

	text = extract_paragraphs.get_all_paragraphs(currCV)

	if text is not False:
		badCVs.append(currCV)

labeled_cvs = ([(cv, 'Good') for cv in goodCVs] + [(cv, 'Bad') for cv in badCVs])

featuresets = [(cv_features(cv), cv_type) for (cv, cv_type) in labeled_cvs]
random.shuffle(featuresets)

algorithm = nltk.classify.MaxentClassifier.ALGORITHMS[0]
classifier = nltk.MaxentClassifier.train(featuresets, algorithm, max_iter=4)

print("Loaded CoverLetter Model\n")

def classify(spacy_doc):
	return (classifier.classify(cv_features(spacy_doc)), classifier.prob_classify(cv_features(spacy_doc)))
