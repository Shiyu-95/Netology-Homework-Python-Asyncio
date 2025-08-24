import asyncio
import aiohttp
import datetime

from models import SwapiPeople, Session, init_orm, close_orm

API_URL = 'https://www.swapi.tech/api/people/'


async def count_of_people(session):
    async with session.get(API_URL) as response:
        data = await response.json()
        return data['total_records']


async def get_people(person_id, session):
    async with session.get(f'{API_URL}{person_id}') as response:
        json = await response.json()
        if json.get("result") is None:
            return None
        swapi_people = SwapiPeople(
            id=json["result"]['uid'],
            birth_year=json["result"]["properties"]['birth_year'],
            eye_color=json["result"]["properties"]['eye_color'],
            hair_color=json["result"]["properties"]['hair_color'],
            homeworld=json["result"]["properties"]['homeworld'],
            mass=json["result"]["properties"]['mass'],
            name=json["result"]["properties"]['name'],
            skin_color=json["result"]["properties"]['skin_color']
        )
        print(swapi_people.id)
    return swapi_people


async def add_people(people):
    async with Session() as session:
        session.add_all(people)
        await session.commit()


async def main():
    await init_orm()
    async with aiohttp.ClientSession() as session:
        total_records = await count_of_people(session)
        coros = [get_people(person_id, session) for person_id in range(1, total_records + 1)]
        people = await asyncio.gather(*coros)
        people = [person for person in people if person is not None]
        await add_people(people)
    await close_orm()


start = datetime.datetime.now()
main_coro = main()
asyncio.run(main_coro)
