from copy import deepcopy
from typing import Sequence, Optional, List, Dict, cast, Set

from pyexlatex.logic.format.and_join import join_with_commas_and_and_output_list

from derobertis_cv.models.skill import SkillModel
from derobertis_cv.models.cased import first_word_untouched_rest_capitalized, \
    first_word_untouched_rest_lower, first_word_untouched_rest_title


def _recursive_sort_skills(skills: List[SkillModel], **sort_kwargs):
    skills.sort(**sort_kwargs)
    for skill in skills:
        _recursive_sort_skills(skill.children, **sort_kwargs)


PROGRAMMING_SKILL = SkillModel('Programming', 5)
SOFTWARE_ARCHITECTURE_SKILL = SkillModel('software architecture', 4)
OS_SKILL = SkillModel('operating systems', 3)
HARDWARE_SKILL = SkillModel('computer hardware', 3)
SOFTWARE_DEVELOPMENT_SKILL = SkillModel('software development', 5, parents=(PROGRAMMING_SKILL,))
FRONTEND_SKILL = SkillModel('Front-end Development', 4, parents=(SOFTWARE_DEVELOPMENT_SKILL, SOFTWARE_ARCHITECTURE_SKILL))
BACKEND_SKILL = SkillModel('Back-end Development', 5, parents=(SOFTWARE_DEVELOPMENT_SKILL, SOFTWARE_ARCHITECTURE_SKILL))
CLI_SKILL = SkillModel(
    'CLI Development',
    3,
    parents=(SOFTWARE_DEVELOPMENT_SKILL, SOFTWARE_ARCHITECTURE_SKILL),
    case_capitalize_func=first_word_untouched_rest_capitalized,
    case_lower_func=first_word_untouched_rest_lower,
    case_title_func=first_word_untouched_rest_title,
)
DATABASE_SKILL = SkillModel('Databases', 4, parents=(PROGRAMMING_SKILL,))
DEV_OPS_SKILL = SkillModel('Dev-Ops', 4, parents=(PROGRAMMING_SKILL,))
REMOTE_DEVELOPMENT_SKILL = SkillModel('Remote development', 3, parents=(PROGRAMMING_SKILL,))
SECURITY_SKILL = SkillModel('Security', 3, parents=(PROGRAMMING_SKILL, SOFTWARE_ARCHITECTURE_SKILL))
WEB_DEVELOPMENT_SKILL = SkillModel(
    'Web Development',
    4,
    parents=(SOFTWARE_DEVELOPMENT_SKILL, SOFTWARE_ARCHITECTURE_SKILL, REMOTE_DEVELOPMENT_SKILL, SECURITY_SKILL),
)
CSS_SKILL = SkillModel('CSS', 3, parents=(WEB_DEVELOPMENT_SKILL, FRONTEND_SKILL), flexible_case=False)
FRAMEWORK_SKILL = SkillModel('Frameworks', 5, parents=(PROGRAMMING_SKILL,))
DEBUGGING_SKILL = SkillModel('Debugging', 4, parents=(PROGRAMMING_SKILL,))
TESTING_SKILL = SkillModel('Automated testing', 4, parents=(PROGRAMMING_SKILL,))
PARALLELISM_SKILL = SkillModel('Parallelism', 4, parents=(PROGRAMMING_SKILL,))
CRYPTOGRAPHY_SKILL = SkillModel('Cryptography', 3, parents=(PROGRAMMING_SKILL, SECURITY_SKILL))
ASYNC_SKILL = SkillModel('Asynchronous Programming', 4, parents=(PROGRAMMING_SKILL,))
DISTRIBUTED_SKILL = SkillModel('Distributed Computing', 4, parents=(REMOTE_DEVELOPMENT_SKILL,))
EXCEL_SKILL = SkillModel('Excel', 4, flexible_case=False)
AUTOMATION_SKILL = SkillModel('automation', 5, parents=(PROGRAMMING_SKILL,))
SERVER_ADMIN_SKILL = SkillModel('server administration', 4, parents=(DEV_OPS_SKILL, WEB_DEVELOPMENT_SKILL))
NETWORKING_SKILL = SkillModel('networking', 3, parents=(DEV_OPS_SKILL,))
MONITORING_SKILL = SkillModel('application monitoring', 2, parents=(DEV_OPS_SKILL,))
CI_SKILL = SkillModel('CI/CD', 4, parents=(DEV_OPS_SKILL,), flexible_case=False)
SEO_SKILL = SkillModel('SEO', 2, parents=(WEB_DEVELOPMENT_SKILL,), flexible_case=False)
CMS_SKILL = SkillModel('CMS', 4, parents=(WEB_DEVELOPMENT_SKILL,), flexible_case=False)
MIGRATIONS_SKILL = SkillModel('migrations', 5, parents=(DATABASE_SKILL,))
IDE_SKILL = SkillModel('IDEs', 4, parents=(PROGRAMMING_SKILL,), flexible_case=False)


