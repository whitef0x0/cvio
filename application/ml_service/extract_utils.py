"""
Text Extraction Functions For Strings
"""
from __future__ import absolute_import
import re

def extract_email_addresses(string):
	r = re.compile(r'[\w\.-]+@[\w\.-]+')
	return r.findall(string)

def has_email_addresses(string):
	r = re.compile(r'[\w\.-]+@[\w\.-]+')
	has_match = r.search(string)
	if has_match is not None:
		return True
	else: 
		return False

def extract_phone_numbers(string):
	r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
	phone_numbers = r.findall(string)
	return [re.sub(r'\D', '', number) for number in phone_numbers]


def has_phone_numbers(string):
	r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
	has_match = r.search(string)
	if has_match is not None:
		return True
	else: 
		return False

def string_is_sentence(sentence):
    for i, token in enumerate(sentence):
        if token.i == sentence.end-1 and (token.text == '.' or token.text == '!' or token.text == '?' or token.text == ';'):
            return True
    return False