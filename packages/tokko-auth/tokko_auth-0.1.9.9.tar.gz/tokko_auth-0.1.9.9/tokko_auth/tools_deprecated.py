from typing import Callable, Union, Any, Dict
from dataclasses import dataclass, field
from os import environ as env

from requests.exceptions import (ConnectionError, TooManyRedirects, HTTPError, ConnectTimeout)
from jose.exceptions import JWTError
from jose import jwt
import requests

from tokko_auth.exceptions import (
    TokenNotFound,
    MustBeBearerToken,
    MustStartWithBearer,
    ProviderUnreachable,
    UnableDecodeToken,
    TokenIsExpired,
    IncorrectClaims,
    ProviderHttpError
)
from tokko_auth.constants import AUTH0, COGNITO

AUTH_STRATEGY = COGNITO


def _cognito_jwk_strategy() -> str:
    region = env.get("AWS_COGNITO_REGION")
    pool_id = env.get("AWS_COGNITO_USERS_POOL_ID")

    return f"https://cognito-idp.{region}.amazonaws.com/{pool_id}/.well-known/jwks.json"


def _auth0_jwk_strategy() -> str:
    auth_domain = env.get("AUTH0_DOMAIN")

    return f"https://{auth_domain}/.well-known/jwks.json"


STRATEGIES: Dict[str, Callable] = {
    AUTH0: _auth0_jwk_strategy,
    COGNITO: _cognito_jwk_strategy,
}


def build_jwk_url(strategy: str = AUTH_STRATEGY) -> str:
    try:

        if not isinstance(strategy, str):
            raise TypeError("Unsupported strategy type")

        _jwk_url = STRATEGIES[strategy]

        if callable(_jwk_url):
            _jwk_url = _jwk_url()

        return _jwk_url

    except KeyError:
        raise KeyError("Unsupported Build JWK strategy")


def get_jwk(jwk_url) -> dict:
    try:
        r = requests.get(jwk_url)

        if not r.status_code == 200:
            r.raise_for_status()

        content_type = r.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            raise ProviderHttpError(description=f"Invalid content type. {content_type} is not supported",
                                    status_code=500)

        _jwk = r.json()

        return _jwk

    except (ConnectionError, TooManyRedirects, ConnectTimeout) as e:
        # It is connected?
        raise IOError(f"Transport error. {e}")
    except HTTPError as e:
        raise IOError(f"Protocol Error. {e}")


def default_issuer_strategy(token: str, **options):
    _jwk_url = options.get("jwk_url")
    _algorithms = options.get("algorithms")
    _audience = options.get("audience")

    if not all([_jwk_url, _audience, _algorithms]):
        raise KeyError("ISSUER, ALGORITHMS & AUDIENCE are required arguments")

    try:
        jwks = get_jwk(_jwk_url)
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=_algorithms,
                    audience=_audience,
                )
                return payload
            except jwt.ExpiredSignatureError:
                raise TokenIsExpired
            except jwt.JWTClaimsError as e:
                print(e)
                raise IncorrectClaims
            except Exception:
                raise UnableDecodeToken
        raise KeyError("Required key not found")
    except (ConnectionError, ConnectTimeout, HTTPError):
        raise ProviderUnreachable
    except JWTError:
        raise UnableDecodeToken
    except KeyError:
        raise KeyError("Required key not found")


def default_permission_strategy(token: str):
    ...


def get_auth_token_from_headers(key_name: str = "Authorization", **headers) -> Union[str, None]:
    """
    Returns Auth token from headers
    ===
    """
    auth = headers.get(key_name)

    # Syntactic Token validations
    if not auth:
        raise TokenNotFound

    parts = auth.split()

    if len(parts) == 1 or len(parts) > 2:
        raise MustBeBearerToken

    # Semantic Token validations
    if not parts[0].lower() == "bearer":
        raise MustStartWithBearer

    return parts[1]


@dataclass(init=True)
class PassportChecker:
    jwk_url: Union[Callable, str]

    strategy_kwargs: Dict[str, Any] = field(default_factory=lambda: {})
    jwk_url_kwargs: Dict[str, Any] = field(default_factory=lambda: {})
    auto_init: bool = True
    token: str = ""

    JWT_ISSUER = 'issuer'
    JWT_PERMISSION = 'permissions'

    AVAILABLE_STRATEGIES = {
        JWT_ISSUER: default_issuer_strategy,
        JWT_PERMISSION: lambda: 1
    }

    def get_jwk_url(self) -> str:

        _jwk_url = self.jwk_url

        if not _jwk_url:
            raise ValueError

        if callable(_jwk_url):
            return _jwk_url(self.token, **self.jwk_url_kwargs)

        elif isinstance(_jwk_url, str):
            return _jwk_url

        raise TypeError

    def approve_or_deny(self, token=None, strategy=JWT_ISSUER):

        if strategy not in self.AVAILABLE_STRATEGIES.keys():
            raise KeyError

        _strategy_callable = self.AVAILABLE_STRATEGIES[strategy]

        token = token or self.token

        if not token:
            raise ValueError

        self.strategy_kwargs.update({
            "jwk_url": self.jwk_url
        })

        _strategy_callable(token, **self.strategy_kwargs)

        return {
            "is_valid": True,
            "message": "Token seems valid",
            "token": self.token
        }

    def __post_init__(self):
        if self.auto_init:
            self.approve_or_deny()
