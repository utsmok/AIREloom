import marimo

__generated_with = "0.11.17"
app = marimo.App(width="medium")


@app.cell
def _():
    import os
    import json
    import httpx
    import polars as pl
    return httpx, json, os, pl


@app.cell
def _():
    base_url = "https://api.openaire.eu/graph/"
    org_url = base_url + "organizations"
    research_products_url = base_url + "researchProducts"
    projects_url = base_url + "projects"
    return base_url, org_url, projects_url, research_products_url


@app.cell
def _(httpx):
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
    return basic_params, client, client_id, credentials, header, secret, token


@app.cell
def _(basic_params, client, org_url):
    ut_params = basic_params.copy()
    ut_params["pid"] = "https://ror.org/006hf6230"
    ut_data = client.get(url=org_url, params=ut_params).json()["results"][0]
    ut_id = ut_data["id"]
    return ut_data, ut_id, ut_params


@app.cell
def _(basic_params, client, pl, projects_url):
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
    return (get_projects,)


@app.cell
def _(get_projects, get_research_products, ut_id):
    ut_projects_df = get_projects(ut_id)
    all_project_ids = ut_projects_df["id"].to_list()
    ut_research_products_df = get_research_products(all_project_ids[0:1])
    return all_project_ids, ut_projects_df, ut_research_products_df


@app.cell
def _(basic_params, client, pl):
    def get_research_products(all_project_ids):
        def get_data(given_url, params, existing_data=None):
            research_products_data = client.get(url=given_url, params=params).json()
            result = research_products_data.get("results")
            if not result:
                return existing_data
            if not existing_data:
                existing_data = []
            if isinstance(result, list):
                existing_data.extend(result)
            if isinstance(result, dict):
                existing_data.append(result)
            params["cursor"] = research_products_data["header"]["nextCursor"]
            return get_data(given_url, params, existing_data)

        
        all_research_products = []
        total = len(all_project_ids)
        for item_num, id in enumerate(all_project_ids):
            url = f"https://api.openaire.eu/graph/researchProducts?relProjectId={id}&relOrganizationId=openorgs____::604881198363fedbb5d5478f465305f2"
            params = basic_params.copy()
            cur_len = len(all_research_products)
            done = False
            research_products_data = get_data(url, params)
            if isinstance(research_products_data, list):
                all_research_products.extend(research_products_data)
            if isinstance(research_products_data, dict):
                all_research_products.append(research_products_data)
        
            print(f'[{item_num}/{total}] {len(all_research_products)} (+{len(all_research_products) - cur_len})')
        return pl.DataFrame(all_research_products, infer_schema_length=None)
    return (get_research_products,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
