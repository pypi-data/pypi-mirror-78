
import json


def find_service_names(pid, services):
    names = []
    for service in services:
        for ins in service['instances']['sequential']:
            if pid == ins['pid']:
                names.append(service)
    return names

def get_server_services(server_instances, services):
    service_names = []
    for instances in server_instances:

        names = find_service_names(instances['handle']['pid'], services)
        service_names.extend(names)
    return service_names


def parse_server_by_alias(servers, services, alias):
    for server in servers:
        if server['alias'] == alias:
            server['server_services'] = get_server_services(
                server['instances'], services)
            return server

    return dict()


def parse_variable(var):
    envar = var.split("=")
    return dict(key=envar[0], value=envar[1])


def parse_environment(servers):
    for server in servers:
        env = server['environment']['variables']
        server['environment_variables'] = []
        for var in env:
            server['environment_variables'].append(parse_variable(var))
    return servers


def parse_executable_by_alias(executables, alias):
    for exe in executables:
        if exe['alias'] == alias:
            return exe

    return dict()
