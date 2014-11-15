require('./app.css');
var React = require('react');
var View = require('./components/view.react');

module.exports = {
  init: function() {
    if (!window.React) {
      window.React = React; // for React dev tools
    }

    React.render(<View />, document.body);
  }
};
