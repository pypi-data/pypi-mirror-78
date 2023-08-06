from hestia_earth.schema import CycleFunctionalUnitMeasure, SiteSiteType

from .shared import validate_dates, validate_list_dates, diff_in_days, get_dict_key


SITE_TYPES_1ha = [
    SiteSiteType.CROPLAND.value,
    SiteSiteType.PERMANENT_PASTURE.value
]


def validate_cycle_dates(cycle: dict):
    return validate_dates(cycle) or {
        'level': 'error',
        'dataPath': '.endDate',
        'message': 'must be greater than startDate'
    }


def validate_cycleDuration(cycle: dict):
    duration = diff_in_days(cycle.get('startDate'), cycle.get('endDate'))
    return duration == round(cycle.get('cycleDuration'), 1) or {
        'level': 'error',
        'dataPath': '.cycleDuration',
        'message': f"must equal to endDate - startDate in days (~{duration})"
    }


def validate_functionalUnitMeasure(cycle: dict):
    site_type = get_dict_key(cycle, 'site.siteType')
    value = cycle.get('functionalUnitMeasure')
    expected = CycleFunctionalUnitMeasure._1_HA.value
    return site_type not in SITE_TYPES_1ha or value == expected or {
        'level': 'error',
        'dataPath': '.functionalUnitMeasure',
        'message': f"must equal to {expected}"
    }


def validate_cycle(cycle: dict):
    return [
        validate_cycle_dates(cycle),
        validate_cycleDuration(cycle) if 'cycleDuration' in cycle
        and 'startDate' in cycle and 'endDate' in cycle and cycle.get('numberOfCycles') is None else True,
        validate_functionalUnitMeasure(cycle) if 'functionalUnitMeasure' in cycle else True,
        validate_list_dates(cycle, 'emissions'),
        validate_list_dates(cycle, 'practices')
    ]
