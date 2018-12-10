var gulp = require("gulp");
var sass = require("gulp-sass");
var sourcemaps = require("gulp-sourcemaps");
var browserSync = require("browser-sync").create();

var userInterfaceDir = "user_interface/";

var	sassPaths = [
			'node_modules',
		];

gulp.task('sass:dev', function() {
	return gulp.src([userInterfaceDir + 'src/scss/**/*.scss'])
		.pipe(sourcemaps.init())
    .pipe(sass({
      includePaths: sassPaths
    }).on('error', sass.logError))
		.pipe(sourcemaps.write('./maps'))
		.pipe(gulp.dest(userInterfaceDir + 'static/user_interface/css'))
    .pipe(browserSync.stream())
});

gulp.task("watch", function() {
  browserSync.init({
  	files: [userInterfaceDir + "templates/**/*.html"],
    proxy: "localhost:8000",
  });

  gulp.watch(userInterfaceDir + 'src/scss/**/*.scss', ['sass:dev']);
});

gulp.task("default", ["watch"]);