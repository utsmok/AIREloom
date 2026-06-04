"""Example: Working with the OpenAIRE Persons endpoint.

Demonstrates searching for researchers, retrieving individual person records,
and exploring co-authorship networks.
"""
import asyncio
import os

from dotenv import load_dotenv

load_dotenv(".env")

from aireloom import AireloomClient
from aireloom.endpoints import PersonsFilters


async def main():
    client_id = os.getenv("AIRELOOM_OPENAIRE_CLIENT_ID")
    client_secret = os.getenv("AIRELOOM_OPENAIRE_CLIENT_SECRET")

    async with AireloomClient(client_id=client_id, client_secret=client_secret) as client:
        # 1. Search for a researcher by name
        print("=== Search for researchers named 'Wesley Brewer' ===")
        response = await client.persons.search(
            page=1,
            page_size=5,
            filters=PersonsFilters(search="Wesley Brewer"),
        )
        print(f"Found {response.header.numFound} results")
        for person in (response.results or [])[:5]:
            print(f"  {person.givenName} {person.familyName}")
            print(f"    ID: {person.id}")
            if person.originalId:
                print(f"    ORCID: {person.originalId[0]}")
            if person.biography:
                print(f"    Bio: {person.biography[:100]}...")
            print()

        # 2. Get a specific person by OpenAIRE ID
        print("=== Get person by ID ===")
        person = await client.persons.get("orcid_______::ebbe30d5171e6e53545e7acb391bc9a2")
        print(f"  Name: {person.givenName} {person.familyName}")
        print(f"  ID: {person.id}")
        if person.originalId:
            print(f"  Identifiers: {person.originalId}")
        if person.subject:
            print(f"  Subjects: {', '.join(person.subject[:5])}")

        # 3. Search by ORCID using originalId filter
        print("\n=== Search by ORCID ===")
        response = await client.persons.search(
            filters=PersonsFilters(originalId="0000-0002-3639-3956"),
            page=1,
            page_size=1,
        )
        if response.results:
            p = response.results[0]
            print(f"  Found: {p.givenName} {p.familyName} (ID: {p.id})")

        # 4. Browse persons with iteration (cursor-based)
        print("\n=== Iterate persons (first 10) ===")
        count = 0
        async for person in client.persons.iterate(
            page_size=10,
            filters=PersonsFilters(search="machine learning"),
        ):
            count += 1
            name = f"{person.givenName or '?'} {person.familyName or '?'}"
            print(f"  {count}. {name}")
            if count >= 10:
                break
        print(f"  (showing first {count} results)")


if __name__ == "__main__":
    asyncio.run(main())
