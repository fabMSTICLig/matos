const BundleAnalyzerPlugin = require("webpack-bundle-analyzer")
  .BundleAnalyzerPlugin;

module.exports = {
  publicPath: "/static/",
  configureWebpack: {
    plugins: [new BundleAnalyzerPlugin()],
    optimization: {
      splitChunks: {
        minSize: 10000,
        maxSize: 250000,
        chunks: "all"
      }
    }
  },
  chainWebpack: config => {
    config.plugins.delete("prefetch");
  }
};
