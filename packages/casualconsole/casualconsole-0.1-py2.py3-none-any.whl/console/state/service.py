
import json
from datetime import datetime
from operator import itemgetter


def find_parent_server(service_instances, servers):
    for inst in service_instances:
        for server in servers:
            for instance in server['instances']:
                if instance['handle']['pid'] == inst['pid']:
                    return server['alias']
    return 'unknown'


def parse_service_by_name(services, servers, name):

    for service in services:
        if service['name'] == name:
            service['parent_server'] = find_parent_server(
                service['instances']['sequential'], servers)
            return service
    return dict()


def chunk_services(services, rows_per_page):

    for i in range(0, len(services), rows_per_page):
        yield services[i:i + rows_per_page]


def filter_services(all_services, filters):
    PAGE = 0
    CATEGORY = 1
    MAX_ROWS = 2
    rows_per_page = filters[MAX_ROWS]
    services = []
    pages = 0
    try:
        sorted_list = sorted(all_services, key=itemgetter('name'))

        if filters[CATEGORY] != 'all':
            for service in sorted_list:
                if service['category'] == filters[CATEGORY]:
                    services.append(service)
        else:
            services = sorted_list

        chunked_list = list(chunk_services(services, rows_per_page))
        
        if filters[PAGE] > 0:
            services = chunked_list[filters[PAGE]-1]
            pages = len(chunked_list)
        else:
            services = []
            
    except Exception as e:
        print(e)
        services = []

    return dict(services=services,pages=pages)



