from unittest.mock import Mock

import pytest  # type: ignore

import openslides_backend.services.database as database
import openslides_backend.services.database.commands as commands
from openslides_backend.shared.filters import FilterOperator
from openslides_backend.shared.patterns import Collection, FullQualifiedId

engine = Mock()
log = Mock()

db = database.Adapter(engine, log)


def test_get() -> None:
    fqid = FullQualifiedId(Collection("fakeModel"), 1)
    fields = ["a", "b", "c"]
    command = commands.Get(fqid=fqid, mappedFields=fields)
    engine.get.return_value = {"f": 1, "meta_deleted": False, "meta_position": 1}
    partial_model, num = db.get(fqid, fields)
    assert command.data == {"fqid": fqid, "mapped_fields": fields}
    assert num is not None
    assert partial_model is not None
    engine.get.assert_called_with(command)


def test_getMany() -> None:
    fields = ["a", "b", "c"]
    collection = Collection("a")
    ids = [1]
    command = commands.GetMany(collection=collection, mapped_fields=fields, ids=ids)
    engine.getMany.return_value = [{"f": 1, "meta_deleted": False, "meta_position": 1}]
    partial_model = db.getMany(collection=collection, mapped_fields=fields, ids=ids)
    assert command.data == {
        "requests": [{"collection": collection, "mapped_fields": fields, "ids": ids}]
    }
    assert partial_model is not None
    engine.getMany.assert_called_with(command)


def test_getAll() -> None:
    fields = ["a", "b", "c"]
    collection = Collection("a")
    command = commands.GetAll(collection=collection, mapped_fields=fields)
    engine.getAll.return_value = [{"f": 1, "meta_deleted": False, "meta_position": 1}]
    partial_models = db.getAll(collection=collection, mapped_fields=fields)
    assert command.data == {"collection": collection, "mapped_fields": fields}
    assert partial_models is not None
    engine.getAll.assert_called_with(command)


@pytest.mark.skip(reason="no way of currently testing this")
def test_filter() -> None:
    assert False


def test_exists() -> None:
    collection = Collection("a")
    field = "f"
    value = "1"
    operator = "0"
    filter = FilterOperator(field=field, value=value, operator=operator)
    command = commands.Exists(collection=collection, filter=filter)
    engine.exists.return_value = {"exists": True, "position": 1}
    found = db.exists(collection=collection, filter=filter)
    assert found is not None
    assert command.data == {
        "collection": collection,
        "filter": {"field": field, "operator": operator, "value": value},
    }
    engine.exists.called_with(command)


def test_count() -> None:
    collection = Collection("a")
    field = "f"
    value = "1"
    operator = "0"
    filter = FilterOperator(field=field, value=value, operator=operator)
    command = commands.Count(collection=collection, filter=filter)
    engine.count.return_value = {"count": True, "position": 1}
    count = db.count(collection=collection, filter=filter)
    assert count is not None
    assert command.data == {
        "collection": collection,
        "filter": {"field": field, "operator": operator, "value": value},
    }
    engine.exists.called_with(command)


@pytest.mark.skip(reason="no way of currently testing this")
def test_min() -> None:
    assert False


@pytest.mark.skip(reason="no way of currently testing this")
def test_max() -> None:
    assert False
