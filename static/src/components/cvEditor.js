import React, {DOM as E} from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import * as actionCreators from '../actions/coverletter';

import { EditorState, CompositeDecorator } from 'draft-js';
import Editor from 'draft-js-editor';
import Popover from 'react-popover';

class PopoverComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isOpen: false,
      hover: false
    };
  }
  togglePopoverEnter = () => {
    this.setState({
      isOpen: true,
      hover: true
    })
  }
  togglePopoverLeave = () => {
    this.setState({
      isOpen: false,
      hover: false
    })
  }
  render(){
  }
};

class ClicheComponent extends PopoverComponent {
  render(){
    var problemSpanStyle = styles.problemDecorator;
    if (this.state.hover) {
      problemSpanStyle.backgroundColor = '#4CAF50'
    } else {
      problemSpanStyle.backgroundColor = '#FFCE8B'
    }
    var popoverBody = [E.div({style: styles.problemPopover}, "Watch out for corporate cliches. Describing why you are uniquely suited to the job makes you standout in the pile.")];
    return (
      <Popover isOpen={this.state.isOpen} body={popoverBody}>
        <span className="phrase-highlight" onMouseEnter={this.togglePopoverEnter} onMouseLeave={this.togglePopoverLeave} style={problemSpanStyle}>
          {this.props.children}
        </span>
      </Popover>
    );
  }
};

class WordyComponent extends PopoverComponent {
  render(){
    var problemSpanStyle = styles.problemDecorator;
    if (this.state.hover) {
      problemSpanStyle.backgroundColor = '#4CAF50'
    } else {
      problemSpanStyle.backgroundColor = '#FFCE8B'
    }
    var popoverBody = [E.div({style: styles.problemPopover}, "This is an wordy word/phrase. Being concise makes your coverletter easier to read.")];
    return (
      <Popover isOpen={this.state.isOpen} body={popoverBody}>
        <span className="phrase-highlight" onMouseEnter={this.togglePopoverEnter} onMouseLeave={this.togglePopoverLeave} style={problemSpanStyle}>
          {this.props.children}
        </span>
      </Popover>
    );
  }
};

class NeutralComponent extends PopoverComponent {
  render(){
    var neutralSpanStyle = styles.neutralDecorator;
    if (this.state.hover) {
      neutralSpanStyle.backgroundColor = '#a8a8a8'
    } else {
      neutralSpanStyle.backgroundColor = '#e8e8e8'
    }
    var popoverBody = [E.div({style: styles.neutralPopover}, "This phrase is repeated several times in your coverletter.")];

    return (
      <Popover isOpen={this.state.isOpen} body={popoverBody}>
        <span className="phrase-highlight" onMouseEnter={this.togglePopoverEnter} onMouseLeave={this.togglePopoverLeave} style={neutralSpanStyle}>
          {this.props.children}
        </span>
      </Popover>
    );
  }
};

var getRepeatedStrategy = (repeated_phrases_list) => {

  return (contentBlock, callback) => {
    var REPEATED_REGEX = null
    if(repeated_phrases_list.length == 1){
      REPEATED_REGEX = new RegExp('(' + repeated_phrases_list[0] + ')', 'g')
    } else {
      REPEATED_REGEX = new RegExp('(' + repeated_phrases_list.join('|') + ')', 'g') 
    }

    const text = contentBlock.getText();
    let matchArr, start;

    while ((matchArr = REPEATED_REGEX.exec(text)) !== null) {
      start = matchArr.index;
      callback(start, start + matchArr[0].length);
    }
  }
}

var getClicheStrategy = (cliche_list) => {

  return (contentBlock, callback) => {
    var CLICHE_REGEX = null
    if(cliche_list.length == 1){
      CLICHE_REGEX = new RegExp('(' + cliche_list[0] + ')', 'g')
    } else {
      CLICHE_REGEX = new RegExp('(' + cliche_list.join('|') + ')', 'g') 
    }

    const text = contentBlock.getText();
    let matchArr, start;

    while ((matchArr = CLICHE_REGEX.exec(text)) !== null) {
      start = matchArr.index;
      callback(start, start + matchArr[0].length);
    }
  }
}

var getWordyStrategy = (too_wordy_list) => {

  return (contentBlock, callback) => {
    console.log(too_wordy_list);
    var WORDY_REGEX = null;

    if(too_wordy_list.length == 1){
      WORDY_REGEX = new RegExp('(' + too_wordy_list[0] + ')', 'g')
    } else {
      console.log('wordyStrategy');
      WORDY_REGEX = new RegExp('(' + too_wordy_list.join('|') + ')', 'g') 
    }

    const text = contentBlock.getText();
    let matchArr, start;

    while ((matchArr = WORDY_REGEX.exec(text)) !== null) {
      start = matchArr.index;
      callback(start, start + matchArr[0].length);
    }
  }
}

