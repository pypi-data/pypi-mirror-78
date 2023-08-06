from flask import Flask, render_template, jsonify, session, request, Response, send_from_directory

from flask_cors import CORS
from os import getenv, environ, path
from flask_assets import Environment, Bundle
from console.assets.assets import bundles

import console.utils as utils
import mimetypes

import console.state.information as info

mimetypes.add_type('image/svg+xml', '.svg')

import console.routes.routes as routes




def get_casual_version():
  version = info.casual_version()
  return dict(casual_version=version)

def create_app():
  app = Flask(__name__, template_folder='templates', static_folder='static')
  config_setup = getenv("CONFIGURATION_SETUP", None)

  if config_setup is not None:
    app.config.from_object(config_setup)
  else:
    app.config.from_object("console.config.config.ProductionConfig")

  utils.init_app(app)

  app.context_processor(get_casual_version)
  assets = Environment(app)
  assets.register(bundles)
  for route in routes.get_routes():
    app.register_blueprint(route)


  #app.config['SECRET_KEY'] = getenv('SECRET_KEY') or 'IU43IUN34+34-34F34VDsdfkj456'

  @app.route("/favicon.ico")
  def favicon():
    return send_from_directory(path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

  @app.route("/test")
  def hello():
    print("testing session")
    #print(session.cookie)
    if 'visits' in session:
      session['visits'] = session.get('visits') + 1
    else:
      session['visits'] = 1
    return "Total visits: {}".format(session.get('visits'))
  
  return app
