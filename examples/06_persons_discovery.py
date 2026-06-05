# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "aireloom",
#     "marimo",
# ]
#
# [tool.marimo.runtime]
# auto_instantiate = true
# ///

import marimo

__generated_with = "0.13.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(
        """
    # 👤 Persons Discovery

    Search for researchers, retrieve individual person records, and explore co-authorship networks using the OpenAIRE Persons endpoint.

    *Switch to code view with Ctrl+. to see all code cells*
    """
    )


@app.cell
def _():
    from aireloom import AireloomClient
    from aireloom.endpoints import PersonsFilters

    return AireloomClient, PersonsFilters


@app.cell
async def _(AireloomClient, PersonsFilters, mo):
    async with AireloomClient() as client:
        response = await client.persons.search(
            page=1,
            page_size=5,
            filters=PersonsFilters(search="Wesley Brewer"),
        )

    lines = [f"**Found {response.header.numFound} results**\n"]
    for person in (response.results or [])[:5]:
        name = f"{person.givenName} {person.familyName}"
        lines.append(f"- **{name}**  ")
        lines.append(f"  - ID: `{person.id}`")
        if person.originalId:
            lines.append(f"  - ORCID: `{person.originalId[0]}`")
        if person.biography:
            lines.append(f"  - Bio: {person.biography[:100]}…")
        lines.append("")

    mo.md("\n".join(lines))


@app.cell
async def _(AireloomClient, mo):
    async with AireloomClient() as client:
        person = await client.persons.get(
            "orcid_______::ebbe30d5171e6e53545e7acb391bc9a2"
        )

    lines = [
        f"**Name:** {person.givenName} {person.familyName}  ",
        f"**ID:** `{person.id}`",
    ]
    if person.originalId:
        lines.append(f"**Identifiers:** {person.originalId}")
    if person.subject:
        lines.append(f"**Subjects:** {', '.join(person.subject[:5])}")

    mo.md("\n".join(lines))


@app.cell
async def _(AireloomClient, PersonsFilters, mo):
    async with AireloomClient() as client:
        response = await client.persons.search(
            filters=PersonsFilters(originalId="0000-0002-3639-3956"),
            page=1,
            page_size=1,
        )

    if response.results:
        p = response.results[0]
        mo.md(f"Found: **{p.givenName} {p.familyName}** (ID: `{p.id}`)")
    else:
        mo.md("No person found with that ORCID.")


@app.cell
async def _(AireloomClient, PersonsFilters, mo):
    async with AireloomClient() as client:
        persons = []
        async for person in client.persons.iterate(
            page_size=10,
            filters=PersonsFilters(search="machine learning"),
        ):
            name = f"{person.givenName or '?'} {person.familyName or '?'}"
            persons.append(name)
            if len(persons) >= 10:
                break

    rows = [f"{i + 1}. {name}" for i, name in enumerate(persons)]
    mo.md(
        f"**First {len(persons)} results for 'machine learning':**\n\n"
        + "\n".join(rows)
    )


if __name__ == "__main__":
    app.run()
