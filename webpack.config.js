var path = require("path")
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')
var ExtractTextPlugin = require("extract-text-webpack-plugin");

var vendorPath = path.join(__dirname, "./disasterinfosite/static/js/vendor/");

module.exports = {
  context: __dirname,
  resolve: {
    modules: [
      vendorPath,
      path.join(__dirname, 'node_modules'),
      path.join(__dirname, "./disasterinfosite/static/js/")
    ],
  },
  entry: {
    vendor: ["foundation.min", "modernizr", "leaflet", "jquery", "slick-carousel"],
    app: './disasterinfosite/static/js/app'
  },

  output: {
      path: path.resolve('./disasterinfosite/static/build/'),
      filename: "[name].js",
  },

  plugins: [
    new BundleTracker({filename: './webpack-stats.json'}),
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery",
      L: "leaflet"
    }),
    new webpack.optimize.CommonsChunkPlugin({
      name: "vendor",
      minChunks: Infinity,
    }),
    new ExtractTextPlugin({
      filename: "[name].css",
      allChunks: true
    }),
    new webpack.optimize.UglifyJsPlugin({
        compress: {
            warnings: false
        }
    })
  ],
  devtool: 'eval-source-map',
  module: {
    loaders: [
    {
      test: /\.css(\?v=\d+\.\d+\.\d+)?$/,
      loader: ExtractTextPlugin.extract({fallback: "style-loader", use: "css-loader"})
    },
    {
      test: /\.(png|gif|jpe?g|svg)(\?v=\d+\.\d+\.\d+)?$/i,
      loader: "url-loader?name=[name].[ext],limit=1000"
    },{
      test: /\.html(\?v=\d+\.\d+\.\d+)?$/i,
      loader: 'html-loader'
    }]
  }
}
