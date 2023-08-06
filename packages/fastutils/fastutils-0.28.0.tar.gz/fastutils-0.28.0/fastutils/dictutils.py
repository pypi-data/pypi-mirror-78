# -*- coding: utf-8 -*-
import typing

class _NULL(object):
    pass
_NULL = _NULL()


class Object(dict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        changed = fix_object(self)

    def __setitem__(self, key, value):
        result = super().__setitem__(key, value)
        self.__dict__[key] = value
        return result

    def __setattr__(self, name, value):
        if isinstance(value, dict) and not isinstance(value, self.__class__):
            value = to_object(value)
        self[name] = value
        result = super().__setattr__(name, value)
        return result

def to_object(data: dict) -> Object:
    result = Object()
    for key, value in data.items():
        if isinstance(value, dict):
            value = to_object(value)
        result[key] = value
        setattr(result, key, value)
    return result

def fix_object(data):
    changed = False
    keys = list(data.keys())
    for key in keys:
        value = data[key]
        if isinstance(value, dict) and not isinstance(value, Object):
            data[key] = to_object(value)
            changed = True
    return changed

def deep_merge(target : dict, data : dict) -> None:
    for key2, value2 in data.items():
        value1 = target.get(key2, None)
        if isinstance(value1, dict) and isinstance(value2, dict):
            deep_merge(value1, value2)
        else:
            target[key2] = value2


def select(data : dict, path : str, default_value : typing.Any = None) -> dict:
    paths = path.split(".")
    for path in paths:
        if isinstance(data, dict) and path in data:
            data = data[path]
        elif isinstance(data, (list, tuple)) and path.isdigit() and int(path) < len(data):
            data = data[int(path)]
        elif hasattr(data, path):
            data = getattr(data, path)
        else:
            return default_value
    return data

def touch(data, path, default_value):
    result = select(data, path, _NULL)
    if result == _NULL:
        update(data, path, default_value)
        return select(data, path, None)
    else:
        return result

def update(data : dict, path : str, value : typing.Any) -> dict:
    paths = path.split(".")
    for index in range(0, len(paths) - 1):
        path = paths[index]
        path_next = paths[index + 1]

        if isinstance(data, dict) and path in data:
            data = data[path]
        elif isinstance(data, list) and int(path) < len(data):
            data = data[int(path)]
        else:
            if isinstance(data, list) and int(path) >= len(data):
                for _ in range(int(path) + 1 - len(data)):
                    data.append(None)
            if path_next.isdigit():
                next_value = []
            else:
                next_value = {}
            if path.isdigit():
                data[int(path)] = next_value
                data = data[int(path)]
            else:
                data[path] = next_value
                data = data[path]
    path = paths[-1]
    if path.isdigit():
        for _ in range(int(path) + 1 - len(data)):
            data.append(None)
        data[int(path)] = value
    else:
        data[path] = value
    return
    


def update(data : typing.Union[dict, Object], path : str, value : typing.Any) -> typing.Union[dict, Object]:

    old_data = data

    if isinstance(data, Object):
        is_object = True
    else:
        is_object = False

    def is_forloop_last(index, data):
        if index == len(data) - 1:
            return True
        else:
            return False
            
    def insert_empty(index, paths, data, path):
        empty = {}
        if is_object:
            empty = Object()
        if not is_forloop_last(index, paths):
            next_path = paths[index+1]
            if next_path.isdigit():
                empty = []
        data[path] = empty
        return data[path]

    paths = path.split(".")
    last_path = paths[-1]
    paths = paths[:-1]
    len_paths = len(paths)
    for index, path in enumerate(paths):
        if isinstance(data, dict) and path in data:
            data = data[path]
        elif isinstance(data, (list, tuple)) and path.isdigit():
            if int(path) < len(data):
                data = data[int(path)]
            else:
                for _ in range(int(path) + 1 - len(data)):
                    data.append(None)
                data = insert_empty(index, paths, data, int(path))
        elif hasattr(data, path):
            data = getattr(data, path)
        else:
            data = insert_empty(index, paths, data, path)
    if isinstance(data, (list, tuple)) and last_path.isdigit():
        if int(last_path) < len(data):
            data[int(last_path)] = value
        else:
            for _ in range(int(last_path) + 1 - len(data)):
                data.append(None)
            data[int(last_path)] = value
    else:
        data[last_path] = value

    return old_data

def ignore_none_item(data: dict) -> dict:
    result = {}
    for key, value in data.items():
        if value is None:
            continue
        if not value:
            if isinstance(value, (list, dict)):
                continue
        result[key] = value
    return result


def change(object_instance : typing.Union[object, dict], data_dict : typing.Union[object, dict], object_key : str, dict_key : str = None) -> bool:
    """Update property value of object_instance, using the value from data_dict. If value changed, return True. If value is equals, return False.
    """
    dict_key = dict_key or object_key
    if isinstance(object_instance, dict):
        object_value = object_instance.get(object_key, None)
    else:
        object_value = getattr(object_instance, object_key, None)
    if isinstance(data_dict, dict):
        dict_value = data_dict.get(dict_key, None)
    else:
        dict_value = getattr(data_dict, dict_key, None)
    if object_value == dict_value:
        return False
    else:
        if isinstance(object_instance, dict):
            object_instance[object_key] = dict_value
        else:
            setattr(object_instance, object_key, dict_value)
        return True

def changes(object_instance : typing.Union[object, dict], data_dict : typing.Union[object, dict], keys : typing.List[typing.Union[str, typing.Tuple[str, str]]]) -> bool:
    """Update property values of object_instance, using the value form data_dict. If any property changed, return True. If values are equal, return False. keys is a list of string or string pair.
    """
    result = False
    for key in keys:
        if isinstance(key, (tuple, set, list)) and len(key) > 1:
            object_key = key[0]
            dict_key = key[1]
        else:
            object_key = key
            dict_key = None
        changed = change(object_instance, data_dict, object_key, dict_key)
        if changed:
            result = True
    return result

def prefix_key(data, prefix):
    """e.g. {"id": 1, "name": "mktg"} -> {"departmentId": 1, "departmentName": "mktg"}
    """
    data2 = {}
    for key, value in data.items():
        key = prefix + key.capitalize()
        data2[key] = value
    return data2
