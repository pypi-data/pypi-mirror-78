import pyexlatex.resume as lr
from derobertis_cv.pldata.authors import AUTHORS

REFERENCE_AUTHOR_KEYS = [
    'andy',
    'nimal',
    'nitish',
    'sugata'
]


def get_references():
    included_authors = [author for author_key, author in AUTHORS.items() if author_key in REFERENCE_AUTHOR_KEYS]
    references = [
        lr.Reference(
            author.name_as_doctor,
            title_lines=author.title_lines,
            company=author.company,
            contact_lines=author.contact_lines,
            email=author.email
        )
        for author in included_authors
    ]
    return references

