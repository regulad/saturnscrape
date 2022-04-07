from enum import Enum

from aiohttp import ClientSession, BaseConnector
from jwt import decode

from .types import *


class SaturnPlatform(Enum):
    SATURN_WEB = "web"


API_URL = "https://saturn.live/backend/prod/api/v2/"


class SaturnLiveClient:
    def __init__(self, platform: SaturnPlatform = SaturnPlatform.SATURN_WEB, *, connector: BaseConnector | None = None):
        self.platform: SaturnPlatform = platform
        self.session: ClientSession = ClientSession(connector=connector)

        self.token: str = ""
        self.student_id: int | None = None
        self.student: FullStudent | None = None
        self.school_id: str | None = None

    def get_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "DNT": "1",
            "X-Saturn-Platform": self.platform.value,
        }

    async def get_student(self, student_id: int) -> FullStudent:
        async with self.session.get(f"{API_URL}user/{student_id}", headers=self.get_headers()) as resp:
            return FullStudent.from_dict(await resp.json())

    async def get_calendar(self, school_id: str) -> list[CalendarDay]:
        async with self.session.get(f"{API_URL}schools/{school_id}/calendar", headers=self.get_headers()) as resp:
            return [CalendarDay.from_dict(day) for day in await resp.json()]

    async def get_all_courses(self, school_id: str) -> list[Course]:
        async with self.session.get(f"{API_URL}schools/{school_id}/courses", headers=self.get_headers()) as resp:
            return [Course.from_dict(course) for course in await resp.json()]

    async def get_courses(self, student_id: int) -> list[DefinedCourse]:
        async with self.session.get(f"{API_URL}user/{student_id}/courses", headers=self.get_headers()) as resp:
            return [DefinedCourse.from_dict(course) for course in await resp.json()]

    async def get_emojis(self) -> list[Emoji]:
        async with self.session.get(f"{API_URL}emojis", **self.get_headers()) as resp:
            return [Emoji.from_dict(emoji) for emoji in await resp.json()]

    # TODO: All chat endpoints

    # TODO: All sports endpoints (minus teams)

    # TODO: Sharing status endpoints

    async def get_schedules(self, student_id: int, *, include_chats: bool) -> list[BellSchedule]:
        async with self.session.get(f"{API_URL}user/{student_id}/schedule",
                                    params={"include_chats": str(include_chats)}, headers=self.get_headers()) as resp:
            return [BellSchedule.from_dict(schedule) for schedule in await resp.json()]

    async def get_schedule_changes(self, school_id: str) -> list[ScheduleChange]:
        async with self.session.get(f"{API_URL}network/reports/schedule_change", params={"school_id": school_id},
                                    headers=self.get_headers()) as resp:
            return [ScheduleChange.from_dict(change) for change in await resp.json()]

    async def get_all_staff(self, school_id: str) -> list[Staff]:
        async with self.session.get(f"{API_URL}schools/{school_id}/staff", headers=self.get_headers()) as resp:
            return [Staff.from_dict(staff) for staff in await resp.json()]

    # TODO: Task endpoints

    async def get_teams(self, school_id: str) -> list[Team]:
        async with self.session.get(f"{API_URL}events/{school_id}/teams", headers=self.get_headers()) as resp:
            return [Team.from_dict(team) for team in await resp.json()]

    async def get_students(self, school_id: str) -> list[Student]:
        async with self.session.get(f"{API_URL}schools/{school_id}/users", headers=self.get_headers()) as resp:
            return [Student.from_dict(student) for student in await resp.json()]

    async def populate(self, token: str):
        self.token = token
        decoded_token: dict = decode(token, options={'verify_signature': False}, algorithms=["HS256"])
        self.student_id: int = int(decoded_token["sub"])
        self.school_id: str = decoded_token["school_id"]
        self.student = await self.get_student(self.student_id)

    async def close(self):
        await self.session.close()


__all__ = ("SaturnLiveClient", "SaturnPlatform")
