from datetime import datetime
from logging import Logger, getLogger
from typing import Any, TypedDict, TYPE_CHECKING, Type
from uuid import UUID

logger: Logger = getLogger(__name__)

if TYPE_CHECKING:
    OLD_CLASS_INHERIT: Type = TypedDict
else:
    OLD_CLASS_INHERIT: Type = dict


class _OldClass(OLD_CLASS_INHERIT):
    # patch between old code and new code. Very hacky, but I don't want to write things.
    def __init__(self, *args, **kwargs: Any) -> None:
        super(_OldClass, self).__init__(*args, **kwargs)
        self.__dict__ = self

    @classmethod
    def from_dict(cls, data: dict) -> "_OldClass":
        copied = data.copy()

        for key, value in copied.copy().items():
            if "id" in key:
                try:
                    copied[key] = UUID(value)
                except Exception:
                    continue
            elif "date" in key or "day" in key:
                try:
                    copied[key] = datetime.strptime(value, "%Y-%m-%d")
                except Exception:
                    continue
            elif "at" in key:
                try:
                    copied[key] = datetime.fromisoformat(value)
                except Exception:
                    continue

        return cls(**copied)

    def to_dict(self) -> dict:
        copied: dict = self.copy()

        for key, value in copied.copy().items():
            if isinstance(value, UUID):
                copied[key] = str(value)
            elif isinstance(value, datetime):
                if "date" in key or "day" in key:
                    copied[key] = value.strftime("%Y-%m-%d")
                else:
                    copied[key] = value.isoformat()

        return copied


class SizeUrls(_OldClass):
    large: str
    medium: str
    small: str


class Image(_OldClass):
    def __eq__(self, other):
        return (
                isinstance(other, self.__class__)
                and self.id == other.id
        )

    content_type: str
    id: str
    is_bitmoji: bool
    metadata: dict[str, int] | None
    resource_url: str
    size_urls: SizeUrls


class BaseStudent(_OldClass):
    def __eq__(self, other):
        return (
                isinstance(other, self.__class__)
                and self.id == other.id
        )

    id: str
    name: str


class Student(BaseStudent):
    ambassador_school: str | None
    bio: str | None
    birthday: datetime | None
    created_at: datetime
    email: str | None
    first_name: str
    grade: int
    hidden: Any | None
    is_ambassador: bool
    last_name: str
    profile_picture: Image | None
    public: bool
    url: str | None
    user_cohort: str | None
    user_instagram: str | None
    user_snapchat: str | None
    user_tiktok: str | None
    user_venmo: str | None
    user_vsco: str | None
    user_education: str | None
    user_city: str | None
    user_workplace: str | None
    schedule_type_response: str | None
    lite_to_live_completed: bool | None
    gameball_id: str | None
    description: str | None
    affinity: str | None
    updated_at: datetime | None
    tags: str | None
    school_id: str | None


class Staff(_OldClass):
    id: int
    name: str
    suggested: bool


class Asset(_OldClass):
    gif: Image | None
    png: Image | None
    unicode: str
    unicode_code: str


class Emoji(_OldClass):
    category: str
    name: str
    position: int
    resources: Asset
    schedule_snapchat_sticker: str | None
    snapchat_sticker: str | None
    tags: list[str]
    updated_at: datetime


class Course(_OldClass):
    emoji: Emoji
    id: int
    name: str
    school: str
    suggested: bool


class Team(_OldClass):
    emoji_id: str
    gender: str
    id: UUID
    level: str
    name: str
    sport: str
    subscribed: bool


# TODO: Sharing status.


# TODO: Messages


# TODO: Chats


class DefinedCourse(_OldClass):
    block: Any | None  # Unknown
    class_chat: UUID | None
    classmates: list[Student]
    course: Course
    id: int
    meeting_times: dict[UUID, list[UUID]]
    nickname: str | None
    room: str
    school: str
    staff: list[Staff]


class Period(_OldClass):
    day_type_id: UUID
    end_time: datetime
    id: UUID
    instance: DefinedCourse
    name: str
    period_type_id: UUID
    start_time: datetime


class BaseSchedule(_OldClass):
    display_name: str
    id: UUID
    name: str
    special: bool
    static: bool


class BellSchedule(BaseSchedule):
    author: BaseStudent | None
    author_id: int | None
    draft: bool
    emoji: Emoji | None
    emoji_id: str | None
    grid: bool
    hidden: bool
    lunch_slot: Any | None  # Unknown
    lunch_waves: list  # Unknown
    order: int
    periods: list[Period]
    school_id: str
    updated_at: datetime


class CalendarDay(_OldClass):
    date: datetime
    is_canceled: bool
    raw_block_name: str
    schedule: BaseSchedule | None


class ScheduleChange(_OldClass):
    count: int
    desired_schedule: str
    desired_schedule_id: UUID
    original_schedule: str
    original_schedule_id: UUID
    user_id: int


class ScheduleChangeReport(_OldClass):
    def __eq__(self, other):
        return (
                isinstance(other, self.__class__)
                and self.key == other.key
        )

    ambassadors: list[BaseStudent]
    changes: list[ScheduleChange]
    district_school_count: int
    district_schools: list[str]
    key: int
    report_count: int
    school_name: str
    school_title: str
    state: str
    status: str
    target_date: datetime
    timezone: str  # We can (possibly) do better.
    upcoming_days: int
    user_count: int


class FullStudent(Student):
    profile_pic_url: str
    gender: Any | None  # Unknown
    gender_preference: Any | None  # Unknown
    onboarded: bool
    phone_number: str
    phone_validated: bool
    granted_scopes: list[Any]  # Unknown
    referred_by: Any | None  # Unknown
    ambassador_school_id: Any | None  # Unknown
    hashid: str
    school_title: str
    school: str
    waitlist_school: Any | None  # Unknown
    courses: list[DefinedCourse]
    permissions: dict[str, bool]


class Task(_OldClass):
    added_by: list[BaseStudent]  # Unknown
    attachments: list[Any]  # Unknown
    course_id: UUID | None
    course_slot: bool
    created_at: datetime
    date_completed: datetime | None
    description: str | None
    due_date: datetime
    due_datetime: datetime
    due_seconds: int
    id: int
    images: list[Image]  # Unknown
    is_completed: bool
    priority: int
    public: bool
    shared_with: list[BaseStudent]
    title: str
    updated_at: datetime


class Identity:
    first_name: str
    last_name: str
    onboarded: bool
    profile_pic: Image
    school_id: str
    scopes: str


__all__ = (
    "SizeUrls",
    "Image",
    "BaseStudent",
    "Student",
    "Staff",
    "Asset",
    "Emoji",
    "Course",
    "Team",
    "DefinedCourse",
    "Period",
    "BaseSchedule",
    "BellSchedule",
    "CalendarDay",
    "ScheduleChange",
    "ScheduleChangeReport",
    "FullStudent",
    "Task",
    "Identity",
)