const getDecorators = (coverletter_state) => {
  var decorators = []

  if(coverletter_state.stats){
    if(coverletter_state.stats.repeated_phrases_list && coverletter_state.stats.repeated_phrases_list.length > 0){
      var repeatedStrategy = getRepeatedStrategy(coverletter_state.stats.repeated_phrases_list);
      decorators.push({
        strategy: repeatedStrategy,
        component: NeutralComponent
      });
    }

    if(coverletter_state.stats.cliches_list && coverletter_state.stats.cliches_list.length > 0){
      var clicheStrategy = getClicheStrategy(coverletter_state.stats.cliches_list);
      decorators.push({
          strategy: clicheStrategy,
          component: ClicheComponent
      });
    }

    if(coverletter_state.stats.too_wordy_list && coverletter_state.stats.too_wordy_list.length > 0){
      var wordyStrategy = getWordyStrategy(coverletter_state.stats.too_wordy_list)
      decorators.push({
        strategy: wordyStrategy,
        component: WordyComponent
      });
    }
  }

  return decorators;
}

function mapStateToProps(state) {
    return {
      error: state.coverletter.error,
      stats: state.coverletter.stats,
      text: state.coverletter.text,
      title: state.coverletter.title,
      decorators: getDecorators(state.coverletter)
    };
}

function mapDispatchToProps(dispatch) {
    return bindActionCreators(actionCreators, dispatch);
}

