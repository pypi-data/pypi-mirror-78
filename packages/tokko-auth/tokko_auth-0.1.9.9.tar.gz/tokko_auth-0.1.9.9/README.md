TokkoAuth
---


# Install
```bash
# Install from PyPi
pip install tokko-auth
# Install from sources
# Tokko REPO Permission is required
pip install -e git@github.com:TokkoLabs/authorization.git
```

## Import & Configure dj-plugin
_your-project/settings.py_
```bash
# Add app to installed apps
INSTALLED_APPS = [
    'tokko_auth'
]

# Also declare app's middleware
MIDDLEWARE = [
    # Has request JWT?
    "tokko_auth.middleware.HasJWTMiddleware",
    # JWT has required NAMESPACE?
    "tokko_auth.middleware.NamespaceAuthorizationMiddleware",
    # Fill "request.user" attribute
    "tokko_auth.middleware.UserRecoverMiddleware",
]

# Finally, declare your AUTH0_DOMAIN
AUTH0_DOMAIN = 'my-auth-sub-dns.auth0.com'
```

## Tools (Future)
future.tools.permission

### Users
Retrieve user permissions

```python
from tokko_auth.future.tools.permissions import PermissionProvider

# Provider Initialization
provider = PermissionProvider()
# Retrieve user permission
provider.users.get("user@email.com")
```

Response:
```
{
    "user_id": "user@email.com",
    "permissions": [
        "namespace_a:action_1",
        "namespace_b:action_1",
        "namespace_a:action_2"
    ]
}
```

## Grant user permission
```python
from tokko_auth.future.tools.permissions import PermissionProvider

# Provider Initialization
provider = PermissionProvider()
# Grant permission
provider.users.grant("user@email.com", "namespace-is-required", "action-is-required")
```

Response:
```
{
  "success": true
}
```

## Revoke user permission
```python
from tokko_auth.future.tools.permissions import PermissionProvider

# Provider Initialization
provider = PermissionProvider()
# Grant permission
provider.users.revoke("user@email.com", "namespace-is-required", "action-is-required")
```

Response:
```
{
  "success": true
}
```

## Permissions
List permission
```python
from tokko_auth.future.tools.permissions import PermissionProvider

# Provider Initialization
provider = PermissionProvider()
# Create permission
provider.permissions.list()
# List permissions method also allows filter permissions
# by namespace or action partial
# provider.permissions.list(partial="nam")
# provider.permissions.list(partial="act")
```

Response:
```
[{
    "namespace": "namespace",
    "action": "action",
    "permission": "namespace:action",
    "description": "description"
}]
```

Create permission
```python
from tokko_auth.future.tools.permissions import PermissionProvider

# Provider Initialization
provider = PermissionProvider()
# Create permission
provider.permissions.add("namespace-is-required",
                         "action-is-required",
                         "description-argument-is-optional")
```

Response:
```
{
    "namespace": "namespace-is-required",
    "action": "action-is-required",
    "permission": "namespace-is-required:action-is-required",
    "description": "description-argument-is-optional"
}
```

Delete permission
```python
from tokko_auth.future.tools.permissions import PermissionProvider

# Provider Initialization
provider = PermissionProvider()
# Delete permission
provider.permissions.delete("namespace-is-required", "action-is-required")
```

Response:
```
{
  "success": true
}
```

## Testing
### Local environment

#### Unit Test
    python manage.py test authorization.tests.unit
#### Service Test
    python manage.py test authorization.tests.service


### Docker environment
Unit Test

    # Require: docker-compose up [-d] [--build]
    docker-compose exec app bash -c "python manage.py test authorization.tests.unit"


Service Test

    # Require: docker-compose up [-d] [--build]
    docker-compose exec app bash -c "python manage.py test authorization.tests.service"

