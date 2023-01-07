from typing import NamedTuple

url = str


class Social(NamedTuple):
    name: str | None
    link: url | None


class Founder(NamedTuple):
    full_name: str | None
    socials: tuple[Social]


class Company(NamedTuple):
    name: str | None
    link: url | None
    socials: tuple[Social]
    founders: tuple[Founder]