LINUX_SKILL = SkillModel('Linux', 4, parents=(OS_SKILL,), flexible_case=False)
WINDOWS_SKILL = SkillModel('Windows', 4, parents=(OS_SKILL,), flexible_case=False)

PRESENTATION_SKILL = SkillModel('presentation', 4)
TYPE_SETTING_SKILL = SkillModel('Typesetting', 4, parents=(PRESENTATION_SKILL,))
WRITING_SKILL= SkillModel('Writing', 4)
RESEARCH_SKILL = SkillModel('Research', 5)
STATISTICS_SKILL = SkillModel('Statistics', 5)
MODELING_SKILL = SkillModel('Modeling', 4)
VERSION_CONTORL_SKILL = SkillModel('Version Control', 4)
COLLABORATION_SKILL = SkillModel('Collaboration', 5)
ENTREPRENEURSHIP_SKILL = SkillModel('Entrepreneurship', 5)
PARSING_SKILL = SkillModel('Parsing', 4, parents=(PROGRAMMING_SKILL,))
TIME_SERIES_SKILL = SkillModel('Time-Series', 3, parents=(STATISTICS_SKILL,))
FORECASTING_SKILL = SkillModel('Forecasting', 3, parents=(TIME_SERIES_SKILL,))
WEB_SCRAPING_SKILL = SkillModel('Web-scraping', 4, parents=(PROGRAMMING_SKILL, AUTOMATION_SKILL))
DOCUMENTATION_SKILL = SkillModel('documentation', 4, parents=(PROGRAMMING_SKILL, PRESENTATION_SKILL, TYPE_SETTING_SKILL))
TEMPLATING_SKILL = SkillModel('templating', 5, parents=(PROGRAMMING_SKILL, PRESENTATION_SKILL, TYPE_SETTING_SKILL))


OPEN_SOURCE_SKILL = SkillModel('Open-Source Development', 5, parents=(PROGRAMMING_SKILL, COLLABORATION_SKILL))
DATA_SCIENCE_SKILL = SkillModel(
    'Data Science',
    4,
    parents=(PROGRAMMING_SKILL, RESEARCH_SKILL, STATISTICS_SKILL, MODELING_SKILL)
)
MACHINE_LEARNING_SKILL = SkillModel('machine learning', 3, parents=(DATA_SCIENCE_SKILL,))
DATA_MUNGING_SKILL = SkillModel('data munging', 5, parents=(DATA_SCIENCE_SKILL,))
DATA_ANALYSIS_SKILL = SkillModel('Data Analysis', 5, parents=(DATA_SCIENCE_SKILL,))
VISUALIZATION_SKILL = SkillModel('visualization', 4, parents=(DATA_SCIENCE_SKILL, PRESENTATION_SKILL))
PLOTTING_SKILL = SkillModel('plotting', 4, parents=(PROGRAMMING_SKILL, PRESENTATION_SKILL, VISUALIZATION_SKILL))


PYTHON_SKILL = SkillModel('Python', 5, parents=(PROGRAMMING_SKILL,), flexible_case=False)
JS_SKILL = SkillModel('JavaScript', 4, parents=(PROGRAMMING_SKILL,), flexible_case=False)
TS_SKILL = SkillModel('TypeScript', 4, parents=(JS_SKILL,), flexible_case=False)
AWS_SKILL = SkillModel('AWS', 3, parents=(DEV_OPS_SKILL, WEB_DEVELOPMENT_SKILL, REMOTE_DEVELOPMENT_SKILL), flexible_case=False)

