#!/usr/bin/env python3
'''
InheritsON, portmanteau of Inheritance and JSON

Fill in missing data that is inherited by a reference field
in a flat list of dictionaries without inheritance depth limit.
'''

from typing import Callable, List


def inherit(parent: dict, child: dict) -> dict:
    '''
    Default inheritance resolver

    >>> inherit(\
        {"id": "parent", "common": "value"},\
        {"id": "child", "parent_id": "parent"}\
    )
    {'id': 'child', 'common': 'value', 'parent_id': 'parent'}
    '''
    assert parent, child
    result = parent.copy()
    result.update(child)
    return result


def fill(
        data: List[dict],
        id_field: str = 'id',
        parent_id_field: str = 'parent_id',
        raise_orphans: bool = True,
        preserve_order: bool = True,
        inheritance_function: Callable[[dict, dict], dict] = inherit) \
        -> List[dict]:
    '''
    Fill in values in children objects from ancestors chain
    by a reference field.

    >>> fill([\
{"id": "parent", "common": "value"},\
{"id": "child", "parent_id": "parent"},\
{"id": "grandchild", "parent_id": "child"}\
    ])
    [\
{'id': 'parent', 'common': 'value'}, \
{'id': 'child', 'common': 'value', 'parent_id': 'parent'}, \
{'id': 'grandchild', 'common': 'value', 'parent_id': 'child'}]

    '''
    loaded = {}
    deferred = {}
    if preserve_order:
        order = []

    for entity in data:
        assert isinstance(entity, dict)
        object_id = entity.get(id_field)
        parent_id = entity.get(parent_id_field)

        if preserve_order:
            order.append(object_id)

        if not parent_id:
            loaded[object_id] = entity
            continue

        if parent_id in loaded:
            assert parent_id not in deferred

            loaded[object_id] = \
                inheritance_function(loaded[parent_id], entity)

        else:
            deferred[object_id] = entity

    while deferred:
        # read `list` as "snapshot"
        for object_id in list(deferred.keys()):

            entity = deferred[object_id]
            parent_id = entity.get(parent_id_field)

            assert parent_id
            if parent_id in loaded:
                loaded[object_id] = \
                    inheritance_function(loaded[parent_id], entity)

                deferred.pop(object_id)

            else:
                if parent_id not in deferred:
                    if raise_orphans:
                        raise ValueError(
                            f'{parent_id} not found in {id_field} values')
                    else:
                        loaded[object_id] = entity
                        deferred.pop(object_id)

    if preserve_order:
        return [loaded[object_id] for object_id in order]

    return list(loaded.values())
