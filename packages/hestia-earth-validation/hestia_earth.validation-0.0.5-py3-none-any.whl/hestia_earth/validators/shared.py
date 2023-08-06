from typing import List
from functools import reduce
from dateutil.parser import parse


def validate_dates(node: dict):
    start = node.get('startDate')
    end = node.get('endDate')
    return start is None or end is None or end > start


def validate_list_dates(node: dict, prop: str):
    def validate(values):
        value = values[1]
        index = values[0]
        return validate_dates(value) or {
            'level': 'error',
            'dataPath': f".{prop}[{index}].endDate",
            'message': 'must be greater than startDate'
        }

    results = list(map(validate, enumerate(node[prop] if prop in node else [])))
    return next((x for x in results if x is not True), True)


def same_properties(value: dict, props: List[str]):
    def identical(test: dict):
        same_values = list(filter(lambda prop: get_dict_key(value, prop) == get_dict_key(test, prop), props))
        return test if len(same_values) == len(props) else None
    return identical


def validate_list_duplicated(node: dict, prop: str, props: List[str]):
    def validate(values):
        value = values[1]
        index = values[0]
        values = node[prop].copy()
        values.pop(index)
        duplicates = list(filter(same_properties(value, props), values))
        return len(duplicates) == 0 or {
            'level': 'error',
            'dataPath': f".{prop}[{index}]",
            'message': f"Duplicates found. Please make sure there is only one entry with the same {', '.join(props)}"
        }

    results = list(map(validate, enumerate(node[prop] if prop in node else [])))
    return next((x for x in results if x is not True), True)


def diff_in_days(from_date: str, to_date: str):
    difference = parse(to_date) - parse(from_date)
    return round(difference.days + difference.seconds/86400, 1)


def diff_in_years(from_date: str, to_date: str):
    return round(diff_in_days(from_date, to_date)/365.2425, 1)


def list_has_props(values: List[dict], props: List[str]):
    return filter(lambda x: all(prop in x for prop in props), values)


def get_dict_key(value: dict, key: str):
    keys = key.split('.')
    return reduce(lambda x, y: x if x is None else x.get(y), keys, value)
