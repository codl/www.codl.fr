'use strict';

var gulp = require('gulp'),
    sass = require('gulp-sass'),
    shell = require('gulp-shell'),
    haml = require('gulp-haml'),
    del = require('del');

gulp.task('clean', function(){
    return del(['output/*']);
});

gulp.task('content', ['haml', 'misc-content']);
gulp.task('assets', ['sass', 'misc-assets']);

gulp.task('misc-assets', function(){
    return gulp.src(['assets/**/*', '!assets/**/*.scss'])
        .pipe(gulp.dest('output'));
});

gulp.task('misc-content', function(){
    return gulp.src(['content/**/*', '!content/**/*.haml'])
        .pipe(gulp.dest('output'));
});

gulp.task('haml', function(){
    return gulp.src('content/**/*.haml')
        .pipe(haml())
        .pipe(gulp.dest('output'));
});

gulp.task('sass', function (){
    return gulp.src('./assets/**/*.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('output'));
});

gulp.task('watch', function (){
    gulp.watch('./content/**/*', ['content']);
    gulp.watch('assets/**/*', ['assets']);
});

gulp.task('default', ['clean-then-all']);

gulp.task('all', ['content', 'assets']);

gulp.task('clean-then-all', ['clean'], function(){
    return gulp.start('all');
});

gulp.task('deploy', ['clean-then-all'], function(){
    return gulp.src('output/')
        .pipe(shell([
            'rsync -ai --delete-after output/ ana.codl.fr:/srv/www.codl.fr'
        ]));
});
