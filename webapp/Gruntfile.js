var webpack = require('webpack');

module.exports = function(grunt) {
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-jsxhint');
  grunt.loadNpmTasks('grunt-webpack');

  grunt.initConfig({
    jshint: {
      options: {
        node: true,
        browser: true,
        esnext: true,
        indent: 2
      },
      all: {
        src: ['src/**/*.js']
      }
    },

    clean: ['dist/*'],

    copy: {
      html: {
        flatten: true,
        expand: true,
        src: ['src/app.html'],
        dest: 'dist/sequence/'
      },
      bootstrapCss: {
        flatten: true,
        expand: true,
        src: ['node_modules/bootstrap/dist/css/*'],
        dest: 'dist/sequence/lib/bootstrap/css'
      },
      bootstrapFonts: {
        flatten: true,
        expand: true,
        src: ['node_modules/bootstrap/dist/fonts/*'],
        dest: 'dist/sequence/lib/bootstrap/fonts'
      },
      bootstrapJs: {
        flatten: true,
        expand: true,
        src: ['node_modules/bootstrap/dist/js/*'],
        dest: 'dist/sequence/lib/bootstrap/js'
      }
    },

    watch: {
      app: {
        files: ['src/**/*'],
        tasks: ['webpack']
      }
    },

    webpack: {
      sequence: {
        context: __dirname,

        entry: {
          app: './src/app.react.js'
        },

        output: {
          publicPath: '',
          path: 'dist/sequence/js',
          sourceMapFilename: 'dist/sequence/js/app.source.map',
          filename: 'app.js',
          library: 'app',
          libraryTarget: 'var'
        },

        debug: false,
        devtool: 'source-map',

        stats: {
          colors: true,
          reasons: false
        },

        resolve: {
          modulesDirectories: ['src', 'node_modules'],
          extensions: ['', '.js', '.css']
        },

        module: {
          loaders: [
            {
              test: /\.react.js/,
              loader: "jsx-loader?harmony=true"
            },
            {
              test: /\.css$/,
              loader: "style-loader!css-loader"
            }
          ]
        },

        plugins: [
          new webpack.optimize.DedupePlugin(),
          new webpack.optimize.OccurenceOrderPlugin(true),
          new webpack.optimize.AggressiveMergingPlugin()
        ]
      }
    }
  });

  grunt.registerTask('build', 'Build code ready for the browser.', ['clean', 'jshint', 'copy', 'webpack']);
};
