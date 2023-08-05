from dataclasses import dataclass, field
from typing import Optional, Sequence

from weakreflist import WeakList

from derobertis_cv.models.nested import NestedModel
from derobertis_cv.pltemplates.logo import HasLogo


@dataclass
class UniversityModel(HasLogo):
    title: str
    abbreviation: str
    logo_url: Optional[str] = None
    logo_svg_text: Optional[str] = None
    logo_base64: Optional[str] = None
    logo_fa_icon_class_str: Optional[str] = None
