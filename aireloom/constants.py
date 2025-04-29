from typing import LiteralString

GRAPH_API_BASE_URL = "https://api.openaire.eu/graph/v1/"

#  curl -u {CLIENT_ID}:{CLIENT_SECRET} \
#  -X POST 'https://aai.openaire.eu/oidc/token' \
#  -d 'grant_type=client_credentials'
REGISTERED_SERVICE_API_TOKEN_URL = "https://aai.openaire.eu/oidc/token"


# GET https://services.openaire.eu/uoa-user-management/api/users/getAccessToken?refreshToken={your_refresh_token}
PERSONAL_API_TOKEN_URL: LiteralString = "https://services.openaire.eu/uoa-user-management/api/users/getAccessToken"




AIRELOOM_VERSION: LiteralString = "0.1.0"

CLIENT_HEADERS: dict[str, str] = {
    "accept": "application/json",
    "User-Agent": f"aireloom/{AIRELOOM_VERSION}"
}
