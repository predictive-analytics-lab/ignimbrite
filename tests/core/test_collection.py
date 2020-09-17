from dataclasses import dataclass
from typing import List, Set, Union, Dict, Collection

import pytest

from rhyolite import from_dict, WrongTypeError


def test_from_dict_with_generic_collection():
    @dataclass
    class X:
        l: List[int]

    result = from_dict(X, {"l": [1]})

    assert result == X(l=[1])


def test_from_dict_with_generic_collection_of_data_classes():
    @dataclass
    class X:
        i: int

    @dataclass
    class Y:
        x_list: List[X]

    result = from_dict(Y, {"x_list": [{"i": 1}, {"i": 2}]})

    assert result == Y(x_list=[X(i=1), X(i=2)])


def test_from_dict_with_generic_collection_of_unions():
    @dataclass
    class X:
        i: int

    @dataclass
    class Y:
        l: List[Union[int, X]]

    result = from_dict(Y, {"l": [1, {"i": 2}]})

    assert result == Y(l=[1, X(i=2)])


def test_from_dict_with_nested_generic_collection():
    @dataclass
    class X:
        i: int

    @dataclass
    class Y:
        l: List[List[X]]

    result = from_dict(Y, {"l": [[{"i": 2}]]})

    assert result == Y(l=[[X(i=2)]])


def test_from_dict_with_set():
    @dataclass
    class X:
        i_set: Set[int]

    result = from_dict(X, {"i_set": {1, 2}})

    assert result == X(i_set={1, 2})


def test_from_dict_with_dict():
    @dataclass
    class X:
        d: Dict[str, int]

    result = from_dict(X, {"d": {"a": 1, "b": 2}})

    assert result == X(d={"a": 1, "b": 2})


def test_from_dict_with_dict_of_data_classes():
    @dataclass
    class X:
        i: int

    @dataclass
    class Y:
        d: Dict[str, X]

    result = from_dict(Y, {"d": {"a": {"i": 42}, "b": {"i": 37}}})

    assert result == Y(d={"a": X(i=42), "b": X(i=37)})


def test_from_dict_with_already_created_data_class_instances():
    @dataclass
    class X:
        i: int

    @dataclass
    class Y:
        x: X
        x_list: List[X]

    result = from_dict(Y, {"x": X(i=37), "x_list": [X(i=42)]})

    assert result == Y(x=X(i=37), x_list=[X(i=42)])


def test_from_dict_with_generic_abstract_collection():
    @dataclass
    class X:
        l: Collection[int]

    result = from_dict(X, {"l": [1]})

    assert result == X(l=[1])


def test_from_dict_with_wrong_type_of_collection_item():
    @dataclass
    class X:
        l: List[int]

    with pytest.raises(WrongTypeError) as exception_info:
        from_dict(X, {"l": ["1"]})

    assert exception_info.value.field_path == "l"
    assert exception_info.value.field_type == List[int]


def test_from_dict_with_wrong_type_of_dict_value():
    @dataclass
    class X:
        d: Dict[str, int]

    with pytest.raises(WrongTypeError) as exception_info:
        from_dict(X, {"d": {"a": "test"}})

    assert exception_info.value.field_path == "d"
    assert exception_info.value.field_type == Dict[str, int]
