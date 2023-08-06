import sys
from flask import render_template, Flask, request, Response, jsonify, make_response
from flask import Blueprint, redirect, session, url_for, flash
import json


import console.state.information as info
import console.state.update as update

import console.routes.api as api

b_routes = Blueprint("b_routes", __name__)


@b_routes.route("/")
def console():
    return render_template('console.html')


@b_routes.route("/servers")
def servers():
    servers = info.get_servers()
    return render_template('particles/server/servers.html', servers=servers)


@b_routes.route("/servers/server")
def get_server():
    try:
        alias = request.args.get('alias', default=None)
        tab = request.args.get('tab', default='conf')
        if tab == '':
            tab = 'conf'

        server = info.get_server_by_alias(alias)

        return render_template("particles/server/server.html", server=server, tabs=[dict(title='Configuration', short='conf'), dict(title='Environment', short='env'), dict(title='Services', short='serv'), dict(title='Member of', short="mem")], activeTab=tab)
    except Exception as e:
        return render_template("particles/errors/server_error.html")


@b_routes.route("/executables")
def get_executables():
    executables = info.get_executables()

    return render_template('particles/server/executables.html', executables=executables)


@b_routes.route("/executables/executable")
def get_executable():
    alias = request.args.get('alias', default=None)
    tab = request.args.get('tab', default='conf')
    if tab == '':
        tab = 'conf'
    executable = info.get_executable_by_alias(alias)

    return render_template('particles/server/executable.html', server=executable, tabs=[dict(title='Configuration', short='conf'), dict(title='Environment', short='env'), dict(title='Member of', short="mem")], activeTab=tab)


@b_routes.route("/groups")
def groups():
    try:
        groups = info.get_groups()
        return render_template('particles/group/groups.html', groups=groups)
    except Exception as e:
        return render_template('particles/errors/groups_error.html')


@b_routes.route("/groups/group")
def get_group():
    name = request.args.get('name', default=None)
    # print(name)
    group = info.get_group_by_name(name)

    return render_template("particles/group/group.html", group=group)


@b_routes.route("/services")
def get_services():
    try:
        page = int(request.args.get('page', default=1))
        category_filter = request.args.get('category', default='all')
        max_rows = int(request.args.get('rows', default=10))
        filters = [page, category_filter, max_rows]
        services = info.get_services(filters)

        return render_template("particles/service/services.html", services=services[0]['services'], categories=services[1], pages=services[0]['pages'], total=services[2])
    except Exception as e:
        return render_template("particles/errors/services_error.html", error=e)


@b_routes.route("/services/service")
def get_service():
    try:
        name = request.args.get('name', default=None)
        service = info.get_service_by_name(name)
        return render_template("particles/service/service.html", service=service)
    except Exception as e:
        return render_template("particles/errors/service_error.html")


@b_routes.route("/gateways")
def get_gateways():
    try:
        gateways = info.get_gateways()
        return render_template("particles/gateway/gateways.html", connections=gateways[0], listeners=gateways[1])
    except Exception as e:
        return render_template("500.html", error=e)

@b_routes.route("/transactions")
def get_transactions():
    transactions = info.get_transactions()
    try:
        template = render_template(
            "particles/transaction/transactions.html", transactions=transactions)

        return template
    except Exception as e:
        return render_template("500.html", error=e)



@b_routes.route("/ajaxtest", methods=["POST","GET"])
def ajax_test():

    return "My Response brings all the boys to the yard"

@b_routes.before_request
def check_before_test():
    pass
@b_routes.before_request
def check_cookies():
  session['collapsed'] = request.cookies.get('collapsed')


@b_routes.before_request
def is_logged_in():
  if 'logged_in_user' not in session:
    return redirect(url_for("b_open.login_view"))

@b_routes.context_processor
def inject_stuff():
  def check_collapsed(collapse = True):
    coll = False
    if 'collapsed' in session:
      coll = session.get('collapsed')
    else:
      session['collapsed'] = collapse
      coll = collapse
    return True if coll == 'true' else False


  collapsed = check_collapsed()
  return dict(collapse=collapsed)


def get_blueprints():
    return b_routes, api.b_api