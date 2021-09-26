from dataclasses import dataclass
from typing import Optional
from mkcommit.validators import matches, validate_initials


@dataclass
class Text:
    text: str

    def check(self, pattern) -> bool:
        return matches(pattern)(self.text)


@dataclass
class Keyword:
    keyword: str
    description: str


@dataclass
class Project:
    name: str
    ticket_system_id: str
    description: Optional[str] = ""


@dataclass
class Initials:
    initials: str
    first_chars: int
    last_chars: int

    def check(self) -> bool:
        return validate_initials(
            self.first_chars,
            self.last_chars
        )(self.initials)
