var gulp = require('gulp');
var browserify = require('browserify');
var babelify = require("babelify");
var uglify = require('gulp-uglify');
var glob  = require('glob');
var es = require('event-stream');
var source = require('vinyl-source-stream');
var rename = require('gulp-rename');

function basename(path) {
   return path.split(/[\\/]/).pop();
}

gulp.task('js', function(done){
  glob('./lid/static/src/js/**.js', function(err, files) {
    var tasks = files.map(function(entry) {
      return browserify({ entries: [entry] })
        .transform(babelify.configure({
          presets: ["env","react"]
        }))
        .bundle()
        .pipe(source(entry))
        .pipe(rename(basename(entry)))
        .pipe(gulp.dest('./lid/static/js'));
    });
    es.merge(tasks).on('end', done);
  })
});

gulp.task('default', [ 'js' ]);