DS_FRAMEWORK_SKILLS = (FRAMEWORK_SKILL, PYTHON_SKILL, DATA_SCIENCE_SKILL)
BE_WEB_FRAMEWORK_SKILLS = (FRAMEWORK_SKILL, PYTHON_SKILL, WEB_DEVELOPMENT_SKILL, BACKEND_SKILL)
FE_TS_WEB_FRAMEWORK_SKILLS = (FRAMEWORK_SKILL, TS_SKILL, WEB_DEVELOPMENT_SKILL, FRONTEND_SKILL)
FULL_STACK_WEB_PYTHON_FRAMEWORK_SKILLS = BE_WEB_FRAMEWORK_SKILLS + (FRONTEND_SKILL,)
WEB_SCRAPING_FRAMEWORK_SKILLS = (FRAMEWORK_SKILL, WEB_SCRAPING_SKILL, PYTHON_SKILL)
PARSING_FRAMEWORK_SKILLS = (FRAMEWORK_SKILL, PARSING_SKILL, PYTHON_SKILL)
ASYNC_FRAMEWORK_SKILLS = (FRAMEWORK_SKILL, PYTHON_SKILL, ASYNC_SKILL)


_SKILLS: List[SkillModel] = [
    PROGRAMMING_SKILL,
    DATA_ANALYSIS_SKILL,
    DATA_MUNGING_SKILL,
    SOFTWARE_ARCHITECTURE_SKILL,
    OS_SKILL,
    SOFTWARE_DEVELOPMENT_SKILL,
    FRONTEND_SKILL,
    BACKEND_SKILL,
    CLI_SKILL,
    DATABASE_SKILL,
    DEV_OPS_SKILL,
    REMOTE_DEVELOPMENT_SKILL,
    SECURITY_SKILL,
    WEB_DEVELOPMENT_SKILL,
    CSS_SKILL,
    FRAMEWORK_SKILL,
    DEBUGGING_SKILL,
    TESTING_SKILL,
    PARALLELISM_SKILL,
    CRYPTOGRAPHY_SKILL,
    ASYNC_SKILL,
    DISTRIBUTED_SKILL,
    EXCEL_SKILL,
    AUTOMATION_SKILL,
    SERVER_ADMIN_SKILL,
    NETWORKING_SKILL,
    MONITORING_SKILL,
    CI_SKILL,
    LINUX_SKILL,
    WINDOWS_SKILL,
    PRESENTATION_SKILL,
    TYPE_SETTING_SKILL,
    WRITING_SKILL,
    RESEARCH_SKILL,
    STATISTICS_SKILL,
    MODELING_SKILL,
    VERSION_CONTORL_SKILL,
    COLLABORATION_SKILL,
    ENTREPRENEURSHIP_SKILL,
    PARSING_SKILL,
    TIME_SERIES_SKILL,
    FORECASTING_SKILL,
    WEB_SCRAPING_SKILL,
    DOCUMENTATION_SKILL,
    TEMPLATING_SKILL,
    PLOTTING_SKILL,
    OPEN_SOURCE_SKILL,
    DATA_SCIENCE_SKILL,
    MACHINE_LEARNING_SKILL,
    PYTHON_SKILL,
    JS_SKILL,
    TS_SKILL,
    AWS_SKILL,
    SEO_SKILL,
    CMS_SKILL,
    MIGRATIONS_SKILL,
    HARDWARE_SKILL,
    IDE_SKILL,
    SkillModel('SQL', 4, parents=(DATABASE_SKILL,), flexible_case=False),
    SkillModel('Redis', 4, parents=(DATABASE_SKILL,), flexible_case=False),
    SkillModel('Angular', 4, parents=FE_TS_WEB_FRAMEWORK_SKILLS, flexible_case=False),
    SkillModel('React', 1, parents=FE_TS_WEB_FRAMEWORK_SKILLS, flexible_case=False),
    SkillModel('Docker', 4, parents=(DEV_OPS_SKILL,), flexible_case=False),
    SkillModel('LaTeX', 4, parents=(TYPE_SETTING_SKILL, RESEARCH_SKILL), flexible_case=False),
    SkillModel('SAS', 3, parents=(PROGRAMMING_SKILL,), flexible_case=False),
    SkillModel('Stata', 4, parents=(PROGRAMMING_SKILL,), flexible_case=False),
    SkillModel('MATLAB', 1, parents=(PROGRAMMING_SKILL,), flexible_case=False),
    SkillModel('NoSQL', 2, parents=(DATABASE_SKILL,), flexible_case=False),
    SkillModel('Git', 4, parents=(VERSION_CONTORL_SKILL,), flexible_case=False),
    SkillModel('Bash', 3, parents=(PROGRAMMING_SKILL,), flexible_case=False),

    SkillModel('EC2', 4, parents=(AWS_SKILL, SERVER_ADMIN_SKILL), flexible_case=False),
    SkillModel('RDS', 3, parents=(AWS_SKILL, DATABASE_SKILL), flexible_case=False),
    SkillModel('VPC', 3, parents=(AWS_SKILL, NETWORKING_SKILL), flexible_case=False),
    SkillModel('Route53', 3, parents=(AWS_SKILL, NETWORKING_SKILL), flexible_case=False),
    SkillModel('S3', 3, parents=(AWS_SKILL, DATABASE_SKILL), flexible_case=False),
    SkillModel('ElastiCache', 3, parents=(AWS_SKILL, DATABASE_SKILL), flexible_case=False),
    SkillModel('IAM', 3, parents=(AWS_SKILL, COLLABORATION_SKILL), flexible_case=False),
    SkillModel('CloudWatch', 3, parents=(AWS_SKILL, MONITORING_SKILL), flexible_case=False),
    SkillModel('CloudFormation', 2, parents=(AWS_SKILL, SERVER_ADMIN_SKILL, NETWORKING_SKILL), flexible_case=False),

    SkillModel('JIRA', 4, parents=(WEB_DEVELOPMENT_SKILL, COLLABORATION_SKILL), flexible_case=False),

    SkillModel('PyCharm', 4, parents=(IDE_SKILL,), flexible_case=False),
    SkillModel('VS Code', 4, parents=(IDE_SKILL,), flexible_case=False),

    SkillModel(
        'empirical research', 5, parents=(RESEARCH_SKILL, STATISTICS_SKILL, DATA_ANALYSIS_SKILL, DATA_MUNGING_SKILL)
    ),

    SkillModel('Github Actions', 4, parents=(CI_SKILL,), flexible_case=False),
    SkillModel('Gitlab CI', 3, parents=(CI_SKILL,), flexible_case=False),

    SkillModel('econometrics', 4, parents=(STATISTICS_SKILL,)),
    SkillModel('project management', 4),
    SkillModel('Quality assurance', 3),
    SkillModel('HTML', 4, parents=(WEB_DEVELOPMENT_SKILL, FRONTEND_SKILL, TYPE_SETTING_SKILL), flexible_case=False),
    SkillModel('Sass', 3, parents=(CSS_SKILL,), flexible_case=False),
    SkillModel('Bootstrap', 3, parents=(CSS_SKILL, JS_SKILL, FRAMEWORK_SKILL), flexible_case=False),
    SkillModel('Material Design', 2, parents=(CSS_SKILL, JS_SKILL, FRAMEWORK_SKILL), flexible_case=False),
    SkillModel('jQuery', 2, parents=(JS_SKILL, FRAMEWORK_SKILL), flexible_case=False),

    SkillModel('pandas', 5, parents=DS_FRAMEWORK_SKILLS + (DATA_ANALYSIS_SKILL, DATA_MUNGING_SKILL), flexible_case=False),
    SkillModel('NumPy', 4, parents=DS_FRAMEWORK_SKILLS + (DATA_ANALYSIS_SKILL, DATA_MUNGING_SKILL), flexible_case=False),
    SkillModel('SciPy', 3, parents=DS_FRAMEWORK_SKILLS + (DATA_ANALYSIS_SKILL,), flexible_case=False),
    SkillModel('SymPy', 4, parents=DS_FRAMEWORK_SKILLS + (DATA_ANALYSIS_SKILL,), flexible_case=False),
    SkillModel('scikit-learn', 3, parents=DS_FRAMEWORK_SKILLS + (MACHINE_LEARNING_SKILL, DATA_ANALYSIS_SKILL), flexible_case=False),
    SkillModel('Jupyter', 4, parents=DS_FRAMEWORK_SKILLS + (IDE_SKILL,), flexible_case=False),
    SkillModel('Matplotlib', 4, parents=DS_FRAMEWORK_SKILLS + (PLOTTING_SKILL,), flexible_case=False),
    SkillModel('HoloViews', 3, parents=DS_FRAMEWORK_SKILLS + (PLOTTING_SKILL,), flexible_case=False),

    SkillModel('Flask', 5, parents=BE_WEB_FRAMEWORK_SKILLS, flexible_case=False),
    SkillModel('Django', 2, parents=BE_WEB_FRAMEWORK_SKILLS, flexible_case=False),
    SkillModel('SQLAlchemy', 5, parents=BE_WEB_FRAMEWORK_SKILLS, flexible_case=False),

    SkillModel('Celery', 4, parents=ASYNC_FRAMEWORK_SKILLS, flexible_case=False),

    SkillModel('Requests', 4, parents=WEB_SCRAPING_FRAMEWORK_SKILLS, flexible_case=False),
    SkillModel('Selenium', 4, parents=WEB_SCRAPING_FRAMEWORK_SKILLS, flexible_case=False),
    SkillModel('Beautiful Soup', 2, parents=PARSING_FRAMEWORK_SKILLS, flexible_case=False),
    SkillModel('lxml', 4, parents=PARSING_FRAMEWORK_SKILLS, flexible_case=False),

    SkillModel('Panel', 4, parents=FULL_STACK_WEB_PYTHON_FRAMEWORK_SKILLS, flexible_case=False),
    SkillModel('Dash', 2, parents=FULL_STACK_WEB_PYTHON_FRAMEWORK_SKILLS, flexible_case=False),
    SkillModel('Sphinx', 4, parents=FULL_STACK_WEB_PYTHON_FRAMEWORK_SKILLS + (DOCUMENTATION_SKILL,), flexible_case=False),

    SkillModel('Pelican', 3, parents=FULL_STACK_WEB_PYTHON_FRAMEWORK_SKILLS + (CMS_SKILL,), flexible_case=False),
    SkillModel('Wagtail', 2, parents=FULL_STACK_WEB_PYTHON_FRAMEWORK_SKILLS + (CMS_SKILL,), flexible_case=False),

    SkillModel('Jinja2', 4, parents=(FRAMEWORK_SKILL, PYTHON_SKILL, TEMPLATING_SKILL), flexible_case=False),
    SkillModel('pytest', 4, parents=(FRAMEWORK_SKILL, PYTHON_SKILL, TESTING_SKILL), flexible_case=False),

    SkillModel('Grafana', 2, parents=(FRAMEWORK_SKILL, MONITORING_SKILL), flexible_case=False),
    SkillModel('Prometheus', 2, parents=(FRAMEWORK_SKILL, MONITORING_SKILL, DATABASE_SKILL), flexible_case=False),

    SkillModel('xlwings', 4, parents=(FRAMEWORK_SKILL, PYTHON_SKILL, EXCEL_SKILL, AUTOMATION_SKILL), flexible_case=False),
    SkillModel('fire', 3, parents=(FRAMEWORK_SKILL, PYTHON_SKILL, CLI_SKILL), flexible_case=False),
]

