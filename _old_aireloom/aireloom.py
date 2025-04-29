from aireloom.httpx_client import Client

# read settings from yaml file, env file, and/or environment variables
# then create SETTINGS object


CLIENT = Client(refresh_token=..., access_token=..., max_retries=..., timeout=...)
