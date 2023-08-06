from functools import reduce

from .cycle import validate_cycle
from .organisation import validate_organisation
from .site import validate_site


VALIDATE_NODE_TYPE = {
    'Cycle': lambda v: validate_cycle(v),
    'Organisation': lambda v: validate_organisation(v),
    'Site': lambda v: validate_site(v)
}


def flatten(values: list):
    return list(reduce(lambda x, y: x + (y if isinstance(y, list) else [y]), values, []))


def node_type(node: dict):
    return node['type'] if 'type' in node else node['@type'] if '@type' in node else None


def validate_node_children(node: dict):
    values = list(filter(lambda v: isinstance(v, list) or isinstance(v, dict), node.values()))
    return list(map(validate_node_type, values))


def validate_node_type(node: dict):
    ntype = node_type(node)
    if ntype is None:
        return []
    validations = flatten(
        (VALIDATE_NODE_TYPE[ntype](node) if ntype in VALIDATE_NODE_TYPE else []) + validate_node_children(node)
    )
    return list(filter(lambda v: v is not True, validations))


def validate_node(node: dict):
    return validate_node_type(node)
