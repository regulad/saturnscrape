from datetime import datetime
from typing import Any
from uuid import UUID


class SizeUrls:
    __slots__ = ("large", "medium", "small")

    def __init__(self, *, large: str, medium: str, small: str):
        self.large: str = large
        self.medium: str = medium
        self.small: str = small

    @classmethod
    def from_dict(cls, d: dict):
        return cls(**d)


class Image:
    def __eq__(self, other):
        return (
                isinstance(other, self.__class__)
                and self.id == other.id
        )

    __slots__ = ("content_type", "id", "is_bitmoji", "metadata", "resource_url", "size_urls")

    def __init__(
            self,
            *,
            content_type: str,
            id: str,
            is_bitmoji: bool,
            metadata: dict[str, int] | None,
            resource_url: str,
            size_urls: SizeUrls
    ):
        self.content_type: str = content_type
        self.id: str = id
        self.is_bitmoji: bool = is_bitmoji
        self.metadata: dict[str, int] | None = metadata
        self.resource_url: str = resource_url
        self.size_urls: SizeUrls = size_urls

    @classmethod
    def from_dict(cls, d: dict):
        d = d.copy()
        d["size_urls"] = SizeUrls.from_dict(d["size_urls"])
        d["metadata"] = d.get("metadata")
        d["is_bitmoji"] = d.get("is_bitmoji", False)
        return cls(**d)


class BaseStudent:
    def __eq__(self, other):
        return (
                isinstance(other, self.__class__)
                and self.id == other.id
        )

    __slots__ = ("id", "name")

    def __init__(self, *, id: int, name: str):
        self.id: int = id
        self.name: str = name

    @classmethod
    def from_dict(cls, d: dict):
        return cls(**d)


class Student(BaseStudent):
    __slots__ = BaseStudent.__slots__ + (
        "ambassador_school",
        "bio",
        "birthday",
        "created_at",
        "email",
        "first_name",
        "grade",
        "hidden",
        "is_ambassador",
        "last_name",
        "profile_picture",
        "public",
        "url",
        "user_cohort",
        "user_instagram",
        "user_snapchat",
        "user_tiktok",
        "user_venmo",
        "user_vsco",
        "updated_at",
    )

    def __init__(
            self,
            *,
            ambassador_school: str | None,
            bio: str | None,
            birthday: datetime,
            created_at: datetime,
            email: str | None,
            first_name: str,
            grade: int,
            hidden: Any | None,  # Unknown
            id: int,
            is_ambassador: bool,
            last_name: str,
            name: str,
            profile_picture: Image | None,
            public: bool,
            url: str | None,
            user_cohort: str | None,
            user_instagram: str | None,
            user_snapchat: str | None,
            user_tiktok: str | None,
            user_venmo: str | None,
            user_vsco: str | None,
    ):
        super().__init__(id=id, name=name)
        self.ambassador_school: str | None = ambassador_school
        self.bio: str | None = bio
        self.birthday: datetime = birthday
        self.created_at: datetime = created_at
        self.email: str | None = email
        self.first_name: str = first_name
        self.grade: int = grade
        self.hidden: Any | None = hidden
        self.is_ambassador: bool = is_ambassador
        self.last_name: str = last_name
        self.profile_picture: Image | None = profile_picture
        self.public: bool = public
        self.url: str | None = url
        self.user_cohort: str | None = user_cohort
        self.user_instagram: str | None = user_instagram
        self.user_snapchat: str | None = user_snapchat
        self.user_tiktok: str | None = user_tiktok
        self.user_venmo: str | None = user_venmo
        self.user_vsco: str | None = user_vsco

    @classmethod
    def from_dict(cls, d: dict):
        d = d.copy()
        d["created_at"] = datetime.fromisoformat(d["created_at"])
        if "profile_picture" in d and d["profile_picture"]:
            d["profile_picture"] = Image.from_dict(d["profile_picture"])
        else:
            d["profile_picture"] = None
        if d.get("birthday"):
            d["birthday"] = datetime.strptime(d["birthday"], "%Y-%m-%d")
        return cls(**d)


class Staff:
    def __eq__(self, other):
        return (
                isinstance(other, self.__class__)
                and self.id == other.id
        )

    __slots__ = ("id", "name", "suggested")

    def __init__(self, *, id: int, name: str, suggested: bool):
        self.id: int = id
        self.name: str = name
        self.suggested: bool = suggested

    @classmethod
    def from_dict(cls, d: dict):
        return cls(**d)


