var _ = require('lodash');
var React = require('react');
var Histogram = require('./histogram.react');
var LineChart = require('./linechart.react');
var SequenceSelector = require('./sequenceSelector.react');
var SequenceDetail = require('./sequenceDetail.react');
var Read = require('../data/read');

module.exports = React.createClass({
  getInitialState: function() {
    var seqs = Read.getRead();

    return {
      sequences: seqs,
      selectedSequence: seqs[0]
    };
  },

  render: function() {
    return <div className="content">
        <div className="row row-eq-height sequence-stats">
          <div className="col-xs-12 col-md-6 col-lg-4"><Histogram values={ this.getBpQualityScores() }
                                                                  xAxisLabel="quality score"
                                                                  yAxisLabel="bp count"
                                                                  addQualityCls={ true }
                                                                  width={ 300 } /></div>
          <div className="col-xs-12 col-md-6 col-lg-4"><Histogram values={ this.getReadQualityScores() }
                                                                  xAxisLabel="avg. quality score"
                                                                  yAxisLabel="read count"
                                                                  addQualityCls={ true }
                                                                  width={ 300 } /></div>
          <div className="col-xs-12 col-md-6 col-lg-4"><Histogram values={ this.getReadLengths() }
                                                                  xAxisLabel="read length"
                                                                  yAxisLabel="read count"
                                                                  width={ 300 } /></div>
        </div>
        <div className="row row-eq-height sequence-display">
          <div className="col-xs-4"><SequenceSelector sequences={ this.state.sequences }
                                                      selectedSequence={ this.state.selectedSequence }
                                                      onItemClick={ this.onItemClick }/></div>
          <div className="col-xs-8 content-col"><SequenceDetail sequence={ this.state.selectedSequence }
                                                                onNextClick={ this.onNextClick }/></div>
        </div>
      </div>;
  },

  getBpQualityScores: function() {
    return _.reduce(this.state.sequences, function(result, seq) {
      return result.concat(seq.qualityScores);
    }, []);
  },

  getReadQualityScores: function() {
    return _.map(this.state.sequences, function(seq) {return seq.averageQuality;});
  },

  getReadLengths: function() {
    return _.map(this.state.sequences, function(seq) {return seq.sequence.length;});
  },

  onItemClick: function(seq) {
    this.setState({
      selectedSequence: seq
    });
  },

  onNextClick: function(seq) {
    var seqIdx = _.findIndex(this.state.sequences, {id: seq.id});
    this.setState({
      selectedSequence: this.state.sequences[seqIdx + 1]
    });
  }
});
