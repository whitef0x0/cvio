CoverLetterIO 
==========================================
[![Build Status](https://travis-ci.org/whitef0x0/coverletterIO.svg?branch=master)](https://travis-ci.org/whitef0x0/coverletterIO)

CoverletterIO is a "Cover Letter Style Checker" libary built in python that uses ML and Rule-based NLP to suggest improvements and rank your coverletters.


## Prerequisites
To install please run
```
pip3 install nltk
pip3 install spacy
pip3 install textacy
```

And run this in your python3 shell
```
python3
import nltk
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
```

```bash
$ pip3 install -r requirements.txt
$ python -m spacy.en.download all
```

##Usage
To use, first make sure you have python3 installed.

If you don't have python3, you can install it from [here](https://www.python.org/downloads/)

Then in your python application, import the library as `import coverletterIO` and use it.

## Testing Your Application
You can run the unit test suite with this command
```bash
python3 -m unittest discover -p "*_test.py"
```

You can run the benchmark test suite with this command
```bash
python3 -m unittest discover -p "*_benchmark.py"
```
## Community
* Ping me on [Twitter](http://twitter.com/davidbaldwynn)

## Credits
Inspired by [textio](https://textio.com)

## License
[The MIT License](LICENSE.md)