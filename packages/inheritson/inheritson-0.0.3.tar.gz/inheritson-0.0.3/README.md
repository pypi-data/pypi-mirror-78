# InheritsON

Fill in missing data that is inherited by a reference field in a flat list of dictionaries without inheritance depth limit.

Name is a portmanteau of Inheritance and JSON.

# Usage

```py
>>> from inheritson import fill
>>> fill([{"id": "parent", "common": "value"}, {"id": "child", "parent_id": "parent"}, {"id": "grandchild", "parent_id": "child"}])
[{'id': 'parent', 'common': 'value'}, {'id': 'child', 'common': 'value', 'parent_id': 'parent'}, {'id': 'grandchild', 'common': 'value', 'parent_id': 'child'}]
```