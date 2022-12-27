from asyncio import get_event_loop, AbstractEventLoop
from datetime import tzinfo
from logging import Logger, getLogger

from arrow import Arrow
from ics import *
from ics.grammar.parse import ContentLine
from ics.utils import arrow_to_iso
from pytz import UTC
from tzlocal import get_localzone
from vobject import vCard, vcard
from vobject.base import Component

from .client import SaturnLiveClient
from .types import *

logger: Logger = getLogger(__name__)


async def make_calendar(client: SaturnLiveClient, school_id: str, student_id: int) -> Calendar:
    """Make an ICS calendar from a calendar on https://saturn.live."""

    calendar_days: list[CalendarDay] = await client.get_calendar(school_id)
    schedules: list[BellSchedule] = await client.get_schedules(student_id, include_chats=False)
    student: Student = await client.get_student(student_id)

    school_name: str = school_id.replace('-', ' ').title()

    loop: AbstractEventLoop = get_event_loop()
    calendar: Calendar = await loop.run_in_executor(
        None,
        lambda: Calendar(creator=str(f"saturn-{school_id}-{student_id}"))
    )
    localzone: tzinfo = get_localzone()

    calendar.extra.extend(
        [
            ContentLine('X-WR-CALNAME', value=f"{student.name} at {school_name}'s Schedule"),
            ContentLine('X-WR-CALDESC', value=f"{student.name} at {school_name}'s Schedule"),
        ]
    )

    for day in calendar_days:
        if day.schedule and not day.is_canceled:
            bell_schedule: BellSchedule = next(filter(lambda x: x.id == day.schedule.id, schedules))

            all_day_event: Event = Event(name=bell_schedule.display_name, begin=day.date, end=day.date)
            all_day_event.make_all_day()
            calendar.events.add(all_day_event)

            for period in bell_schedule.periods:
                if period.instance:
                    def_course: DefinedCourse = period.instance
                    course: Course = def_course.course

                    class_event: Event = Event(
                        name=f"Period {period.name} - {def_course.nickname or course.name} - {def_course.room}",
                        begin=period.start_time.replace(
                            year=day.date.year, month=day.date.month, day=day.date.day, tzinfo=localzone
                        ).astimezone(UTC),
                        end=period.end_time.replace(
                            year=day.date.year, month=day.date.month, day=day.date.day, tzinfo=localzone
                        ).astimezone(UTC),
                        attendees=[
                            Attendee(common_name=student.name, email=student.email) for student in def_course.classmates
                        ],
                        description="Staff: " + ", ".join(map(lambda x: x.name, def_course.staff))
                    )

                    calendar.events.add(class_event)
                else:
                    calendar.events.add(
                        Event(
                            name=period.name,
                            begin=period.start_time.replace(
                                year=day.date.year, month=day.date.month, day=day.date.day, tzinfo=localzone
                            ).astimezone(UTC),
                            end=period.end_time.replace(
                                year=day.date.year, month=day.date.month, day=day.date.day, tzinfo=localzone
                            ).astimezone(UTC),
                        )
                    )

    return calendar


def make_contact(student: Student) -> Component:
    card: Component = vCard()

    # Name
    card.add('n').value = vcard.Name(family=student.last_name, given=student.first_name)
    card.add("fn").value = student.name

    # Profile Picture
    if hasattr(student, "profile_picture") and student.profile_picture:
        card.add("PHOTO").value = student.profile_picture["size_urls"].get("large") or student.profile_picture["size_urls"].get("medium") or student.profile_picture["size_urls"].get("small")

    # Email
    if hasattr(student, "email") and student.email:
        card.add('email')
        card.email.value = student.email
        card.email.type_param = ['WORK', 'INTERNET']

    # Instragram
    if hasattr(student, "instagram") and student.instagram:
        instagram = card.add("IMPP")
        instagram.value = student.user_instagram
        instagram.type_param = ['INSTAGRAM']

    # Snapchat
    if hasattr(student, "snapchat") and student.snapchat:
        instagram = card.add("IMPP")
        instagram.value = student.user_snapchat
        instagram.type_param = ['SNAPCHAT']

    # Tiktok
    if hasattr(student, "tiktok") and student.tiktok:
        instagram = card.add("IMPP")
        instagram.value = student.user_tiktok
        instagram.type_param = ['TIKTOK']

    # Venmo
    if hasattr(student, "venmo") and student.venmo:
        instagram = card.add("IMPP")
        instagram.value = student.user_venmo
        instagram.type_param = ['VENMOP']

    # Vsco
    if hasattr(student, "vsco") and student.vsco:
        instagram = card.add("IMPP")
        instagram.value = student.user_vsco
        instagram.type_param = ['vsco']

    # Phone
    if hasattr(student, "phone_number") and student.phone_number:
        card.add('tel')
        card.tel.value = student.phone_number
        card.tel.type_param = ['CELL', 'VOICE']

    # Birthday
    if hasattr(student, "birthday") and student.birthday:
        card.add('bday').value = arrow_to_iso(Arrow.fromdatetime(student.birthday))

    # Gender
    if hasattr(student, "gender") and student.gender:
        card.add("GENDER").value = student.gender

    return card


__all__ = ["make_calendar", "make_contact"]
