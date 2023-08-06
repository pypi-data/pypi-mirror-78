
import json

bound = {
    0: 'in',
    1: 'out',
    2: 'unknown'
}

runlevel = {
    0: "absent",
    1: "connecting",
    2: "online",
    3: "shutdown",
    4: "error"
}


def get_bound(b):
  return bound[b]

def get_runlevel(level):
  return runlevel[level]



def parse_connections(conns):

  for con in conns:
    con['bound'] = get_bound(con['bound'])
    con['runlevel'] = get_runlevel(con['runlevel'])
  return conns


def parse_gateways(raw):
  connections = raw['connections']
  listeners = raw['listeners']
  
  if len(connections) > 0:
    connections = parse_connections(connections)
    pass

  if len(listeners) > 0:
    #listeners = parse_listeners(listeners)
    pass

  return connections, listeners