_recursive_sort_skills(_SKILLS, key=lambda skill: skill.level, reverse=True)

SKILLS: Dict[str, SkillModel] = {skill.to_lower_case_str(): skill for skill in _SKILLS}


def get_skills(exclude_skills: Optional[Sequence[str]] = None,
               exclude_skill_children: bool = True,
               order: Optional[Sequence[str]] = None) -> List[SkillModel]:
    if exclude_skills is None:
        exclude_skills = []

    skills = [skill for key, skill in SKILLS.items() if key not in exclude_skills]
    if not exclude_skill_children:
        use_skills = skills
    else:
        child_excluded_skills: Set[SkillModel] = set()
        for skill_name in exclude_skills:
            skill = SKILLS[skill_name]
            children = cast(Set[SkillModel], skill.get_nested_children())
            child_excluded_skills.update(children)
        child_excluded_skill_names = {child.to_lower_case_str() for child in child_excluded_skills}
        use_skills = [skill for skill in skills if skill.to_lower_case_str() not in child_excluded_skill_names]

    if order is not None:
        _recursive_sort_skills(
            use_skills,
            key=lambda skill: order.index(skill.to_lower_case_str())
            if skill.to_lower_case_str() in order else 100000 - skill.level  # type: ignore
        )

    return use_skills


def get_skills_str_list(exclude_skills: Optional[Sequence[str]] = None, exclude_skill_children: bool = True,
                   order: Optional[Sequence[str]] = None) -> List[str]:
    skills = get_skills(
        exclude_skills=exclude_skills,
        exclude_skill_children=exclude_skill_children,
        order=order
    )
    formatted_skills = [skills[0].to_capitalized_str()] + [skill.to_lower_case_str() for skill in skills[1:]]
    joined = join_with_commas_and_and_output_list(formatted_skills)
    return joined
