'use strict';

var gulp = require('gulp'),
    sass = require('gulp-sass'),
    shell = require('gulp-shell'),
    haml = require('gulp-haml'),
    cachebust = new require('gulp-cachebust')(),
    del = require('del');

gulp.task('clean', function(){
    return del(['output/*']);
});

gulp.task('content', ['haml', 'misc-content']);
gulp.task('assets', ['sass', 'misc-assets']);

gulp.task('misc-assets', function(){
    return gulp.src(['assets/**/*', '!assets/**/*.scss'])
        .pipe(cachebust.resources())
        .pipe(gulp.dest('output/assets'));
});

gulp.task('misc-content', ['assets'], function(){
    return gulp.src(['content/**/*', '!content/**/*.haml'])
        .pipe(cachebust.references())
        .pipe(gulp.dest('output'));
});

gulp.task('haml', ['assets'], function(){
    return gulp.src('content/**/*.haml')
        .pipe(haml())
        .pipe(cachebust.references())
        .pipe(gulp.dest('output'));
});

gulp.task('sass', ['misc-assets'], function (){
    return gulp.src('./assets/**/*.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(cachebust.references())
        .pipe(cachebust.resources())
        .pipe(gulp.dest('output/assets'));
});

gulp.task('watch', function (){
    gulp.watch(['assets/**/*', 'content/**/*'], ['content']);
});

gulp.task('default', ['clean-then-all']);

gulp.task('all', ['content', 'assets']);

gulp.task('clean-then-all', ['clean'], function(){
    return gulp.start('all');
});

gulp.task('deploy', ['clean-then-all'], function(){
    return gulp.src('output/')
        .pipe(shell([
            'rsync -ai --no-times --delete-after output/ ana.codl.fr:/srv/www.codl.fr'
        ]));
});
