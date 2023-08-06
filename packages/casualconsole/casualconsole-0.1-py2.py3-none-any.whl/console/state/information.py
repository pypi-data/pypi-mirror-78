import casual.server.api as api
import json
import console.state.server as server_info 
import console.state.group as group_info
import console.state.service as service_info
import console.state.gateway as gateway_info
import console.state.transaction as transaction_info


def get_domain():
  domain_service = ".casual/domain/state"
  domain = api.call(domain_service, "")
  dict_domain = json.loads(domain)
  result = dict_domain['result']
  return result


def get_member_of(servers, groups):
  for server in servers:
    server['memberof'] = []
    for group in groups:
      if group['id'] in server['memberships']:
        server['memberof'].append(group)
  return servers


def get_servers():
  try:
    domain = get_domain()

    groups = domain['groups']
    servers = domain['servers']
    servers = get_member_of(servers, groups)
    return servers
  except Exception as e:
    print(e)

def get_server_by_alias(alias):
  try:
    servers = get_servers()
    services = get_all_services()
    servers = server_info.parse_environment(servers)
    server = server_info.parse_server_by_alias(servers,services, alias)
    return server
  except Exception as e:
    print(e)
    

def get_executables():
  domain = get_domain()
  groups = domain['groups']
  executables = domain['executables']
  executables = get_member_of(executables, groups)
  return executables

def get_executable_by_alias(alias):
  executables = get_executables()
  executables = server_info.parse_environment(executables)

  executable = server_info.parse_executable_by_alias(executables, alias)
  return executable

def get_groups():
  try:
    domain = get_domain()
    groups = domain['groups']
    servers = domain['servers']
    executables = domain['executables']
    
    servers = get_member_of(servers, groups)
    executables = get_member_of(executables, groups)

    groups = group_info.get_group_members(groups, servers, executables)
    
    return groups

  except Exception as e:
    print(e)

def get_group_by_name(name):
  try:
    domain = get_domain()
    servers = domain['servers']
    executables = domain['executables']
    groups = domain['groups']
    group = group_info.parse_group_by_name(groups, servers,executables,name)
    return group
  except Exception as e:
    print(e)

def get_all_services():
  casual_service = ".casual/service/state"
  services = api.call(casual_service, "")
  dict_services = json.loads(services)
  all_services = dict_services['result']['services']
  return all_services

def get_services(filters):
  
  all_services = []
  categories = []
  try:
    all_services = get_all_services()
    total_services = len(all_services)

    for service in all_services:
      if service['category'] not in categories:
        categories.append(service['category'])

    filtered_services = service_info.filter_services(all_services, filters)
    return filtered_services, categories, total_services
  except Exception as e:
    print(e)
    return {}, [], 0

def get_service_by_name(name):
  try:
    services = get_all_services()
    servers = get_servers()
    service = service_info.parse_service_by_name(services, servers, name)
    return service
  except Exception as e:
    print(e)


def get_gateways():
  casual_service = ".casual/gateway/state"
  response = api.call(casual_service, "")
  raw_gateways = json.loads(response)['result']
  gateways = gateway_info.parse_gateways(raw_gateways)
  return gateways

def get_transactions():
  casual_service = ".casual/transaction/state"
  response = api.call(casual_service, "")
  transactions = json.loads(response)['result']
  transactions = transaction_info.parse_transactions(transactions)
  return transactions

def casual_version():
  domain = get_domain()
  version = domain['version']['casual']
  return version

