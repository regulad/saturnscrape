from enum import Enum
from time import time
from typing import Literal

from aiohttp import ClientSession, BaseConnector
from jwt import decode

from .types import *


class SaturnPlatform(Enum):
    SATURN_WEB = "web"


API_URL = "https://saturn.live/backend/prod/api/v2/"


class SaturnLiveClient:
    def __init__(
            self,
            access_token: str,
            refresh_token: str,
            *,
            user_agent: str | None = None,
            platform: SaturnPlatform = SaturnPlatform.SATURN_WEB,
            connector: BaseConnector | None = None
    ):
        self.platform: SaturnPlatform = platform
        self.session: ClientSession = ClientSession(connector=connector)

        self.refresh_token: str = refresh_token
        self.token: str = access_token
        self.user_agent: str | None = user_agent

        self.identity: Identity | None = None

    async def on_token_change(self, access_token: str) -> None:
        """For saving the token to a file or database so you can log in later."""
        pass

    async def authorize(self, access_token: str, refresh_token: str) -> tuple[str, Identity, str | None]:
        async with self.session.post(
                "https://saturn.live/refresh/prod/auth",
                json={"access_token": access_token, "refresh_token": refresh_token}
        ) as resp:
            if resp.status == 200:
                json_data: dict = await resp.json()
                return json_data["access_token"], Identity.from_dict(json_data["identity"]), json_data[
                    "refresh_token"] or refresh_token
            else:
                raise resp.raise_for_status()

    async def get_token(self) -> None:
        if self.token:
            decoded_token: dict = decode(self.token, options={'verify_signature': False}, algorithms=["HS256"])
            if decoded_token["exp"] > time():
                return
        self.token, self.identity, self.refresh_token = await self.authorize(self.refresh_token, self.refresh_token)
        await self.on_token_change(self.token)

    async def get_headers(self) -> dict:
        headers: dict = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "DNT": "1",
            "X-Saturn-Platform": self.platform.value,
        }
        if self.user_agent:
            headers["User-Agent"] = self.user_agent
        await self.get_token()
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    async def get_student(self, student_id: int | Literal["me"]) -> Student:
        async with self.session.get(f"{API_URL}user/{student_id}", headers=await self.get_headers()) as resp:
            if resp.status == 200:
                json_data: dict = await resp.json()
                if json_data["public"]:
                    return FullStudent.from_dict(json_data)
                else:
                    return Student.from_dict(json_data)  # Private accounts are missing data.
            else:
                raise resp.raise_for_status()

    async def get_calendar(self, school_id: str) -> list[CalendarDay]:
        async with self.session.get(f"{API_URL}schools/{school_id}/calendar", headers=await self.get_headers()) as resp:
            if resp.status == 200:
                return [CalendarDay.from_dict(day) for day in await resp.json()]
            else:
                raise resp.raise_for_status()

    async def get_all_courses(self, school_id: str) -> list[Course]:
        async with self.session.get(f"{API_URL}schools/{school_id}/courses", headers=await self.get_headers()) as resp:
            if resp.status == 200:
                return [Course.from_dict(course) for course in await resp.json()]
            else:
                raise resp.raise_for_status()

    async def get_courses(self, student_id: int) -> list[DefinedCourse]:
        async with self.session.get(f"{API_URL}user/{student_id}/courses", headers=await self.get_headers()) as resp:
            if resp.status == 200:
                return [DefinedCourse.from_dict(course) for course in await resp.json()]
            else:
                raise resp.raise_for_status()

    async def get_emojis(self) -> list[Emoji]:
        async with self.session.get(f"{API_URL}emojis", **await self.get_headers()) as resp:
            if resp.status == 200:
                return [Emoji.from_dict(emoji) for emoji in await resp.json()]
            else:
                raise resp.raise_for_status()

    # TODO: All chat endpoints

    # TODO: All sports endpoints (minus teams)

    # TODO: Sharing status endpoints

    async def get_schedules(self, student_id: int, *, include_chats: bool) -> list[BellSchedule]:
        async with self.session.get(f"{API_URL}user/{student_id}/schedule",
                                    params={"include_chats": str(include_chats)},
                                    headers=await self.get_headers()) as resp:
            if resp.status == 200:
                return [BellSchedule.from_dict(schedule) for schedule in await resp.json()]
            else:
                raise resp.raise_for_status()

    async def get_schedule_changes(self, school_id: str) -> list[ScheduleChange]:
        async with self.session.get(f"{API_URL}network/reports/schedule_change", params={"school_id": school_id},
                                    headers=await self.get_headers()) as resp:
            if resp.status == 200:
                return [ScheduleChange.from_dict(change) for change in await resp.json()]
            else:
                raise resp.raise_for_status()

    async def get_all_staff(self, school_id: str) -> list[Staff]:
        async with self.session.get(f"{API_URL}schools/{school_id}/staff", headers=await self.get_headers()) as resp:
            if resp.status == 200:
                return [Staff.from_dict(staff) for staff in await resp.json()]
            else:
                raise resp.raise_for_status()

    async def get_tasks(self) -> list[Task]:
        async with self.session.get(f"{API_URL}tasks", headers=await self.get_headers()) as resp:
            if resp.status == 200:
                return [Task.from_dict(task) for task in await resp.json()]
            else:
                raise resp.raise_for_status()

    async def add_task(self, task: Task) -> None:
        async with self.session.post(f"{API_URL}tasks", json=dict(task), headers=await self.get_headers()) as resp:
            if resp.status != 200:
                raise resp.raise_for_status()

    async def remove_task(self, task_id: int) -> None:
        async with self.session.delete(f"{API_URL}tasks/{task_id}", headers=await self.get_headers()) as resp:
            if resp.status != 204:
                raise resp.raise_for_status()

    async def get_teams(self, school_id: str) -> list[Team]:
        async with self.session.get(f"{API_URL}events/{school_id}/teams", headers=await self.get_headers()) as resp:
            if resp.status == 200:
                return [Team.from_dict(team) for team in await resp.json()]
            else:
                raise resp.raise_for_status()

    async def get_students(self, school_id: str) -> list[Student]:
        async with self.session.get(f"{API_URL}schools/{school_id}/users", headers=await self.get_headers()) as resp:
            if resp.status == 200:
                return [Student.from_dict(student) for student in await resp.json()]
            else:
                raise resp.raise_for_status()

    async def close(self):
        await self.session.close()


__all__ = ("SaturnLiveClient", "SaturnPlatform")
