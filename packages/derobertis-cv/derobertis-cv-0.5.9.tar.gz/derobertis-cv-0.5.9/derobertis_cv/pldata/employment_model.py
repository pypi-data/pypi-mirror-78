import datetime
from dataclasses import dataclass
from typing import Any, Optional

import pyexlatex.resume as lr


@dataclass
class EmploymentModel:
    contents: Any
    company_name: str
    job_title: str
    location: str
    employ_begin_date: datetime.date
    employ_end_date: Optional[datetime.date] = None
    date_format: str = "%B %Y"

    @property
    def begin_date_str(self) -> str:
        return self.employ_begin_date.strftime(self.date_format)

    @property
    def end_date_str(self) -> str:
        if self.employ_end_date is None:
            return "Present"
        return self.employ_end_date.strftime(self.date_format)

    @property
    def date_str(self) -> str:
        return f"{self.begin_date_str} - {self.end_date_str}"

    @property
    def sort_key(self) -> datetime.date:
        if self.employ_end_date is not None:
            return self.employ_end_date
        return datetime.datetime.now()

    def to_pyexlatex_employment(self) -> lr.Employment:
        return lr.Employment(
            self.contents,
            self.company_name,
            self.date_str,
            self.job_title,
            self.location,
        )
