/* eslint-env node */

const TerserPlugin = require("terser-webpack-plugin");

const production = process.env.ENVIRONMENT !== "devel";

// turn on terser plugin on production
const minimizer = production
  ? [
      new TerserPlugin({
        sourceMap: true,
      }),
    ]
  : [];

module.exports = {
  entry: {
    "global-nav": "./static/js/global-nav.js",
    base: "./static/js/base.js",
  },
  output: {
    filename: "[name].js",
    path: __dirname + "/static/js/dist",
  },
  mode: production ? "production" : "development",
  devtool: production ? "source-map" : "eval-source-map",
  module: {
    rules: [
      {
        test: /\.js$/,
        // Exclude node_modules from using babel-loader
        // except some that use ES6 modules and need to be transpiled:
        // such as swiper http://idangero.us/swiper/get-started/
        // and also react-dnd related
        exclude: /node_modules\/(?!(dom7|ssr-window)\/).*/,
        use: {
          loader: "babel-loader",
        },
      },
      // loaders are evaluated from bottom to top (right to left)
      // so first transpile via babel, then expose as global
      {
        test: require.resolve(__dirname + "/static/js/base.js"),
        use: ["expose-loader?dqlite.base", "babel-loader"],
      },
    ],
  },
  optimization: {
    minimize: true,
    minimizer,
  },
};
