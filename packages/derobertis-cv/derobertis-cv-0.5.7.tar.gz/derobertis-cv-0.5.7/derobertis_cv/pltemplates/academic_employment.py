from typing import Optional, Sequence, Union, Any
import pyexlatex as pl
import pyexlatex.resume as lr


class AcademicEmployment(lr.Employment):

    def __init__(self, contents, company_name: str, employed_dates: str, job_title: str, location: str,
                 courses_taught: Optional[Sequence[Union[str, Sequence[str]]]] = None,
                 extra_contents: Optional[Any] = None):
        if extra_contents is None:
            extra_contents = []

        if courses_taught is not None:
            # TODO [#2]: don't use raw, use latex objects
            taught_bullet_contents = []
            for course in courses_taught:
                if isinstance(course, (list, tuple)):
                    from pyexlatex.logic.builder import _build
                    # Put each part of course taught on left and right side
                    course_item_str = _build([
                        ' '.join(course[:-1]),
                        pl.Raw(r'\itemsep -0.5em \vspace{-0.5em}'),
                        pl.UnorderedList(['Semesters: ' + course[-1]]),
                    ])
                    taught_bullet_contents.append(course_item_str)
                else:
                    taught_bullet_contents.append(course)
                taught_bullet_contents.append(pl.Raw(r'\itemsep -0.3em \vspace{-0.3em}'))
            del taught_bullet_contents[-1]  # remove spacing after last item
            taught_contents = [
                '',
                pl.Bold('Courses taught:'),
                pl.Raw(r'\itemsep -0.5em \vspace{-0.5em}'),
                pl.UnorderedList(taught_bullet_contents)
            ]
            extra_contents[:0] = taught_contents

        super().__init__(
            contents,
            company_name=company_name,
            employed_dates=employed_dates,
            job_title=job_title,
            location=location,
            extra_contents=extra_contents
        )