import casual.server.api as api
import json
import server as server_info
import group as group_info


def create_dict():
    return { "environment": {
        "variables": {
            "files": [],
            "variables": []
        },
        "aliases": []
      }
    }

def get_input(env):
    body = create_dict()
    variables = dict()
    for e in env['variables']:
        body['environment']['variables']['variables'].append(
            dict(key=e['key'], value=e['value']))

    body['environment']['aliases'] = [env['alias']]

    return body


def set_env(env):
    service_name = ".casual/domain/environment/set"

    input = json.dumps(get_input(env))

    resp = api.call(service_name, input)

    return resp
