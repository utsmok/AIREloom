from collections import defaultdict

import httpx
import polars as pl

base_url = "https://api.openaire.eu/graph/"
org_url = base_url + "organizations"
research_products_url = base_url + "researchProducts"
projects_url = base_url + "projects"


client_id = "457a7148-0179-477c-9100-9ffd4e6c8cb4"
secret = "OZLF7wevQvmgyDWkaLLNlnwrO7jzRctSW7jINDjnh5LSHwSKtaejO7s6tkzJW1y3o-MN3lLN4ziuI3nYFAgqvA"
credentials = httpx.post(
    url="https://aai.openaire.eu/oidc/token",
    auth=httpx.BasicAuth(username=client_id, password=secret),
    data={"grant_type": "client_credentials"},
)
token = credentials.json()["access_token"]
header = {"Authorization": "Bearer " + token, "accept": "application/json"}
basic_params = {"cursor": "*", "pageSize": 100}
client = httpx.Client(headers=header)


def get_projects(ut_id):
    projects_params = basic_params.copy()
    projects_params["relOrganizationId"] = ut_id
    done = False
    ut_projects = []
    while not done:
        projects_data = client.get(url=projects_url, params=projects_params).json()
        result = projects_data["results"]
        if isinstance(result, list):
            ut_projects.extend(result)
        if isinstance(result, dict):
            ut_projects.append(result)

        if len(projects_data["results"]) == 0:
            done = True
        else:
            projects_params["cursor"] = projects_data["header"]["nextCursor"]
    return pl.DataFrame(ut_projects, infer_schema_length=None)


def get_research_products(project_ids: list[str]) -> dict[str, list[dict]]:
    def get_data(
        given_url: str, params: dict, existing_data: list[dict] | None = None
    ) -> list[None] | list[dict[str, str | dict | list]]:
        research_products_data = client.get(url=given_url, params=params).json()

        if not existing_data:
            existing_data = []
            print(research_products_data["header"])
        result = research_products_data.get("results")

        if not result:
            return existing_data
        if isinstance(result, list):
            existing_data.extend(result)
        if isinstance(result, dict):
            existing_data.append(result)

        params["cursor"] = research_products_data["header"]["nextCursor"]
        return get_data(given_url, params, existing_data)

    all_research_products = defaultdict(list)
    total = len(project_ids)
    print(f"getting related research_products for {total} project ids")
    for item_num, id in enumerate(project_ids):
        url = "https://api.openaire.eu/graph/researchProducts"
        params = basic_params.copy()
        params["relProjectId"] = id
        all_research_products[id] = get_data(url, params)
        print(f"[{item_num}/{total}] +{len(all_research_products[id])}")
    return all_research_products


ut_params = basic_params.copy()
ut_params["pid"] = "https://ror.org/006hf6230"
ut_data: dict[str, str | list | dict] = client.get(
    url=org_url, params=ut_params
).json()["results"][0]
ut_id: str = ut_data["id"]

ut_projects_df: pl.DataFrame = get_projects(ut_id)
all_project_ids: list[str] = ut_projects_df["id"].to_list()
ut_research_products: dict[str, list[dict]] = get_research_products(all_project_ids)

print(
    f"Writing data for related research products for {len(ut_research_products)} projects to file..."
)
with open("ut_research_products.json", "w", encoding="utf-8") as f:
    f.write(str(ut_research_products))
