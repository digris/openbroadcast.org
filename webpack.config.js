/* === dont forget to import scss to main.js file === */

const webpack = require('webpack');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const path = require('path');

const DEV_MODE = process.env.NODE_ENV !== 'production';

// points to STATIC_ROOT configured in django
const STATIC_ROOT = path.resolve(__dirname, 'website', 'static-src');

// pints to static source folder, un project root
const STATIC_SRC = path.resolve(__dirname, 'static');

// must be the same as WEBPACK_DEVSERVER_HEADER
const DEVSERVER_HEADER = 'X-WEBPACK-DEVSERVER';

module.exports = {
    entry: './static/js/bundle.js',
    output: {
        path: DEV_MODE ? path.resolve(STATIC_ROOT, 'js') : path.resolve(STATIC_ROOT, 'dist', 'js'),
        filename: "bundle.js",
        publicPath: 'http://localhost:3000/static/js/'
    },
    devtool: 'source-map',
    module: {
        rules: [
            {
                test: /\.js$/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: [
                            'env'
                        ]
                    }
                }
            },
            {
                test: /\.vue$/,
                use: {
                    loader: 'vue-loader',
                    options: {
                        includePaths: ['./static/js/'],
                    },
                }
            },
            {
                test: /\.sass$/,
                use: [
                    DEV_MODE ? 'style-loader' : MiniCssExtractPlugin.loader,
                    {
                        loader: "css-loader",
                        options: {
                            sourceMap: true
                        }
                    },
                    {
                        loader: 'sass-loader',
                        options: {
                            sourceMap: true,
                            includePaths: ['./node_modules'],
                            query: {
                                includePaths: [
                                    path.resolve(__dirname, 'node_modules')
                                ]
                            }
                        },
                    },
                    {
                        loader: 'postcss-loader',
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
            filename: '../css/bundle.css'
        }),
        new CopyWebpackPlugin([
            {
                from: path.resolve(STATIC_SRC, 'font'),
                to: path.resolve(STATIC_ROOT, 'font')
            },
            {
                from: path.resolve(STATIC_SRC, 'img'),
                to: path.resolve(STATIC_ROOT, 'img')
            }
        ], {debug: 'info'}),
        new webpack.ProvidePlugin({
            $: "jquery",
            jQuery: "jquery"
        })
    ],
    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.esm.js' // 'vue/dist/vue.common.js' for webpack
        }
    },
    devServer: {
        hot: true,
        inline: true,
        port: 3000,
        compress: true,
        disableHostCheck: true,
        host: 'local.openbroadcast.org',
        headers: {
            'Access-Control-Allow-Origin': '*'
        },
        proxy: {
            '/': {
                target: 'http://127.0.0.1:8080',
                onProxyReq: proxyReq => {
                    // add header to let django know about getting a devserver request
                    proxyReq.setHeader(DEVSERVER_HEADER, 'on');
                }
            },

        }

    }
};