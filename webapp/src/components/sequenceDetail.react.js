var _ = require('lodash');
var React = require('react');
var SequenceSummary = require('./sequenceSummary.react');
var Read = require('../data/read');

module.exports = React.createClass({
    propTypes: {
      sequence: React.PropTypes.object,
      onNextClick: React.PropTypes.func
    },

  render: function() {
    var seq = this.props.sequence;

    if (!seq) {
      return <div className="sequence-detail blank-slate">Select a sequence read.</div>;
    }

    var bases = _.map(seq.sequence.split(''), function(base, idx) {
      var qual = seq.qualityScores[idx];
      var baseCls = Read.getQualityDescriptor(qual);
      var tooltip = 'base: ' + base +
        '\nposition: ' + (idx + 1) +
        '\nquality score: ' + qual +
        '\nquality code: ' + seq.qualityCode[idx];
      return <span key={ 'base-' + idx } className={ baseCls } title={ tooltip }>{ base }</span>;
    }, this);

    return <div className="sequence-detail">
      <SequenceSummary sequence={ this.props.sequence } />
      <p className="sequence-text">{ bases }</p>
      <button onClick={ this.onClick }>Next Read<span className="glyphicon glyphicon-chevron-right" aria-hidden="true"></span></button>
    </div>;
  },

  onClick: function(event) {
    if (this.props.onNextClick) {
      this.props.onNextClick(this.props.sequence);
    }
  }
});
