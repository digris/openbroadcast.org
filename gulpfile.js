'use strict';

var gulp = require('gulp');
var $ = require('gulp-load-plugins')();
var browserSync = require('browser-sync').create();

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
        port: 3000,
        host: 'local.openbroadcast.org',
        open: false,
        proxy: {
            target: "127.0.0.1:" + 8080
        },
        ui: {
            port: 3000 + 1
        }
    });
    gulp.watch("website/site-static/sass/**/*.sass", ['styles']);
});

gulp.task('styles', function () {
    return gulp.src([
            'website/site-static/sass/screen.sass',
            'website/site-static/sass/print.sass',
            'website/site-static/sass/aplayer.sass',
            'website/site-static/sass/scheduler.sass',
            'website/site-static/sass/admin.sass'
        ])
        .pipe($.sourcemaps.init())
        .pipe($.sass({
            precision: 10
        }))
        .pipe($.autoprefixer({browsers: AUTOPREFIXER_BROWSERS}))
        .pipe($.sourcemaps.write())
        .pipe(gulp.dest('website/site-static/css/'))
        .pipe(browserSync.stream({match: '**/*.css'}))
        .pipe($.size({title: 'styles'}));
});


gulp.task('default', ['proxy']);
gulp.task('watch', ['proxy']);
