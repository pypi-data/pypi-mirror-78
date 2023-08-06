from dataclasses import dataclass
import json

from Crypto.PublicKey import RSA
from arrow import get as _, now
from typing import Union, List
from jose import jwt


ListOrDict = Union[dict, list]


@dataclass
class TokenHeaders:
    kid: Union[int, str] = "no-kid-provided"
    extra_headers: dict = None

    def as_dict(self) -> dict:
        headers = self.extra_headers or {}

        headers.update({"kid": self.kid})

        return headers

    def __str__(self) -> str:
        return json.dumps(self.as_dict(), indent=4)


@dataclass
class Payload:
    """Payload interface"""

    # Testing constants
    DEFAULT_SCOPE = "email profile openid"
    PERMISSION = []
    DEFAULT_AUD = "https://testing.provider.com/"
    DEFAULT_GTY = "client-credentials"
    DEFAULT_ISS = "https://testing.com/service"

    __epoch__ = _("1970-01-01")
    __now__ = now()

    scope: str = DEFAULT_SCOPE
    permissions: List[str] = None
    expiration_minutes: int = 24 * 60  # Token expires in 1 day.
    aud: str = DEFAULT_AUD
    iss: str = DEFAULT_ISS
    gty: str = DEFAULT_GTY

    extra_claim: dict = None

    @property
    def iat(self) -> int:
        return round((self.__now__ - self.__epoch__).total_seconds())

    @property
    def exp(self) -> int:
        _n = self.__now__
        return round((_n.shift(minutes=self.expiration_minutes) - self.__epoch__).total_seconds())

    def as_dict(self) -> dict:
        permissions = ",".join(self.permissions or [])
        claims = {
            "scope": self.scope,
            "permissions": permissions,
            "iss": self.iss,
            "aud": self.aud,
            "iat": self.iat,
            "exp": self.exp,
            "gty": self.gty,
        }
        claims.update(self.extra_claim or {})

        return claims

    def __str__(self) -> str:
        return json.dumps(self.as_dict(), indent=4)


@dataclass
class TokenFabrik:
    pk_bits: int = 1024
    private_key: str = None
    public_key = None

    headers: dict = None
    payload: dict = None
    algorithm: str = "RS256"
    permission: list = None
    extra_claims: dict = None
    auth_header_key_name = "Authorization"

    __token__ = None

    @staticmethod
    def build_token(payload: ListOrDict, rsa_id: str, algorithm: str, headers: dict):

        return jwt.encode(
            payload,
            key=rsa_id,
            algorithm=algorithm,
            headers=headers,
        )

    def __initialize_headers__(self):

        headers = self.headers or {}

        self.headers = TokenHeaders(**headers).as_dict()

    def __initialize_payload__(self):

        payload = self.payload or {}
        self.payload = Payload(permissions=self.permission, extra_claim=self.extra_claims, **payload).as_dict()

    def __initialize_private_key__(self) -> str:
        """Load or create PrivateKey and PublicKey"""

        if not self.private_key:
            rsa_key = RSA.generate(bits=self.pk_bits)
        else:
            if not isinstance(self.private_key, str):
                raise TypeError
            rsa_key = RSA.importKey(self.private_key)

        self.private_key = rsa_key.export_key().decode()
        self.public_key = rsa_key.publickey().exportKey('PEM')

        return self.private_key

    def initialize(self):

        self.__initialize_private_key__()
        self.__initialize_headers__()
        self.__initialize_payload__()

    def __post_init__(self):
        self.initialize()

    def authorization_header(self) -> dict:

        return {self.auth_header_key_name: self.bearer}

    @property
    def bearer(self):

        return f"Bearer {self.token}"

    @property
    def token(self):

        if not self.__token__:
            self.__token__ = self.build_token(payload=self.payload, headers=self.headers,
                                              rsa_id=self.private_key,
                                              algorithm=self.algorithm)
        return self.__token__


