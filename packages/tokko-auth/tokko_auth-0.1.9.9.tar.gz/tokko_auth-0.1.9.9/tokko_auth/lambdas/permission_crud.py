from typing import Union, Dict, Any
from os import environ as env
import json

import boto3

PERMISSION_DYNAMO_TABLE_NAME = env.get("PERMISSION_DYNAMO_TABLE_NAME", "auth_permission")

# DynamoDB Initialization
# dynamo_db = boto3.resource("dynamodb")
# permission_table = dynamo_db.Table(PERMISSION_DYNAMO_TABLE_NAME)

dynamo_db = "ToDo"  # boto3.resource("dynamodb")
permission_table = "ToDo"  # dynamo_db.Table("")


# Utils
def make_params(verb, **qs_params):

    # Required Params
    pid = qs_params.get("pid")
    namespace = qs_params.get("namespace", "")
    action = qs_params.get("action", "")

    # Optional Params
    extra = qs_params.get("extra")
    filters = qs_params.get("filters")

    verb_params = {
        "POST": {"namespace": namespace, "action": action},
        "GET": {"pid": pid or '__all__', "filters": filters or {}},
        "PUT": {"pid": pid, "namespace": namespace, "action": action},
        "DELETE": {"pid": pid, "e": extra or {}},
    }

    try:

        return verb_params[verb]

    except KeyError:

        raise KeyError("Bad Request")


def make_response(status: int, body: Union[dict, list], **extras) -> Dict[str, Any]:

    headers = extras.get("headers", {})
    headers["content-Type"] = headers.get("Content-Type", "application/json")

    response = {
        "statusCode": status,
        "headers": headers,
        "body": json.dumps(body)
    }

    return response


# Permission CRUD
def create_permission(namespace: str = None, action: str = None):
    """

    DynamoDB Integration:
    ---

    required_fields = [namespace, action]

    if not all(required_fields):
        raise KeyError("NAMESPACE & ACTION fields are required.")

    try:
        permission_table.put_item(Item={
            "namespace": namespace,
            "action": action
        })

        return permission_table.get_item(Key={'namespace':{'S': namespace},
                                              'action':{'S': action}})
    except Exception as e:
        print(e)

        raise KeyError
    """
    required_fields = [namespace, action]

    if not all(required_fields):
        raise KeyError("NAMESPACE & ACTION fields are required.")

    return {
        "id": "new-object-id",
        "namespace": namespace,
        "action": action,
        "permission": f"{namespace}:{action}",
    }


def retrieve_permission(pid: str, **filters):
    """

    DynamoDB Integration:
    ---

    if not all(required_fields):
        raise KeyError("NAMESPACE & ACTION fields are required")

    try:
        if pid == '__all__':

            return permission_table.query(
                    Key=Key('namespace').between('A', 'Z')
                    ProjectionExpression="namespace, action"
                )
            .

        return permission_table.get_item(Key={"pid": {"S": pid}})

    except Exception as e:
        print(e)

        return []
    """
    if pid == '__all__':
        pid = "some-pid"

    return [{
        "pid": pid,
        "namespace": "test_namespace",
        "action": "test_action",
        "permission": "test_namespace:test_action",
    }]


def update_permission(pid: str = None, namespace: str = None, action: str = None):
    """

    DynamoDB Integration:
    ---

    if not pid:
        raise KeyError("PID argument is required.")

    try:
        _update_expression = ", ".join(f"SET {k} = :{k}" for k in perm_data.keys())
        _expression_attr_values = {f":{k}": v for k, v in perm_data.items()}

        permission_table.get_update(Key={"pid": {"S": pid}},
                                    updateExpression=_update_expression,
                                    expressionAttributeValues=_expression_attr_values)

        return permission_table.get_item(Key={"pid": {"S": pid}})

    except Exception as e:
        print(e)

        raise KeyError(e)
    """

    if not pid:
        raise KeyError("PID argument is required.")

    return {
        "pid": pid,
        "namespace": namespace or "not modified",
        "action": action or "not modified"
    }


def delete_permission(pid: str = None, **extra):
    """
    DynamoDB Integration:
    ---

    if not pid:
        raise KeyError("PID argument is required.")

    return permission_table.delete_item(Key={"pid": {"S": pid}})
    """

    if not pid:
        raise KeyError("PID argument is required.")

    return {
        "success": True,
    }


def lambda_handler(event, context):
    actions = {

        "POST": lambda namespace, action: create_permission(namespace, action),
        "GET": lambda pid, filters: retrieve_permission(pid, **filters),
        "PUT": lambda pid, namespace, action: update_permission(pid, namespace, action),
        "DELETE": lambda pid, **e: delete_permission(pid, **e),
    }

    action = event['httpMethod']
    qs_params = event.get("queryStringParameters") or {}

    try:

        status = 200
        body = actions[action](**make_params(action, qs_params))

    except KeyError as bad_request:

        status = 400
        body = {
            "message": f"Bad request. {bad_request}",
            "status": status,
        }

    except Exception as e:

        print(f"{e}. Action: {action}. QSParams: {qs_params}")
        status = 500

        body = {
            "message": f"Internal Error.",
            "status": status,
        }

    return make_response(status, body=body)

