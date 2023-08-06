from dataclasses import dataclass
from enum import Enum
from typing import List, Sequence, Optional, Union

import pyexlatex as pl
import pyexlatex.resume as lr
from pyexlatex.models.item import ItemBase

from derobertis_cv.pldata.jobs import (
    get_professional_jobs,
    get_academic_jobs
)
from derobertis_cv.pldata.education import get_education
from derobertis_cv.pldata.papers import (
    get_working_papers,
    get_works_in_progress, ResearchProjectModel
)
from derobertis_cv.pldata.skills import get_skills, get_skills_str_list
from derobertis_cv.pldata.software import get_software_projects
from derobertis_cv.pldata.awards import get_awards
from derobertis_cv.pldata.interests import get_research_interests
from derobertis_cv.pldata.references import get_references
from derobertis_cv.pltemplates.software.section import SoftwareSection


class ResumeSection(Enum):
    RESEARCH_INTERESTS = 'research interests'
    EDUCATION = 'education'
    ACADEMIC_EXPERIENCE = 'academic experience'
    PROFESSIONAL_EXPERIENCE = 'professional experience'
    WORKING_PAPERS = 'working papers'
    WORKS_IN_PROGRESS = 'works in progress'
    AWARDS_GRANTS = 'awards and grants'
    SOFTWARE_PROJECTS = 'software projects'
    REFERENCES = 'references'
    SKILLS = 'skills'
    OVERVIEW = 'overview'


@dataclass
class CVModel:
    sections: List[Union[ResumeSection, ItemBase]]
    included_software_projects: Optional[Sequence[str]] = None
    excluded_software_projects: Optional[Sequence[str]] = None
    software_project_order: Optional[Sequence[str]] = None
    excluded_companies: Optional[Sequence[str]] = None
    exclude_skills: Optional[Sequence[str]] = None
    exclude_skill_children: bool = True
    skill_order: Optional[Sequence[str]] = None
    professional_section_name: str = 'Professional Experience'
    overview_text: str = (
        'An entrepreneur, full-stack web engineer and architect, data scientist, empirical researcher, and '
        'project manager with a track record of building, deploying, and managing open- and '
        'closed-source applications and research projects.'
    )
    include_private_jobs: bool = False

    def __post_init__(self):
        if self.software_project_order is None and self.included_software_projects is not None:
            self.software_project_order = self.included_software_projects
        self._validate()

    def _validate(self):
        if self.included_software_projects is not None and self.excluded_software_projects is not None:
            raise ValueError('cannot have both included and excluded software projects')


def get_cv_contents(model: CVModel) -> List[ItemBase]:
    lr_jobs = [
        job.to_pyexlatex_employment() for job in get_professional_jobs(
            excluded_companies=model.excluded_companies,
            include_private=model.include_private_jobs,
        )
    ]

    all_contents = {
        ResumeSection.RESEARCH_INTERESTS: pl.Section(
            get_research_interests(),
            title='Research Interests'
        ),
        ResumeSection.EDUCATION: lr.SpacedSection(
            get_education(),
            title='Education'
        ),
        ResumeSection.ACADEMIC_EXPERIENCE: pl.Section(
            get_academic_jobs(),
            title='Academic Experience'
        ),
        ResumeSection.PROFESSIONAL_EXPERIENCE: pl.Section(
            lr_jobs,
            title=model.professional_section_name
        ),
        ResumeSection.WORKING_PAPERS: lr.SpacedSection(
            ResearchProjectModel.list_to_pyexlatex_publication_list(get_working_papers()),
            title='Working Papers'
        ),
        ResumeSection.WORKS_IN_PROGRESS: lr.SpacedSection(
            ResearchProjectModel.list_to_pyexlatex_publication_list(get_works_in_progress()),
            title='Works in Progress'
        ),
        ResumeSection.AWARDS_GRANTS: lr.SpacedSection(
            [award.to_pyexlatex_award() for award in get_awards()],
            title='Awards and Grants'
        ),
        ResumeSection.SOFTWARE_PROJECTS: SoftwareSection(
            get_software_projects(
                include_projects=model.included_software_projects,
                exclude_projects=model.excluded_software_projects,
                order=model.software_project_order,
            ),
            title='Software Projects',
            compact=True
        ),
        ResumeSection.REFERENCES: lr.SpacedSection(
            [
                pl.TextSize(-1),
                get_references(),
            ],
            title='References',
            num_cols=2
        ),
        ResumeSection.SKILLS: pl.Section(
            get_skills_str_list(
                exclude_skills=model.exclude_skills,
                exclude_skill_children=model.exclude_skill_children,
                order=model.skill_order,
            ),
            title='Skills'
        ),
        ResumeSection.OVERVIEW: pl.Section(
            model.overview_text,
            title='Overview'
        )
    }

    selected_contents = []
    for section in model.sections:
        if isinstance(section, ResumeSection):
            selected_contents.append(all_contents[section])
        else:
            selected_contents.append(section)

    return selected_contents