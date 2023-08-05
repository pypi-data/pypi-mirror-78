from copy import deepcopy
from pyexlatex.logic.format.and_join import join_with_commas_and_and_output_list

RESEARCH_INTERESTS = [
    'empirical corporate finance',
    'empirical asset pricing',
    'behavioral finance',
    'market microstructure',
    'monetary policy'
]

def get_research_interests():
    formatted_research_interests = deepcopy(RESEARCH_INTERESTS)
    formatted_research_interests[0] = formatted_research_interests[0].capitalize()
    joined = join_with_commas_and_and_output_list(formatted_research_interests)
    return joined