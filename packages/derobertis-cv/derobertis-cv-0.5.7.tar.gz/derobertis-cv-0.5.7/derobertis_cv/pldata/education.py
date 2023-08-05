import pyexlatex.resume as lr


def get_education():
    return [
        lr.Education(
            'University of Florida',
            'Gainesville, FL',
            'Ph.D. in Business Administration - Finance and Real Estate',
            'August 2020',
        ),
        lr.Education(
            'Virginia Commonwealth University',
            'Richmond, FL',
            'Master of Science in Business, Concentration in Finance',
            'May 2014'
        ),
        lr.Education(
            'Virginia Commonwealth University',
            'Richmond, FL',
            'Bachelor of Science in Business, Concentration in Finance',
            'May 2013'
        ),
    ]