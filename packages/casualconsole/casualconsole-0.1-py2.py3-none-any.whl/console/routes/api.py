from flask import request, Blueprint, make_response, jsonify, session


import console.state.information as info
import console.state.update as update

b_api = Blueprint("b_api", __name__)


@b_api.route("/console/api/v1/server/environment/set", methods=["POST"])
def set_environment():
    envs = request.get_json()
    #print(json.dumps(envs))
    varis = {}
    varis['variables'] = []
    for env in envs['variables']:
        varis['variables'].append(dict(key=env['key'], value=env['value']))
    varis['alias'] = envs['alias']
    setenv = update.set_env(varis)

    return make_response("", 204)

@b_api.route("/console/api/v1/server/environment/get", methods=["GET"])
def get_environment():

    alias = request.args.get('alias', default=None)
    server_type = request.args.get('type', default=None)
    if server_type == 'server':
      server = info.get_server_by_alias(alias)
      env = server['environment_variables']
    elif server_type == 'executable':
      executable = info.get_executable_by_alias(alias)
      env = executable['environment_variables']
    # print(server)
    return jsonify({"env": env})


@b_api.before_request
def is_logged_in():
  if 'logged_in_user' in session:
    pass
  else:
    return make_response("", 401)