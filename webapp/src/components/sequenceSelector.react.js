var _ = require('lodash');
var React = require('react');
var SequenceSummary = require('./sequenceSummary.react');

module.exports = React.createClass({
    propTypes: {
      sequences: React.PropTypes.array.isRequired,
      selectedSequence: React.PropTypes.object,
      onItemClick: React.PropTypes.func
    },

  render: function() {
    var seqs = _.map(this.props.sequences, function(seq, idx) {
      return <SequenceSummary key={ 'seq-' + idx }
                              sequence={ seq }
                              selected={ this.props.selectedSequence && this.props.selectedSequence.id === seq.id }
                              onItemClick={ this.props.onItemClick } />;
    }, this);

    return <div className="sequence-selector-container">{ seqs }</div>;
  }
});
