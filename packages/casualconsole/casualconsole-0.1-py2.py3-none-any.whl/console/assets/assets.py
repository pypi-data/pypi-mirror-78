from flask_assets import Bundle
import glob

#scss_files = glob.glob("scss/**/*.scss")

bundles = {
    'casual_css': Bundle(
        'scss/casual.scss',
        filters='libsass',
        depends=('scss/**/**/*.scss', 'scss/**/*.scss'),
        output='gen/casual.css',
    ),
    'lib_js': Bundle(
        'js/lib/jquery-3.5.0.min.js', 'js/lib/jquery-cookie-1.4.1.min.js',
        filters='jsmin', output='gen/lib.js'
    ),
    'casual_js': Bundle(
        'js/casual/casual.js', 'js/casual/server.js',
        filters='jsmin', output='gen/casual.js'
    ),
}