"""
# Tutorial I: Dame un token!

En este tutorial vamos a ver como rapidamente podemos hacernos con un JWT utilizando el modulo **TokenFabrik**

```python
from tokko_auth.future.testing import TokenFabrik

token_fabric = TokenFabrik()

print(token_fabric.token)
```

## Results

### Token
```
eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Im5vLWtpZC1wcm92aWRlZCJ9.
eyJzY29wZSI6ImVtYWlsIHByb2ZpbGUgb3BlbmlkIiwicGVybWlzc2lvbnMiOiIiLCJpc
3MiOiJodHRwczovL3Rlc3RpbmcuY29tL3NlcnZpY2UiLCJhdWQiOiJodHRwczovL3Rlc3
RpbmcucHJvdmlkZXIuY29tLyIsImlhdCI6MTU4NzY4MjYwMSwiZXhwIjoxNTg3NzY5MDA
xLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMifQ.gXa5-T3azYOXAWShV2l8unQj6plLD
yrrZZevWwfIsb8eDdYBJLu08jS5fcH7rTtXUMxRd3HNHhQFMkTNJJyZnZ5_uYE54rZZRd
2C3EsgjU_0em6KFIFnPF-WraQuzgWQ8xiOmzzpdUiv6UYQLrBXkGQlQnk-pQuyC8Y_3MK
b0qQ
```

_Nota Importante:_ JTW de ejemplo. El JWT contiene fechas en su interior y por muy posiblemente, el token
generado no sea ESTRICTAMENTE igual al expuesto.

### Headers

```
{
  "typ": "JWT",
  "alg": "RS256",
  "kid": "no-kid-provided"
}
```

### Payload

```
{
  "scope": "email profile openid",
  "permissions": "",
  "iss": "https://testing.com/service",
  "aud": "https://testing.provider.com/",
  "iat": 1587682601,
  "exp": 1587769001,
  "gty": "client-credentials"
}
```

---

# Tutorial II: Crear Tokens Customizados

**TokenFabrik** incluso permite la creacion de JWTs customizados. Es posible agregar nuevos
headers, nuevos claims, especificar permisos etc.


```python
from tokko_auth.future.testing import TokenFabrik

token_fabric = TokenFabrik(
    headers={
        "kid": "custom-key-id",
        "extra_headers":
            {
                "custom_header_01": "custom-value-01",
                "custom_header_02": "custom-value-02",
            }},
    extra_claims={
        "my-custom-claim": "custom-claim-value"
    },
    permission=[
        "namespace:action01",
        "namespace:action02",
        "namespace01:action01"
    ]
)
```

## Results

#### Token
```
eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImN1c3RvbV9oZWFkZXJfMDEiOiJjdXN0b20tdmFsdWUtMDEiLCJ
jdXN0b21faGVhZGVyXzAyIjoiY3VzdG9tLXZhbHVlLTAyIiwia2lkIjoiY3VzdG9tLWtleS1pZCJ9.eyJzY29wZ
SI6ImVtYWlsIHByb2ZpbGUgb3BlbmlkIiwicGVybWlzc2lvbnMiOiJuYW1lc3BhY2U6YWN0aW9uMDEsbmFtZXNw
YWNlOmFjdGlvbjAyLG5hbWVzcGFjZTAxOmFjdGlvbjAxIiwiaXNzIjoiaHR0cHM6Ly90ZXN0aW5nLmNvbS9zZXJ
2aWNlIiwiYXVkIjoiaHR0cHM6Ly90ZXN0aW5nLnByb3ZpZGVyLmNvbS8iLCJpYXQiOjE1ODc2ODE5ODgsImV4cC
I6MTU4Nzc2ODM4OCwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwibXktY3VzdG9tLWNsYWltIjoiY3VzdG9tL
WNsYWltLXZhbHVlIn0.nNLVS8VClhpHlV6ZjN31Z1TcZKuq9uPh5DY5J1ZvmwxMQBL2sLd2jqiGk0l0_7eesWiI
rd9EeLCYhEnHq6m_bRgI8Uyy7YXs5X3_0GfzVkSNPFxOhoxuj5ZP11uk77UZBWGa7Dcikux19tccsk-fnEJbQGA
dRPx-sbHpmrV1Wx8
```

_Nota Importante:_ JWT de ejemplo. El JWT contiene fechas en su interior y por muy posiblemente, el token
generado no sea ESTRICTAMENTE igual al expuesto.

#### Headers
```
{
  "typ": "JWT",
  "alg": "RS256",
  "custom_header_01": "custom-value-01",
  "custom_header_02": "custom-value-02",
  "kid": "custom-key-id"
}
```

#### Payload:
```
{
  "scope": "email profile openid",
  "permissions": "namespace:action01,namespace:action02,namespace01:action01",
  "iss": "https://testing.com/service",
  "aud": "https://testing.provider.com/",
  "iat": 1587681988,
  "exp": 1587768388,
  "gty": "client-credentials",
  "my-custom-claim": "custom-claim-value"
}
```
"""
