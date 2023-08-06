from datetime import datetime
import base64, uuid

def epochtodate(nano):
  if(nano > 0):
    billion = 1000*1000*1000
    dt = datetime.fromtimestamp(nano).replace(microsecond=0)
    return dt
  else:
    return "-"

def base64_to_uuid(b64_input):
  try:
    bin_string = base64.b64decode(b64_input)
    guid = uuid.UUID(bytes=bin_string)
    guid = str(guid).replace('-', "")
  except Exception as e:
    guid = "unkown"
  return guid

def formatMicroSec(micro):
  return "{:6f}".format(micro)


def init_app(app):
  app.add_template_filter(epochtodate, 'epochToDate')
  app.add_template_filter(base64_to_uuid, 'base64ToUuid')
  app.add_template_filter(formatMicroSec, 'formatMicroSec')


