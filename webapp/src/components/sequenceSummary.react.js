var React = require('react');

module.exports = React.createClass({
    propTypes: {
      sequence: React.PropTypes.object.isRequired,
      selected: React.PropTypes.bool,
      onItemClick: React.PropTypes.func
    },

  render: function() {
    var seq = this.props.sequence;
    var summaryCls = "sequence-summary" +
      (this.props.onItemClick ? ' clickable' : '') +
      (this.props.selected ? ' selected' : '');
    var qualityCls = "sequence-quality " + seq.qualityDescriptor;

    return <div className={ summaryCls } onClick={ this.onClick } title={ seq.id }>
      <div className={ qualityCls }></div>
      <div className="sequence-id">{ seq.runId } <span className="sequence-expander glyphicon glyphicon-chevron-right" aria-hidden="true"></span></div>
      <div className="sequence-id">{ seq.cellId }</div>
      <div className="sequence-description">
        { seq.sequence.length } bp with { seq.averageQuality.toFixed(1) } avg. quality
      </div>
      <div className="sequence-description">
        { ((seq.lowQualityCount / seq.sequence.length) * 100).toFixed(1) }% ({ seq.lowQualityCount }) poor quality base pairs
      </div>
    </div>;
  },

  onClick: function(event) {
    if (this.props.onItemClick) {
      this.props.onItemClick(this.props.sequence);
    }
  }
});
