'use strict';

var gulp = require('gulp'),
    sass = require('gulp-sass'),
    del = require('del');

gulp.task('clean', function(){
    return del(['output/*']);
});

gulp.task('content', ['misc-content']);
gulp.task('assets', ['sass', 'misc-assets']);

gulp.task('misc-assets', function(){
    return gulp.src(['assets/**/*', '!assets/**/*.scss'])
        .pipe(gulp.dest('output'));
});

gulp.task('misc-content', function(){
    return gulp.src('content/**/*')
        .pipe(gulp.dest('output'));
});

gulp.task('sass', function (){
    return gulp.src('./assets/**/*.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('output'));
});

gulp.task('watch', function (){
    gulp.watch('./assets/**/*.scss', ['sass']);
    gulp.watch('./content/**/*', ['misc-content']);
    gulp.watch(['assets/**/*', '!assets/**/*.scss'], ['misc-assets']);
});

gulp.task('default', ['clean'], function(){
gulp.start('content', 'assets');
});
