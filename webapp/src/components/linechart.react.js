var React = require('react');
var Read = require('../data/read');
var d3 = require('d3');

module.exports = React.createClass({
    propTypes: {
      values: React.PropTypes.array.isRequired,
      xAxisLabel: React.PropTypes.string,
      yAxisLabel: React.PropTypes.string,
      addQualityCls: React.PropTypes.bool
    },

  render: function() {
    return <div ref="chart" className="stats-container linechart"></div>;
  },

  componentDidMount: function() {
    this.renderChart();
  },

  renderChart: function() {
    var data = this.props.values;

    var margin = {top: 10, right: 10, bottom: 40, left: 50},
        width = 215,
        height = 180;

    var x = d3.scale.linear()
      .domain([0, d3.max(data, function(d) {return d.x;})])
      .range([0, width]);

    var y = d3.scale.linear()
        .domain([d3.min(data, function(d) { return d.y; }), d3.max(data, function(d) { return d.y; })])
        .range([height, 0]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

    var lineFunction = d3.svg.line()
      .x(function(d) { return x(d.x); })
      .y(function(d) { return y(d.y); })
      .interpolate("linear");

    var svg = d3.select(this.refs.chart.getDOMNode()).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var line = svg.append("path")
      .attr("d", lineFunction(data))
      .attr("class", "stroke-generic");

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis);

    svg.append("text")
      .attr("class", "x label")
      .attr("text-anchor", "middle")
      .attr("x", width / 2)
      .attr("y", height + 38)
      .text(this.props.xAxisLabel);

    svg.append("text")
        .attr("class", "y label")
        .attr("text-anchor", "middle")
        .attr("y", -35)
        .attr("x", height / -2)
        .attr("transform", "rotate(-90)")
        .text(this.props.yAxisLabel);
  }
});
