print("Starting to Load App.py\n")

from flask import request, render_template, jsonify, url_for, redirect, g
from .models import User, CoverLetter
from index import app, db
from sqlalchemy.exc import IntegrityError
from .utils.auth import generate_token, requires_auth, verify_token

from .ml_service import score
#from .ml_service import get_model

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/<path:path>', methods=['GET'])
def any_root_path(path):
    return render_template('index.html')

@app.route("/api/user", methods=["GET"])
@requires_auth
def get_user():
    return jsonify(result=g.current_user)

@app.route("/api/create_user", methods=["POST"])
def create_user():
    incoming = request.get_json()
    user = User(
        email=incoming["email"],
        password=incoming["password"]
    )
    db.session.add(user)

    try:
        db.session.commit()
    except IntegrityError:
        return jsonify(message="User with that email already exists"), 409

    new_user = User.query.filter_by(email=incoming["email"]).first()

    return jsonify(
        id=user.id,
        token=generate_token(new_user)
    )


@app.route("/api/get_token", methods=["POST"])
def get_token():
    incoming = request.get_json()
    user = User.get_user_with_email_and_password(incoming["email"], incoming["password"])
    if user:
        return jsonify(token=generate_token(user))

    return jsonify(error=True), 403


@app.route("/api/is_token_valid", methods=["POST"])
def is_token_valid():
    incoming = request.get_json()
    is_valid = verify_token(incoming["token"])

    if is_valid:
        return jsonify(token_is_valid=True)
    else:
        return jsonify(token_is_valid=False), 403


@app.route("/api/coverletter/stats", methods=["POST"])
def get_coverletter_stats():
    incoming = request.get_json()

    if not incoming.get('coverletter'):
        return jsonify(error="Missing coverletter text"), 500

    if not incoming.get('coverletter_title'):
        cv = CoverLetter(
           text=incoming["coverletter"]
        )
    else:
        cv = CoverLetter(
            text=incoming["coverletter"],
            title=incoming["coverletter_title"]
        )
    spacy_doc, paragraphs, entire_doc = score.setup_cv_text(incoming['coverletter'])

    if not paragraphs:
        return jsonify(error="No paragraphs found in text"), 406

    db.session.add(cv)
    try:
        db.session.commit()
    except IntegrityError:
        print("Coverletter with that text already exists")
    else:
        print("Coverletter successfully saved")

    '''
    outcome, dist = get_model.classify(spacy_doc)
    probability_scores = []
    for label in dist.samples():
        probability_scores.append({
            'label': label,
            'prob': dist.prob(label)
        })
    print("CV has been classified")
    '''
    returnObj = {    
        #'outcome': outcome,
        #'confidence': probability_scores,
        'relevancy_score': score.relevancy_score(spacy_doc, paragraphs),
        'positivity_score': score.positivity_score(spacy_doc, paragraphs),
        'past_tense_score': score.past_tense_score(spacy_doc, paragraphs),

        'valid_word_count': score.valid_word_count(spacy_doc),
        'sentence_length': list(score.sentence_length_score(spacy_doc))[0],

        'narrative_voice_percentage': score.narrative_voice_score(spacy_doc, paragraphs),
        'acronym_entity_percentage': score.acronym_entity_percentage(spacy_doc),
        'action_word_percentage': score.action_word_percentage(spacy_doc),
        'active_verb_percentage': score.active_verb_percentage(spacy_doc),
        'adjective_percentage': score.adjective_percentage(spacy_doc),
        'verb_percentage': score.verb_percentage(spacy_doc),

        'contains_offensive_words': list(score.contains_offensive_words(paragraphs))[0],
        'spelling_mistakes_score': list(score.spelling_mistake_score(paragraphs))[0],
        'spelling_mistakes_list': list(score.spelling_mistake_score(paragraphs))[1],
        
        'lexical_illusions': list(score.lexical_illusions(paragraphs))[0],
        'lexical_illusions_list': list(score.lexical_illusions(paragraphs))[1],

        'proselint_score': list(score.proselint_score(paragraphs))[0],
        'proselint_list': list(score.proselint_score(paragraphs))[1],
        'cliches_score': list(score.cliches_score(paragraphs))[0],
        'cliches_list': list(score.cliches_score(paragraphs))[1],
        'too_wordy_score': list(score.too_wordy_score(paragraphs))[0],
        'too_wordy_list': list(score.too_wordy_score(paragraphs))[1],
        'exclamation_point_count': score.num_exclamation_point(paragraphs),
        'repeated_phrases_count': list(score.repeated_phrases_score(entire_doc))[0],
        'repeated_phrases_list': list(score.repeated_phrases_score(entire_doc))[1],

        'has_contact_details': score.has_contact_details(spacy_doc),
        'has_greeting': score.has_greeting(spacy_doc),
        'has_signature': score.has_signature(spacy_doc),
        'ratio_2nd_person_pronouns_to_1st_person_pronouns': score.ratio_2nd_person_pronouns_to_1st_person_pronouns(spacy_doc)
    }

    return jsonify(results=returnObj)
