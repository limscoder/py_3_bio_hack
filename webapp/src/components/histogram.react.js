var React = require('react');
var Read = require('../data/read');
var d3 = require('d3');

module.exports = React.createClass({
    propTypes: {
      values: React.PropTypes.array.isRequired,
      xAxisLabel: React.PropTypes.string,
      yAxisLabel: React.PropTypes.string,
      width: React.PropTypes.number,
      addQualityCls: React.PropTypes.bool
    },

  render: function() {
    return <div ref="chart" className="stats-container histogram"></div>;
  },

  componentDidMount: function() {
    this.renderChart();
  },

  renderChart: function() {
    var values = this.props.values;

    var margin = {top: 10, right: 10, bottom: 40, left: 20},
        width = this.props.width || 265,
        height = 180;

    var x = d3.scale.linear()
      .domain([0, d3.max(values)])
      .range([0, width]);

    var data = d3.layout.histogram()
        .bins(x.ticks(20))
        (values);

    var y = d3.scale.linear()
        .domain([0, d3.max(data, function(d) { return d.y; })])
        .range([height, 0]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var parent = this.refs.chart.getDOMNode();
    parent.innerHTML = '';
    var svg = d3.select(parent).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var bar = svg.selectAll(".bar")
        .data(data)
      .enter().append("g")
        .attr("class", "bar")
        .attr("transform", function(d) { return "translate(" + x(d.x) + "," + y(d.y) + ")"; });

    bar.append("rect")
        .attr("x", 1)
        .attr("width", x(data[0].dx) - 1)
        .attr("height", function(d) { return height - y(d.y); })
        .append('svg:title')
        .text(function(d) {return d.y;});

    if (this.props.addQualityCls) {
      bar.attr("class", function(d) {return Read.getQualityDescriptor(d.x);});
    } else {
      bar.attr("class", "fill-generic");
    }

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    svg.append("text")
      .attr("class", "x label")
      .attr("text-anchor", "middle")
      .attr("x", width / 2)
      .attr("y", height + 38)
      .text(this.props.xAxisLabel);

    svg.append("text")
        .attr("class", "y label")
        .attr("text-anchor", "middle")
        .attr("y", -5)
        .attr("x", height / -2)
        .attr("transform", "rotate(-90)")
        .text(this.props.yAxisLabel);
  }
});
