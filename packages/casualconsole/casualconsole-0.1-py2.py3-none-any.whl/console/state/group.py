
import json

def get_group_members(groups, servers, executables):
  for group in groups:
    if 'membercount' not in group:
      group['membercount'] = 0
      group['server_members'] = []
      group['executable_members'] = []
    for server in servers:
      if group['id'] in server['memberships']:
        group['membercount'] += 1
        group['server_members'].append(server)
    for server in executables:
      if group['id'] in server['memberships']:
        group['membercount'] += 1
        group['executable_members'].append(server)

  return groups

def get_group_dependencies(group, groups):
  group['group_dependencies'] = []
  for g in groups:
    if g['id'] in group['dependencies']:
      group['group_dependencies'].append(g)
 
  return group
def parse_group(group,groups, servers, executables):
  
  group = get_group_members([group], servers, executables)[0]
  group = get_group_dependencies(group, groups)


  
  return group

def get_group_by_name(groups, name):
  group = None
  for group in groups:
    if group['name'] == name: 
      return group


def parse_group_by_name(groups,servers, executables, name):

  group = get_group_by_name(groups, name)
  if group is not None:
    group = get_group_members([group], servers, executables)[0]
    group = get_group_dependencies(group, groups)
  
  return group
  

