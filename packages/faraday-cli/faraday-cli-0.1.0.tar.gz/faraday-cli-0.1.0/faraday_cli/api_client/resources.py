from simple_rest_client.resource import Resource


class LoginResource(Resource):
    actions = {
        "auth": {"method": "POST", "url": "login"},
        "get_token": {"method": "GET", "url": "v2/token/"},
        "validate": {"method": "GET", "url": "v2/preferences/"},
    }


class WorkspaceResource(Resource):
    actions = {
        "list": {"method": "GET", "url": "v2/ws/"},
        "get": {"method": "GET", "url": "v2/ws/{}/"},
        "create": {"method": "POST", "url": "v2/ws/"},
        "delete": {"method": "DELETE", "url": "v2/ws/{}/"},
    }


class BulkCreateResource(Resource):
    actions = {"create": {"method": "POST", "url": "v2/ws/{}/bulk_create/"}}


class HostResource(Resource):
    actions = {
        "list": {"method": "GET", "url": "v2/ws/{}/hosts/"},
        "get": {"method": "GET", "url": "v2/ws/{}/hosts/{}/"},
        "create": {"method": "POST", "url": "v2/ws/{}/hosts/"},
        "delete": {"method": "DELETE", "url": "v2/ws/{}/hosts/{}/"},
        "get_services": {
            "method": "GET",
            "url": "v2/ws/{}/hosts/{}/services/",
        },
        "get_vulns": {"method": "GET", "url": "v2/ws/{}/vulns/"},
    }


class ServiceResource(Resource):
    actions = {"get": {"method": "GET", "url": "v2/ws/{}/services/{}/"}}


class CredentialResource(Resource):
    actions = {
        "list": {"method": "GET", "url": "v2/ws/{}/credential/"},
    }


class AgentResource(Resource):
    actions = {
        "list": {"method": "GET", "url": "v2/ws/{}/agents/"},
        "get": {"method": "GET", "url": "v2/ws/{}/agents/{}/"},
        "run": {"method": "POST", "url": "v2/ws/{}/agents/{}/run/"},
    }