class Asset:
    __slots__ = ("gif", "png", "unicode", "unicode_code")

    def __init__(
            self,
            *,
            gif: Image | None,
            png: Image | None,
            unicode: str,
            unicode_code: str
    ):
        self.gif: Image | None = gif
        self.png: Image | None = png
        self.unicode: str = unicode
        self.unicode_code: str = unicode_code

    @classmethod
    def from_dict(cls, d: dict):
        d = d.copy()
        if d.get("gif"):
            d["gif"] = Image.from_dict(d["gif"])
        if d.get("png"):
            d["png"] = Image.from_dict(d["png"])
        return cls(**d)


class Emoji:
    def __eq__(self, other):
        return (
                isinstance(other, self.__class__)
                and self.position == other.position
        )

    __slots__ = ("category", "name", "position", "resources", "schedule_snapchat_sticker", "tags", "snapchat_sticker")

    def __init__(
            self,
            *,
            category: str,
            name: str,
            position: int,
            resources: Asset,
            schedule_snapchat_sticker: str | None,
            snapchat_sticker: str | None,
            tags: list[str]
    ):
        self.category: str = category
        self.name: str = name
        self.position: int = position
        self.resources: Asset = resources
        self.schedule_snapchat_sticker: str | None = schedule_snapchat_sticker
        self.snapchat_sticker: str | None = snapchat_sticker
        self.tags: list[str] = tags

    @classmethod
    def from_dict(cls, d: dict):
        d = d.copy()
        d["resources"] = Asset.from_dict(d["resources"])
        d["snapchat_sticker"] = d.get("snapchat_sticker") or d.get("schedule_snapchat_sticker")
        return cls(**d)


class Course:
    def __eq__(self, other):
        return (
                isinstance(other, self.__class__)
                and self.id == other.id
        )

    __slots__ = ("emoji", "id", "name", "school", "suggested")

    def __init__(
            self,
            *,
            emoji: Emoji,
            id: int,
            name: str,
            school: str,
            suggested: bool
    ):
        self.emoji: Emoji = emoji
        self.id: int = id
        self.name: str = name
        self.school: str = school
        self.suggested: bool = suggested

    @classmethod
    def from_dict(cls, d: dict):
        d = d.copy()
        d["emoji"] = Emoji.from_dict(d["emoji"])
        return cls(**d)


class Team:
    __slots__ = ("emoji_id", "gender", "id", "level", "name", "sport", "subscribed")

    def __init__(
            self,
            *,
            emoji_id: str,
            gender: str,
            id: UUID,
            level: str,
            name: str,
            sport: str,
            subscribed: bool,
    ):
        self.emoji_id: str = emoji_id
        self.gender: str = gender
        self.id: UUID = id
        self.level: str = level
        self.name: str = name
        self.sport: str = sport
        self.subscribed: bool = subscribed

    @classmethod
    def from_dict(cls, d: dict):
        d = d.copy()
        d["id"] = UUID(d["id"])
        return cls(**d)


# TODO: I don't use tasks, so I can't get any data from it.


# TODO: Sharing status.


# TODO: Messages


# TODO: Chats


class DefinedCourse:
    def __eq__(self, other):
        return (
                isinstance(other, self.__class__)
                and self.id == other.id
        )

    __slots__ = (
        "block",
        "class_chat",
        "classmates",
        "course",
        "id",
        "meeting_times",
        "nickname",
        "room",
        "school",
        "staff"
    )

    def __init__(
            self,
            *,
            block: Any | None,  # Unknown
            class_chat: UUID | None,
            classmates: list[Student],
            course: Course,
            id: int,
            meeting_times: dict[UUID, list[UUID]],
            nickname: str | None,
            room: str,
            school: str,
            staff: list[Staff],
    ):
        self.block: Any | None = block
        self.class_chat: UUID | None = class_chat
        self.classmates: list[Student] = classmates
        self.course: Course = course
        self.id: int = id
        self.meeting_times: dict[UUID, list[UUID]] = meeting_times
        self.nickname: str | None = nickname
        self.room: str = room
        self.school: str = school
        self.staff: list[Staff] = staff

    @classmethod
    def from_dict(cls, d: dict):
        d = d.copy()
        if d.get("class_chat"):
            d["class_chat"] = UUID(d["class_chat"])
        d["classmates"] = [Student.from_dict(s) for s in d.get("classmates", [])]
        d["course"] = Course.from_dict(d["course"])
        d["meeting_times"] = {UUID(k): [UUID(m) for m in v] for k, v in d["meeting_times"].items()}
        d["staff"] = [Staff.from_dict(s) for s in d["staff"]]
        return cls(**d)


