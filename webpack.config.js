require("@babel/polyfill");

const webpack = require('webpack');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const StyleLintPlugin = require('stylelint-webpack-plugin');
const path = require('path');

const DEV_MODE = process.env.NODE_ENV !== 'production';

// pints to static source folder, un project root
const STATIC_SRC = path.resolve(__dirname, 'obp_ui');

// points to STATIC_ROOT configured in django
const STATIC_ROOT = path.resolve(__dirname, 'build', 'static');

// must be the same as WEBPACK_DEVSERVER_HEADER
const DEVSERVER_HEADER = 'X-WEBPACK-DEVSERVER';

// dev-server behind a proxy (devsupport/compose.yml): bundle & hmr socket are
// reached through the proxy's port instead of directly on :3000
const PUBLIC_PATH = process.env.WEBPACK_PUBLIC_PATH || 'http://localhost:3000/static/js/';
const SOCK_PORT = process.env.WEBPACK_SOCK_PORT;
const PROXY_TARGET = process.env.WEBPACK_PROXY_TARGET || 'http://127.0.0.1:5000';
// polling - file events from bind mounts are not reliable everywhere
const WATCH_POLL = process.env.WEBPACK_WATCH_POLL ? parseInt(process.env.WEBPACK_WATCH_POLL, 10) : false;

module.exports = {
  entry: {
    bundle: [
      '@babel/polyfill',
      './obp_ui/js/bundle.js',
    ],

  },
  // entry: './obp_ui/js/bundle.js',
  output: {
    path: DEV_MODE ? path.resolve(STATIC_ROOT, 'js') : path.resolve(STATIC_ROOT, 'dist', 'js'),
    filename: '[name].js',
    publicPath: PUBLIC_PATH,
  },
  devtool: 'source-map',
  module: {
    rules: [
      {
        enforce: 'pre',
        test: /\.(js|vue)$/,
        // loader: 'eslint-loader',
        exclude: [
          /node_modules/,
        ]
      },
      /**/
      {
        test: /\.js$/,
        exclude: [/node_modules/],
        use: {
          loader: 'babel-loader',
        }
      },
      {
        test: /\.vue$/,
        use: {
          loader: 'vue-loader',
          options: {
            includePaths: ['./obp_ui/js/'],
          },
        }
      },
      {
        test: /\.scss$/,
        // test: /\.(scss|sass)$/,
        use: [
          DEV_MODE ? 'vue-style-loader' : MiniCssExtractPlugin.loader,
          // 'vue-style-loader',
          'css-loader',
          'sass-loader',
          {
            loader: 'sass-resources-loader',
            options: {
              resources: [
                './obp_ui/style/abstracts/*.scss',
              ]
            },
          },
        ]
      },
      {
        test: /\.css$/,
        use: [
          'vue-style-loader',
          'css-loader'
        ]
      },

      {
        test: /\.sass$/,
        use: [
          DEV_MODE ? 'style-loader' : MiniCssExtractPlugin.loader,
          {
            loader: "css-loader",
            options: {
              sourceMap: DEV_MODE,
            }
          },
          {
            loader: 'sass-loader',
            options: {
              // sassOptions: {
              //   indentedSyntax: true,
              // },
              sourceMap: DEV_MODE,
              // includePaths: ['./node_modules'],
              // query: {
              //   includePaths: [
              //     path.resolve(__dirname, 'node_modules')
              //   ]
              // }
            },
          },
          {
            loader: 'postcss-loader',
          }
        ]
      },
      {
        test: /\.font\.js/,
        use: [
          DEV_MODE ? 'style-loader' : MiniCssExtractPlugin.loader,
          'css-loader',
          {
            loader: 'webfonts-loader',
            options: {},
          }
        ]
      },
      {
        test: /\.(png|svg|jpg|gif|woff|woff2|eot|ttf)$/,
        use: [
          'file-loader'
        ]
      }
    ]
  },
  plugins: [
    new webpack.HotModuleReplacementPlugin(),
    new MiniCssExtractPlugin({
      // this is relative to output.path
      filename: '../css/[name].css',
    }),
    new CopyWebpackPlugin([
      {
        from: path.resolve(STATIC_SRC, 'font'),
        to: path.resolve(STATIC_ROOT, 'font')
      },
      {
        from: path.resolve(STATIC_SRC, 'img'),
        to: path.resolve(STATIC_ROOT, 'img')
      },
      {
        from: path.resolve(STATIC_SRC, 'icons'),
        to: path.resolve(STATIC_ROOT, 'icons')
      }
    ], {debug: 'warn'}),
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery"
    }),
    new VueLoaderPlugin(),
    new StyleLintPlugin({
      files: [
        './obp_ui/js/**/*.vue',
        './obp_ui/style/**/*.scss',
      ],
    })
  ],
  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js', // 'vue/dist/vue.common.js' for webpack 1
      src: path.resolve(__dirname, 'obp_ui/js/'),
      style: path.resolve(__dirname, 'obp_ui/style/'),
    },
  },
  devServer: {
    hot: true,
    inline: true,
    port: 3000,
    compress: true,
    disableHostCheck: true,
    //host: 'obp-next.local',
    host: '0.0.0.0',
    ...(SOCK_PORT ? {sockPort: SOCK_PORT} : {}),
    ...(WATCH_POLL ? {watchOptions: {poll: WATCH_POLL}} : {}),
    headers: {
      'Access-Control-Allow-Origin': '*'
    },
    proxy: {
      '/': {
        target: PROXY_TARGET,
        onProxyReq: proxyReq => {
          proxyReq.setHeader(DEVSERVER_HEADER, 'on');
        }
      },

    }
  }
};
