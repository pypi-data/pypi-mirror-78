import pyexlatex as pl
import pyexlatex.resume as lr

from derobertis_cv import plbuild
from derobertis_cv.plbuild.paths import images_path
from derobertis_cv.pldata.constants.contact import CONTACT_LINES
from derobertis_cv.pldata.cv import CVModel, get_cv_contents, ResumeSection
from derobertis_cv.pldata.software.config import EXCLUDED_SOFTWARE_PROJECTS, PROFESSIONAL_SOFTWARE_PROJECT_ORDER

AUTHORS = ['Nick DeRobertis']

DOCUMENT_CLASS = lr.Resume
OUTPUT_LOCATION = plbuild.paths.DOCUMENTS_BUILD_PATH
HANDOUTS_OUTPUT_LOCATION = None


SECTIONS = [
    ResumeSection.OVERVIEW,
    pl.VSpace(0.2),
    ResumeSection.EDUCATION,
    pl.VSpace(0.2),
    ResumeSection.PROFESSIONAL_EXPERIENCE,
    ResumeSection.ACADEMIC_EXPERIENCE,
    ResumeSection.SKILLS,
    pl.VSpace(0.2),
    ResumeSection.WORKING_PAPERS,
    pl.VSpace(0.2),
    ResumeSection.WORKS_IN_PROGRESS,
    pl.VSpace(0.2),
    ResumeSection.AWARDS_GRANTS,
    pl.VSpace(0.4),
    ResumeSection.SOFTWARE_PROJECTS,
]


def get_content():
    model = CVModel(
        SECTIONS,
        excluded_software_projects=EXCLUDED_SOFTWARE_PROJECTS,
        software_project_order=PROFESSIONAL_SOFTWARE_PROJECT_ORDER,
        include_private_jobs=True,
    )
    contents = get_cv_contents(model)
    return contents

DOCUMENT_CLASS_KWARGS = dict(
    contact_lines=CONTACT_LINES
)
OUTPUT_NAME = f'{AUTHORS[0]} Professional CV'