class Period:
    def __eq__(self, other):
        return (
                isinstance(other, self.__class__)
                and self.id == other.id
        )

    __slots__ = (
        "day_type_id",
        "end_time",
        "id",
        "instance",
        "name",
        "period_type_id",
        "start_time"
    )

    def __init__(
            self,
            *,
            day_type_id: UUID,
            end_time: datetime,
            id: UUID,
            instance: DefinedCourse,
            name: str,
            period_type_id: UUID,
            start_time: datetime,
    ):
        self.day_type_id: UUID = day_type_id
        self.end_time: datetime = end_time
        self.id: UUID = id
        self.instance: DefinedCourse = instance
        self.name: str = name
        self.period_type_id: UUID = period_type_id
        self.start_time: datetime = start_time

    @classmethod
    def from_dict(cls, d: dict):
        d = d.copy()
        d["day_type_id"] = UUID(d["day_type_id"])
        d["period_type_id"] = UUID(d["period_type_id"])
        d["id"] = UUID(d["id"])
        d["instance"] = DefinedCourse.from_dict(d["instance"])
        if d.get("start_time"):
            d["start_time"] = datetime.fromisoformat(d["start_time"])  # TODO
        if d.get("end_time"):
            d["end_time"] = datetime.fromisoformat(d["end_time"])  # TODO
        return cls(**d)


class BaseSchedule:
    def __eq__(self, other):
        return (
                isinstance(other, self.__class__)
                and self.id == other.id
        )

    __slots__ = (
        "display_name",
        "id",
        "name",
        "special",
        "static",
    )

    def __init__(
            self,
            *,
            display_name: str,
            id: UUID,
            name: str,
            special: bool,
            static: bool,
    ):
        self.display_name: str = display_name
        self.id: UUID = id
        self.name: str = name
        self.special: bool = special
        self.static: bool = static

    @classmethod
    def from_dict(cls, d: dict):
        d = d.copy()
        d["id"] = UUID(d["id"])
        return cls(**d)


class BellSchedule(BaseSchedule):
    def __init__(
            self,
            *,
            author: BaseStudent,
            author_id: int,
            created_at: datetime,
            display_name: str,
            draft: bool,
            emoji: Emoji | None,
            emoji_id: str | None,
            hidden: bool,
            id: UUID,
            lunch_slot: Any | None,  # Unknown
            lunch_waves: list,  # Unknown
            name: str,
            order: int,
            periods: list[Period],
            school_id: str,
            special: bool,
            static: bool,
            updated_at: datetime,
    ):
        super().__init__(
            display_name=display_name,
            id=id,
            name=name,
            special=special,
            static=static,
        )
        self.author: BaseStudent = author
        self.author_id: int = author_id
        self.created_at: datetime = created_at
        self.draft: bool = draft
        self.emoji: Emoji | None = emoji
        self.emoji_id: str | None = emoji_id
        self.hidden: bool = hidden
        self.lunch_slot: Any | None = lunch_slot
        self.lunch_waves: list = lunch_waves
        self.order: int = order
        self.periods: list[Period] = periods
        self.school_id: str = school_id
        self.updated_at: datetime = updated_at

    __slots__ = BaseSchedule.__slots__ + (
        "author",
        "author_id",
        "created_at",
        "draft",
        "emoji",
        "emoji_id",
        "hidden",
        "lunch_slot",
        "lunch_waves",
        "order",
        "periods",
        "school_id",
        "updated_at",
    )

    @classmethod
    def from_dict(cls, d: dict):
        d = d.copy()
        d["author"] = BaseStudent.from_dict(d["author"])
        d["periods"] = [Period.from_dict(p) for p in d["periods"]]
        d["id"] = UUID(d["id"])
        if d.get("emoji"):
            d["emoji"] = Emoji.from_dict(d["emoji"])
        return cls(**d)


class CalendarDay:
    def __init__(
            self,
            *,
            date: datetime,
            is_cancelled: bool,
            raw_block_name: str,
            schedule: BaseSchedule | None,
    ):
        self.date: datetime = date
        self.is_cancelled: bool = is_cancelled
        self.raw_block_name: str = raw_block_name
        self.schedule: BaseSchedule | None = schedule

    @classmethod
    def from_dict(cls, d: dict):
        d = d.copy()
        d["date"] = datetime.strptime(d["date"], "%Y-%m-%d")
        if d.get("schedule"):
            d["schedule"] = BaseSchedule.from_dict(d["schedule"])
        return cls(**d)


