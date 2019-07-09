var path = require("path");
var webpack = require("webpack");
var BundleTracker = require("webpack-bundle-tracker");
var MiniCssExtractPlugin = require('mini-css-extract-plugin');

var vendorPath = path.join(__dirname, "static/js/vendor/");

module.exports = {
  context: __dirname,
  resolve: {
    modules: [
      vendorPath,
      path.join(__dirname, "node_modules"),
      path.join(__dirname, "static/js/")
    ]
  },
  entry: {
    vendor: ["leaflet", "jquery", "slick-carousel"],
    app: "./static/js/app"
  },

  output: {
    path: path.resolve("static/build/"),
    filename: "[name].js"
  },

  plugins: [
    new BundleTracker({ filename: "./webpack-stats.json" }),
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery"
    }),
    new MiniCssExtractPlugin({
      filename: "[name].css",
      allChunks: true
    })
  ],
  devtool: "eval-source-map",
  module: {
    rules: [
      {
        test: /\.scss$/,
        use: [
          "style-loader", // creates style nodes from JS strings
          "css-loader", // translates CSS into CommonJS
          "sass-loader" // compiles Sass to CSS, using Node Sass by default
        ]
      },
      {
        test: /\.css(\?v=\d+\.\d+\.\d+)?$/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
            query: { sourceMap: true }
          },
          'css-loader'
        ]
      },
      {
        test: /\.(png|gif|jpe?g|svg|ttf|eot|ico|pdf)(\?v=\d+\.\d+\.\d+)?$/i,
        loader: "file-loader?name=[name].[ext],limit=1000"
      },
      {
        test: /\.html(\?v=\d+\.\d+\.\d+)?$/i,
        loader: "html-loader"
      },
      {
        test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
        loader: "url-loader?limit=10000&minetype=application/font-woff"
      }
    ]
  }
};
