import console.routes.views as views
import console.routes.api as api
from console.routes.open import b_open



def get_routes():
  return views.b_routes, api.b_api, b_open