class ScheduleChange:
    def __init__(
            self,
            *,
            count: int,
            desired_schedule: str,
            desired_schedule_id: UUID,
            original_schedule: str,
            original_schedule_id: UUID,
            user_id: int,
    ):
        self.count: int = count
        self.desired_schedule: str = desired_schedule
        self.desired_schedule_id: UUID = desired_schedule_id
        self.original_schedule: str = original_schedule
        self.original_schedule_id: UUID = original_schedule_id
        self.user_id: int = user_id

    __slots__ = (
        "count",
        "desired_schedule",
        "desired_schedule_id",
        "original_schedule",
        "original_schedule_id",
        "user_id",
    )

    @classmethod
    def from_dict(cls, d: dict):
        d = d.copy()
        d["desired_schedule_id"] = UUID(d["desired_schedule_id"])
        d["original_schedule_id"] = UUID(d["original_schedule_id"])
        return cls(**d)


class ScheduleChangeReport:
    def __eq__(self, other):
        return (
                isinstance(other, self.__class__)
                and self.key == other.key
        )

    def __init__(
            self,
            *,
            ambassadors: list[BaseStudent],
            changes: list[ScheduleChange],
            district_school_count: int,
            district_schools: list[str],
            key: int,
            report_count: int,
            school_name: str,
            school_title: str,
            school_state: str,
            status: str,
            target_date: datetime,
            timezone: str,  # We can (possibly) do better.
            upcoming_days: int,
            user_count: int,
    ):
        self.ambassadors: list[BaseStudent] = ambassadors
        self.changes: list[ScheduleChange] = changes
        self.district_school_count: int = district_school_count
        self.district_schools: list[str] = district_schools
        self.key: int = key
        self.report_count: int = report_count
        self.school_name: str = school_name
        self.school_title: str = school_title
        self.school_state: str = school_state
        self.status: str = status
        self.target_date: datetime = target_date
        self.timezone: str = timezone
        self.upcoming_days: int = upcoming_days
        self.user_count: int = user_count

    __slots__ = (
        "ambassadors",
        "changes",
        "district_school_count",
        "district_schools",
        "key",
        "report_count",
        "school_name",
        "school_title",
        "school_state",
        "status",
        "target_date",
        "timezone",
        "upcoming_days",
        "user_count",
    )

    @classmethod
    def from_dict(cls, d: dict):
        d = d.copy()
        d["target_date"] = datetime.strptime(d["target_date"], "%Y-%m-%d")
        d["ambassadors"] = [BaseStudent.from_dict(a) for a in d["ambassadors"]]
        d["changes"] = [ScheduleChange.from_dict(c) for c in d["changes"]]
        return cls(**d)


class FullStudent(Student):
    __slots__ = Student.__slots__ + (
        "updated_at",
        "profile_pic_url",
        "gender",
        "gender_preference",
        "onboarded",
        "phone_number",
        "phone_validated",
        "tags",
        "granted_scopes",
        "school_id",
        "referred_by",
        "ambassador_school_id",
        "hashid",
        "school_title",
        "school",
        "waitlist_school",
        "courses",
        "permissions",
    )

    def __init__(
            self,
            *,
            updated_at: datetime | None,
            profile_pic_url: str,
            gender: Any | None,  # Unknown
            gender_preference: Any | None,  # Unknown
            onboarded: bool,
            phone_number: str,
            phone_validated: bool,
            tags: list[Any],  # Unknown
            granted_scopes: list[Any],  # Unknown
            school_id: str,
            referred_by: Any | None,  # Unknown
            ambassador_school_id: Any | None,  # Unknown
            hashid: str,
            school_title: str,
            school: str,
            waitlist_school: Any | None,  # Unknown
            courses: list[DefinedCourse],
            permissions: dict[str, bool],
            **kwargs,
    ):
        super().__init__(**kwargs)
        self.updated_at: datetime = updated_at
        self.profile_pic_url: str = profile_pic_url
        self.gender: Any | None = gender
        self.gender_preference: Any | None = gender_preference
        self.onboarded: bool = onboarded
        self.phone_number: str = phone_number
        self.phone_validated: bool = phone_validated
        self.tags: list[Any] = tags
        self.granted_scopes: list[Any] = granted_scopes
        self.school_id: str = school_id
        self.referred_by: Any | None = referred_by
        self.ambassador_school_id: Any | None = ambassador_school_id
        self.hashid: str = hashid
        self.school_title: str = school_title
        self.school: str = school
        self.waitlist_school: Any | None = waitlist_school
        self.courses: list[DefinedCourse] = courses
        self.permissions: dict[str, bool] = permissions

    @classmethod
    def from_dict(cls, d: dict):
        d = d.copy()
        if d.get("updated_at"):
            d["updated_at"] = datetime.fromisoformat(d["updated_at"])
        else:
            d["updated_at"] = None
        d["courses"] = [DefinedCourse.from_dict(c) for c in d["courses"]]
        return cls(**d)


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
)
