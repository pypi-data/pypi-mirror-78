from weakref import WeakSet
from dataclasses import dataclass, field
from typing import Optional, Sequence, List, Set, Callable

from weakreflist import WeakList

from derobertis_cv.models.cased import CasedModel
from derobertis_cv.models.category import CategoryModel
from derobertis_cv.models.nested import NestedModel
from derobertis_cv.pltemplates.logo import HasLogo


@dataclass(frozen=True)
class SkillModel(CasedModel, NestedModel, HasLogo):
    title: str
    level: int
    flexible_case: bool = True
    logo_url: Optional[str] = None
    logo_svg_text: Optional[str] = None
    logo_base64: Optional[str] = None
    logo_fa_icon_class_str: Optional[str] = None
    case_lower_func: Callable[[str], str] = lambda x: x.lower()
    case_title_func: Callable[[str], str] = lambda x: x.title()
    case_capitalize_func: Callable[[str], str] = lambda x: x.capitalize()
    parents: Optional[Sequence['NestedModel']] = field(default_factory=lambda: [])
    children: WeakList = field(default_factory=lambda: WeakList())

    def __post_init__(self):
        super().__init__()
