from typing import Optional, Sequence
from derobertis_cv.pltemplates.coauthor import CoAuthor
from derobertis_cv.pldata.constants.institutions import UF_NAME, UF_CONTACT_LINES, ALABAMA, ALABAMA_CONTACT_LINES
from derobertis_cv.pldata.constants.authors import (
    AT_WARRINGTON,
    ASSISTANT_PROF,
    ANDY,
    NIMAL,
    NITISH,
    SUGATA,
    CORBIN,
    JIMMY
)


class Author:

    def __init__(self, name: str, author_key: str, title_lines: Optional[Sequence[str]] = None,
                 company: Optional[str] = None,
                 contact_lines: Optional[Sequence[str]] = None, email: Optional[str] = None):
        self.name = name
        self.author_key = author_key
        self.title_lines = title_lines
        self.company = company
        self.contact_lines = contact_lines
        self.email = email

    @property
    def name_as_doctor(self) -> str:
        return f'Dr. {self.name}'

authors = [
    Author(
        'Andy Naranjo',
        ANDY,
        title_lines=[
            'John B. Hall Professor of Finance & Chairman',
        ],
        company=UF_NAME,
        contact_lines=UF_CONTACT_LINES + ['(352) 392-3781'],
        email=f'andy.naranjo{AT_WARRINGTON}',
    ),
    Author(
        'Mahendrarajah Nimalendran',
        NIMAL,
        title_lines=[
            'John H. and Mary Lou Dasburg Chair Full Professor'
        ],
        company=UF_NAME,
        contact_lines=UF_CONTACT_LINES + ['(352) 392-9526'],
        email=f'mahen.nimalendran{AT_WARRINGTON}',
    ),
    Author(
        'Nitish Kumar',
        NITISH,
        title_lines=[
            ASSISTANT_PROF
        ],
        company=UF_NAME,
        contact_lines=UF_CONTACT_LINES + ['(352) 392-0115'],
        email=f'nitish.kumar{AT_WARRINGTON}',
    ),
    Author(
        'Sugata Ray',
        SUGATA,
        title_lines=[
            ASSISTANT_PROF
        ],
        company=ALABAMA,
        contact_lines=ALABAMA_CONTACT_LINES + ['(205) 348-5726'],
        email=f'sray6@cba.ua.edu',
    ),
    Author(
        'Yong Jin',
        JIMMY
    ),
    Author(
        'Corbin Fox',
        CORBIN
    )
]

CO_AUTHORS = {author.author_key: CoAuthor(author.name) for author in authors}
AUTHORS = {author.author_key: author for author in authors}