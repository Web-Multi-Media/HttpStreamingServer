const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  entry: path.join(__dirname, 'src/js/index'),
  output: {
    path: path.join(__dirname, '../app/StreamServerApp/static/dist'),
    filename: '[name]-[hash].js',
  },
  plugins: [
    new BundleTracker({
      path: __dirname,
      filename: 'webpack-stats.json',
    }),
  ],
};
