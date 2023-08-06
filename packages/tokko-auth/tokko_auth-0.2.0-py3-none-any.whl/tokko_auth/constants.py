from os import environ


# Error codes
UNAUTHORIZED = 401
INTERNAL_ERROR = 500
GATEWAY_ERROR = 503

# AVAILABLE STRATEGIES
AUTH0 = 'auth0'
COGNITO = 'aws-cognito'

AUTH_STRATEGY = COGNITO

ALGORITHMS = environ.get("TOKKO_AUTH_ALGORITHMS",
                         # Pre deprecation support
                         environ.get("ALGORITHMS"))

API_AUDIENCE = environ.get("TOKKO_AUTH_API_AUDIENCE",
                           # Pre deprecation support
                           environ.get("API_AUDIENCE"))

AUTH_DOMAIN = environ.get("TOKKO_AUTH_PROVIDER_DOMAIN",
                          # Pre deprecation support
                          environ.get("AUTH0_DOMAIN"))
