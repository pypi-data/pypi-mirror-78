import pyexlatex as pl
import pyexlatex.resume as lr

from derobertis_cv import plbuild
from derobertis_cv.plbuild.paths import images_path
from derobertis_cv.pldata.constants.contact import CONTACT_LINES
from derobertis_cv.pldata.cv import CVModel, get_cv_contents, ResumeSection
from derobertis_cv.pldata.software.config import ACADEMIC_INCLUDED_SOFTWARE_PROJECTS

AUTHORS = ['Nick DeRobertis']

DOCUMENT_CLASS = lr.Resume
OUTPUT_LOCATION = plbuild.paths.DOCUMENTS_BUILD_PATH
HANDOUTS_OUTPUT_LOCATION = None


SECTIONS = [
    ResumeSection.RESEARCH_INTERESTS,
    pl.VSpace(0.2),
    ResumeSection.EDUCATION,
    pl.VSpace(0.2),
    ResumeSection.ACADEMIC_EXPERIENCE,
    ResumeSection.PROFESSIONAL_EXPERIENCE,
    ResumeSection.WORKING_PAPERS,
    pl.VSpace(0.2),
    ResumeSection.WORKS_IN_PROGRESS,
    pl.VSpace(0.2),
    ResumeSection.AWARDS_GRANTS,
    pl.VSpace(0.4),
    ResumeSection.SOFTWARE_PROJECTS,
    ResumeSection.REFERENCES
]


def get_content():
    model = CVModel(
        SECTIONS,
        included_software_projects=ACADEMIC_INCLUDED_SOFTWARE_PROJECTS,
        professional_section_name='Other Professional Experience',
    )
    contents = get_cv_contents(model)
    return contents

DOCUMENT_CLASS_KWARGS = dict(
    contact_lines=CONTACT_LINES
)
OUTPUT_NAME = f'{AUTHORS[0]} CV'
