WELL_KNOWN_OPENID_CONFIGURATION = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

ISSUER = "https://accounts.google.com"
AUTHORIZATION_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
DEVICE_AUTHORIZATION_ENDPOINT = "https://oauth2.googleapis.com/device/code"
TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
USERINFO_ENDPOINT = "https://openidconnect.googleapis.com/v1/userinfo"
REVOCATION_ENDPOINT = "https://oauth2.googleapis.com/revoke"
JWKS_URI = "https://www.googleapis.com/oauth2/v3/certs"
OAUTH2_V1_USERINFO_ENDPOINT = "https://www.googleapis.com/oauth2/v1/userinfo"

SCOPES_SUPPORTED = ("openid", "email", "profile")
CLAIMS_SUPPORTED = (
    "aud",
    "email",
    "email_verified",
    "exp",
    "family_name",
    "given_name",
    "iat",
    "iss",
    "locale",
    "name",
    "picture",
    "sub",
)
