from typing import List

from .validators import validate_node


def validate(nodes: List[dict]):
    return list(map(validate_node, nodes))
