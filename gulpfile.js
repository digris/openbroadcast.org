'use strict';

var config = require('./settings.json');
var gulp = require('gulp');
var gutil = require('gulp-util');
var $ = require('gulp-load-plugins')();
var browserSync = require('browser-sync').create();
var sass = require('gulp-sass');

var AUTOPREFIXER_BROWSERS = [
  'ie >= 10',
  'ie_mob >= 10',
  'ff >= 30',
  'ff >= 30',
  'chrome >= 34',
  'safari >= 7',
  'opera >= 23',
  'ios >= 7',
  'android >= 4.4'
];

gulp.task('proxy', ['styles'], function () {

    browserSync.init({
        notify: false,
        port: config.local_port,
        host: config.hostname,
        //open: "external",
        open: false,
        proxy: {
            target: "127.0.0.1:" + config.proxy_port
        },
        ui: {
            port: config.local_port + 1,
            weinre: {
                port: config.local_port + 2
            }
        }
    });

    gulp.watch("website/site-static/sass/**/*.sass", ['styles']);
    gulp.watch("website/site-static/js/**/*.coffee", ['scripts']);
    //gulp.watch("website/**/*.html").on('change', browserSync.reload);
});

gulp.task('styles', function () {
    return gulp.src([
            'website/site-static/sass/screen.sass',
            'website/site-static/sass/print.sass',
            'website/site-static/sass/aplayer.sass',
            'website/site-static/sass/scheduler.sass',
            'website/site-static/sass/admin.sass'
            //'website/site-static/sass/wip.sass'
        ])
        .pipe($.sourcemaps.init())
        //.pipe($.plumber())
        .pipe($.sass({
            precision: 10
            //onError: logSASSError
        }))
        .pipe($.autoprefixer({browsers: AUTOPREFIXER_BROWSERS}))
        .pipe($.sourcemaps.write())
        .pipe(gulp.dest('website/site-static/css/'))
        .pipe(browserSync.stream({match: '**/*.css'}))
        .pipe($.size({title: 'styles'}));
});


//Concat and minify scripts
gulp.task('scripts', function() {
    return gulp.src([
          'website/site-static/js/**/*.coffee'
    ])
    .pipe($.coffee({bare: true}).on('error', gutil.log))
    .pipe(gulp.dest('website/site-static/dist/js/'));
});

gulp.task('default', ['proxy']);
gulp.task('watch', ['proxy']);

