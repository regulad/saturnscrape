from argparse import ArgumentParser, Namespace
from asyncio import run, AbstractEventLoop, get_running_loop, gather, Semaphore
from json import dumps
from logging import Logger, getLogger
from os import environ
from typing import cast

from aiofiles import open as aioopen
from ics import Calendar
from vobject.base import Component

from . import *

logger: Logger = getLogger(__name__)


async def async_main(saturn_token: str, saturn_refresh_token: str, *, calendars: list[str | int], me: bool, school: str,
                     contacts: list[str | int], dump: bool) -> None:
    client: SaturnLiveClient = SaturnLiveClient(saturn_token, saturn_refresh_token)
    loop: AbstractEventLoop = get_running_loop()
    my_student: FullStudent = cast(FullStudent, await client.get_student("me"))
    school_id: str = school or my_student.school_id

    if me:
        print(f"{my_student.school_id} {my_student.id}")

    calendars: list[int] = [int(a) if a != "me" else my_student.id for a in calendars]
    contacts: list[int] = [int(a) if a != "me" else my_student.id for a in contacts]

    calendar_semaphore: Semaphore = Semaphore(10)

    async def write_calendar(calendar: int) -> None:
        async with calendar_semaphore:
            ics_calendar: Calendar = await utils.make_calendar(client, school_id, calendar)
            async with aioopen(f"{calendar}.ics", mode="w", loop=loop) as f:
                await f.write(str(ics_calendar))
            print(f"Wrote calendar of {calendar}")

    calendar_tasks: list[Task] = [loop.create_task(write_calendar(calendar)) for calendar in calendars]
    await gather(*calendar_tasks)

    contact_semaphore: Semaphore = Semaphore(10)

    async def write_contact(contact: int) -> None:
        async with contact_semaphore:
            student: Student = await client.get_student(contact)
            vcard: Component = utils.make_contact(student)
            async with aioopen(f"{student.id}.vcf", mode="w", loop=loop) as f:
                await f.write(vcard.serialize())
            print(f"Wrote contact of {student.id} {student.name}")

    if dump:
        students: list[FullStudent] = []

        student_semaphore: Semaphore = Semaphore(10)

        async def write_student(student: Student) -> None:
            async with student_semaphore:
                full_student: Student | FullStudent = await client.get_student(student.id)
                if isinstance(full_student, FullStudent):
                    students.append(full_student)
                    print(f"Scraped {student.id} {student.name}")

        await gather(*[loop.create_task(write_student(student)) for student in await client.get_students(school_id)])

        schedules: list[dict] = [schedule.to_dict() for schedule in
                                      await client.get_schedules(my_student.id, include_chats=False)]
        print("Scraped schedules")

        tasks: list[dict] = [task.to_dict() for task in await client.get_tasks()]
        print("Scraped tasks")

        teams: list[dict] = [team.to_dict() for team in await client.get_teams(school_id)]
        print("Scraped teams")

        calendar_days: list[dict] = [day.to_dict() for day in await client.get_calendar(school_id)]
        print("Scraped calendar days")

        defined_courses: list[dict] = [course.to_dict() for course in await client.get_courses(my_student.id)]
        print("Scraped defined courses")

        emojis: list[dict] = [emoji.to_dict() for emoji in await client.get_emojis()]
        print("Scraped emojis")

        staff: list[dict] = [staff.to_dict() for staff in await client.get_all_staff(school_id)]
        print("Scraped staff")

        schedule_changes: list[dict] = [change.to_dict() for change in
                                             await client.get_schedule_changes(school_id)]
        print("Scraped schedule changes")


        async with aioopen(f"{school_id}.json", mode="w", loop=loop) as fp:
            await fp.write(
                dumps(
                    {
                        "students": [student.to_dict() for student in students],
                        "school": school_id,
                        "schedules": schedules,
                        "tasks": tasks,
                        "teams": teams,
                        "emojis": emojis,
                        "staff": staff,
                        "schedule_changes": schedule_changes,
                        "calendar_days": calendar_days,
                        "defined_courses": defined_courses,
                    },
                    indent=4
                )
            )

    contact_tasks: list[Task] = [loop.create_task(write_contact(contact)) for contact in contacts]
    await gather(*contact_tasks)

    await client.close()


def main() -> None:
    parser: ArgumentParser = ArgumentParser(prog="saturnscrape",
                                            description="Scrape Saturn's website for data, and store either your schduele or your contacts.")
    parser.add_argument("-t", "--token", dest="token", type=str,
                        help="Saturn's API token. Will be read from the environment variable SATURN_TOKEN if not provided.")
    parser.add_argument("-r", "--refresh-token", dest="rtoken", type=str,
                        help="Saturn's refresh token. Will be read from the environment variable SATURN_REFRESH_TOKEN if not provided.")
    parser.add_argument("-s", "--school-id", dest="school", type=str,
                        help="The school ID to use for all operations. Defaults to your own school ID.")
    parser.add_argument("-c", "--calendar", dest="calendars", action='append',
                        help="Student IDs to scrape the calendar from. Optional.")
    parser.add_argument("-a", "--contacts", dest="contacts", action='append',
                        help="Student IDs to scrape the contact from. Optional.")
    parser.add_argument("-m", "--me", dest="me", action='store_const', const=True, default=False,
                        help="Scrape your own ID.")
    parser.add_argument("-d", "--dump", dest="dump", action='store_const', const=True, default=False,
                        help="If all school data should be dumped.")
    args: Namespace = parser.parse_args()

    token: str = args.token or environ["SATURN_TOKEN"]
    refresh_token: str = args.rtoken or environ["SATURN_REFRESH_TOKEN"]
    calendars: list[str | int] = [int(a) if a != "me" else "me" for a in
                                  args.calendars] if args.calendars else None or []
    contacts: list[str | int] = [int(a) if a != "me" else "me" for a in args.contacts] if args.contacts else None or []

    run(async_main(token, refresh_token, calendars=calendars, me=args.me, school=args.school, contacts=contacts,
                   dump=args.dump))


if __name__ == '__main__':
    main()
