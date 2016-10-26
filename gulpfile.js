'use strict';

const gulp = require('gulp'),
    sass = require('gulp-sass'),
    shell = require('gulp-shell'),
    haml = require('gulp-haml'),
    del = require('del'),
    webp = require('imagemin-webp'),
    revertPath = require('gulp-revert-path'),
    rename = require("gulp-rename");

gulp.task('clean', function(){
    return del(['output/*']);
});

gulp.task('content', ['haml', 'misc-content']);
gulp.task('assets', ['sass', 'webp', 'misc-assets']);

gulp.task('misc-assets', ['clean'], function(){
    return gulp.src(['assets/**/*', '!assets/**/*.scss'])
        .pipe(gulp.dest('output/assets'));
});

gulp.task('webp', ['clean'], function(){
    return gulp.src(['assets/**/*.{jpeg,jpg,png}'])
        .pipe(webp()())
        .pipe(revertPath())
        .pipe(rename(function(p){
                p.extname += ".webp";
                return p;
            }))
        .pipe(gulp.dest('output/assets'));
});

gulp.task('misc-content', ['clean', 'assets'], function(){
    return gulp.src(['content/**/*', '!content/**/*.haml'])
        .pipe(gulp.dest('output'));
});

gulp.task('haml', ['clean', 'assets'], function(){
    return gulp.src('content/**/*.haml')
        .pipe(haml())
        .pipe(gulp.dest('output'));
});

gulp.task('sass', ['clean', 'misc-assets'], function (){
    return gulp.src('./assets/**/*.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('output/assets'));
});

gulp.task('watch', function (){
    gulp.watch(['assets/**/*', 'content/**/*'], ['content']);
});

gulp.task('default', ['all']);

gulp.task('all', ['content', 'assets']);

gulp.task('deploy', ['all'], function(){
    return gulp.src('output/')
        .pipe(shell([
            'rsync -ai --no-times --delete-after output/ slyme.codl.fr:/srv/http/www.codl.fr'
        ]));
});