@connect(mapStateToProps, mapDispatchToProps)
class cvEditor extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
          editorState: EditorState.createEmpty(),
          text: '',
          title: '',
          stats: null,
          error: null,
          old_cliches_list: null
        }
    }

    focus = () => {
      this.refs.editor.focus();
    }

    onChange = (editorState) => {

      this.setState({
        editorState: editorState,
      });

      var nextText = editorState.getCurrentContent().getPlainText('\n\n')
      if(this.props.text !== nextText && nextText !== ""){

        this.props.setCoverLetterText(nextText);

        var that = this;
        this.props.fetchCoverLetterStats(nextText, (error) => {

          if(error) {
            console.log(this.props.error);
            this.props.clearCoverLetterStats();
          } else {
            const updatedDecorators = new CompositeDecorator(that.props.decorators);
            if(that.state.old_cliches_list && that.props.stats.cliches_list && that.state.old_cliches_list.length !== that.props.stats.cliches_list.length || (that.props.stats.cliches_list && !that.state.old_cliches_list) ){
              that.setState({
                old_cliches_list: that.props.stats.cliches_list,
                editorState:  EditorState.set(that.state.editorState, {decorator: updatedDecorators})
              });
            }
          }
        });
      } else {
        if(nextText === "" && this.props.stats){
          this.props.clearCoverLetterStats();
        }
      }
    }

    render() {
        return (
            <div style={styles.root} className="row">
              {this.props.stats &&
              <div className="col-xs-12 red">
                <span>Did you get an interview with this cover letter?</span>
                <div className="btn">Yes</div>
                <div className="btn">No</div>
              </div>
              }
              <div className="col-md-9">
                <input className="titleInput" type="text" placeholder="Title of your cover letter"/>
              </div>
              <div className="col-md-9 editor-wrapper">
                <Editor
                  editorState={this.state.editorState}
                  onChange={this.onChange}
                  placeholder="Write your coverletter here..."
                  ref="editor"
                />
              </div>
              {this.props.stats &&
              <div style={styles.sidebar} className="col-md-3 sidebar">

                {this.props.stats.outcome &&
                  <h2>Outcome: {this.props.stats.outcome} </h2>
                }
                <h4>Strengths</h4>
                <ul className='strengths'>
                  {this.props.stats.valid_word_count &&
                    <li>
                      <span>
                        Length is just about right
                      </span>
                    </li>
                  }

                  {this.props.stats.active_verb_percentage > 0.875 &&
                    <li>
                      <span>
                        Strong use of active verbs
                      </span>
                    </li>
                  }

                  {this.props.stats.positivity > 0.6 &&
                    <li>
                      <span>
                        Has a positive tone
                      </span>
                    </li>
                  }

                  {this.props.stats.action_word_percentage > 0.05 && this.props.stats.action_word_percentage < 0.20 &&
                    <li>
                      <span>
                        Number of action words is just right
                      </span>
                    </li>
                  }

                  {this.props.stats.adjective_percentage < 0.09 &&
                    <li>
                      <span>
                        Appropriate use of adjectives
                      </span>
                    </li>
                  }
                </ul>
                <br/>

                <h4>Warnings</h4>
                <ul className='warnings'>
                  {this.props.stats.adjective_percentage >= 0.10 && this.props.stats.adjective_percentage <= 0.15 &&
                    <li>
                      <span>
                        Could use less adjectives
                      </span>
                    </li>
                  }

                  {this.props.stats.active_verb_percentage >= 0.70 && this.props.stats.active_verb_percentage <= 0.875 &&
                    <li>
                      <span>
                        Could use more active verbs
                      </span>
                    </li>
                  }

                  {this.props.stats.cliches_score > 0 && this.props.stats.cliches_score <= 4 &&
                    <li>
                      <span>
                        Has a couple corporate cliches
                      </span>
                    </li>
                  }

                  {this.props.stats.positivity > 0.4 && this.props.stats.positivity < 0.6 &&
                    <li>
                      <span>
                        Has a neutral tone
                      </span>
                    </li>
                  }
                </ul>

                <br/>

                <h4>Problems</h4>
                <ul className='problems'>

                  { this.props.stats.contains_offensive_words != 0 &&
                    <li>
                      <span>
                        Contains {this.props.stats.contains_offensive_words.length} offensive words
                      </span>
                    </li>
                  }

                  { this.props.stats.spelling_mistakes_score != 0 &&
                    <li>
                      <span>
                      Your cover letter has {this.props.stats.spelling_mistakes_score} spelling mistakes
                      </span>
                    </li>
                  }

                  { !this.props.stats.sentence_length &&
                    <li>
                      <span>
                        Sentence length is not optimal
                      </span>
                    </li>
                  }

                  { !this.props.stats.valid_word_count &&
                    <li>
                      <span>
                        Length is not optimal
                      </span>
                    </li>
                  }

                  { !this.props.stats.has_contact_details &&
                    <li>
                      <span>
                        Does not include your contact details
                      </span>
                    </li>
                  }

                  { !this.props.stats.has_greeting &&
                    <li>
                      <span>
                        Missing greeting/salutation
                      </span>
                    </li>
                  }

                  { !this.props.stats.has_signature &&
                    <li>
                      <span>
                        Missing signature after closing
                      </span>
                    </li>
                  }

                  { this.props.stats.active_verb_percentage < 0.70 &&
                    <li>
                      <span>
                        Weak use of active verbs.
                      </span>
                    </li>
                  }

                  { this.props.stats.positivity < 0.4 &&
                    <li>
                      <span>
                        Has a negative tone
                      </span>
                    </li>
                  }

                  { this.props.stats.acronym_entity_percentage > 0.15 &&
                    <li>
                      <span>
                        Has too many acronyms
                      </span>
                    </li>
                  }

                  { this.props.stats.action_word_percentage > 0.20 &&
                    <li>
                      <span>
                        Has too many action words
                      </span>
                    </li>
                  }

                  { this.props.stats.action_word_percentage < 0.05 &&
                    <li>
                      <span>
                        Has too few action words.
                      </span>
                    </li>
                  }

                  { this.props.stats.cliches_score > 4 &&
                    <li>
                      <span>
                        Uses far too many Corporate Cliches
                      </span>
                    </li>
                  }

                  { this.props.stats.too_wordy_score &&
                    <li>
                      <span>
                        Contains too many overly-wordy phrases/words
                      </span>
                    </li>
                  }

                  { this.props.stats.adjective_percentage >= 0.10 &&
                    <li>
                      <span>
                        Has too many adjectives
                      </span>
                    </li>
                  }
                </ul>
              </div>
              }
              {!this.props.stats && !this.props.error &&
              <div style={styles.sidebarEmpty} className="col-md-3 sidebar">
                <h4 style={styles.sidebarHelpText}>CoverletterIO QuickStart</h4>
                <p>
                  Paste in your existing coverletter or simply just start writing to begin.
                </p>
              </div>
              }

              {!this.props.stats && this.props.error == 'serverError' &&
              <div style={styles.sidebarEmpty} className="col-md-3 sidebar">
                <h4 style={styles.sidebarHelpText}>Can't Connect to Server</h4>
                <p>
                  <strong>Uh oh!</strong> We are having problems connecting to our server. Until we can reconnect we won't be able to help you improve your listing.
                </p>
              </div>
              }

              {!this.props.stats && this.props.error == 'needMoreText' &&
              <div style={styles.sidebarEmpty} className="col-md-3 sidebar">
                <h4 style={styles.sidebarHelpText}>Keep Typing!</h4>
                <p>
                  CoverletterIO can help improve your coverletter as soon as you have at least two paragraphs written.
                </p>
              </div>
              }
            </div>
        );
    }
}

const styles = {
  popOver: {
    display: 'block'
  },
  root: {
    paddingTop: 40,
    paddingLeft: 60
  },
  sidebarEmpty: {
    color: 'rgb(108, 105, 106)',
    fontWeight: 300,
    fontSize: '15px',
    borderLeft: '1px solid grey',
    padding: '100 27 64 27'
  },
  sidebar: {
    color: 'rgb(108, 105, 106)',
    fontWeight: 300,
    fontSize: '15px',
    borderLeft: '1px solid grey',
    padding: '0 27 64 27'
  },
  problemDecorator: {
    backgroundColor: '#FFCE8B',
    borderColor: '#FFCE8B',
    cursor: 'pointer'
  },
  problemPopover: {
    padding: '10px 20px',
    minWidth: 150,
    maxWidth: 300,
    borderTop: '5px #4CAF50 solid'
  },
  neutralDecorator: {
    backgroundColor: '#e8e8e8',
    borderColor: '#e8e8e8',
    cursor: 'pointer'
  },
  neutralPopover: {
    padding: '10px 20px',
    maxWidth: 150,
    borderTop: '5px #a8a8a8 solid'
  },
  sidebarHelpText: {
    fontSize: 18,
    fontWeight: 400
  }
};

export default cvEditor;