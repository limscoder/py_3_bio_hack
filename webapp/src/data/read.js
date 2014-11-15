var _ = require('lodash');
var rawRead = require('./rawRead.fastq');
var parsedRead;

var buildRead = function(id, sequence, qualityCode) {
  var qualScores = _.map(qualityCode.split(''), function(char) {
    return char.charCodeAt(0) - 33;
  });
  var lowQualCount = 0;
  var qualSum = _.reduce(qualScores, function(result, score) {
    if (score < 25) {
      lowQualCount++;
    }
    return result + score;
  }, 0);
  var avgQual = qualSum / qualScores.length;
  var idParts = id.split(' ')[0].split(':');

  return {
    id: id,
    runId: idParts.slice(0, 3).join(':'),
    cellId: idParts.slice(3, 7).join(':'),
    sequence: sequence,
    qualityCode: qualityCode,
    qualityScores: qualScores,
    averageQuality: avgQual,
    lowQualityCount: lowQualCount,
    qualityDescriptor: module.exports.getQualityDescriptor(avgQual)
  };
};

module.exports = {
  getRead: function() {
    if (!parsedRead) {
      parsedRead = [];

      for (var idx = 0; idx < rawRead.length; idx += 4) {
        parsedRead.push(buildRead(rawRead[idx], rawRead[idx + 1], rawRead[idx + 3]));
      }
    }

    return parsedRead;
  },

  getQualityDescriptor: function(score) {
    if (score > 35) {
      return 'very-good-score';
    } else if (score > 30) {
      return 'good-score';
    } else if (score > 25) {
      return 'acceptable-score';
    } else if (score > 20) {
      return 'poor-score';
    } else if (score > 15) {
      return 'very-poor-score';
    }

    return 'unreliable-score';
  }
};
