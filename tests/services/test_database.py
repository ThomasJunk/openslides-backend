from unittest.mock import Mock

import openslides_backend.services.datastore as datastore
import openslides_backend.services.datastore.commands as commands
from openslides_backend.services.datastore.adapter.interface import GetManyRequest
from openslides_backend.shared.filters import FilterOperator, Or
from openslides_backend.shared.patterns import Collection, FullQualifiedId

reader = Mock()
writer = Mock()
log = Mock()

db = datastore.Adapter(reader, writer, log)


def test_get() -> None:
    fqid = FullQualifiedId(Collection("fakeModel"), 1)
    fields = ["a", "b", "c"]
    command = commands.Get(fqid=fqid, mappedFields=fields)
    reader.get.return_value = {"f": 1, "meta_deleted": False, "meta_position": 1}
    partial_model = db.get(fqid, fields)
    assert command.data == {"fqid": str(fqid), "mapped_fields": fields}
    assert partial_model is not None
    reader.get.assert_called_with(command)


def test_getMany() -> None:
    fields = ["a", "b", "c"]
    fields2 = ["d", "e", "f"]
    collection = Collection("a")
    ids = [1]
    gmr = GetManyRequest(collection, ids, fields)
    command = commands.GetMany([gmr], fields2)
    reader.getMany.return_value = {
        "a/1": {"f": 1, "meta_deleted": False, "meta_position": 1}
    }
    result = db.getMany([gmr], fields2)
    assert result is not None
    assert command.data == {"requests": [gmr.to_dict()], "mapped_fields": fields2}
    reader.getMany.assert_called_with(command)


def test_getManyByFQIDs() -> None:
    fqid = FullQualifiedId(Collection("fakeModel"), 1)
    command = commands.GetManyByFQIDs([fqid])
    reader.getMany.return_value = {
        "a/1": {"f": 1, "meta_deleted": False, "meta_position": 1}
    }
    result = db.getManyByFQIDs([fqid])
    assert result is not None
    assert command.data == {"requests": [str(fqid)]}


def test_getAll() -> None:
    fields = ["a", "b", "c"]
    collection = Collection("a")
    command = commands.GetAll(collection=collection, mapped_fields=fields)
    reader.getAll.return_value = [{"f": 1, "meta_deleted": False, "meta_position": 1}]
    partial_models = db.getAll(collection=collection, mapped_fields=fields)
    assert command.data == {"collection": str(collection), "mapped_fields": fields}
    assert partial_models is not None
    reader.getAll.assert_called_with(command)


def test_simple_filter() -> None:
    collection = Collection("a")
    field = "f"
    value = "1"
    operator = "="
    filter = FilterOperator(field=field, value=value, operator=operator)
    command = commands.Filters(collection=collection, filter=filter)
    reader.filter.return_value = [
        {"f": 1, "meta_deleted": False, "meta_position": 1},
        {"f": 1, "meta_deleted": False, "meta_position": 5},
        {"f": 1, "meta_deleted": False, "meta_position": 6},
        {"f": 1, "meta_deleted": False, "meta_position": 7},
    ]
    found = db.filter(collection=collection, filter=filter)
    assert found is not None
    assert command.data == {
        "collection": str(collection),
        "filter": {"field": field, "operator": operator, "value": value},
    }
    reader.filter.called_with(command)


def test_complex_filter() -> None:
    collection = Collection("a")
    filter1 = FilterOperator(field="f", value="1", operator="=")
    filter2 = FilterOperator(field="f", value="3", operator="=")
    or_filter = Or([filter1, filter2])
    command = commands.Filters(collection=collection, filter=or_filter)
    reader.filter.return_value = [
        {"f": 1, "meta_deleted": False, "meta_position": 1},
        {"f": 3, "meta_deleted": False, "meta_position": 4},
        {"f": 1, "meta_deleted": False, "meta_position": 6},
        {"f": 1, "meta_deleted": False, "meta_position": 7},
    ]
    found = db.filter(collection=collection, filter=or_filter)
    assert found is not None
    assert command.data == {
        "collection": str(collection),
        "filter": or_filter.to_dict(),
    }
    reader.filter.called_with(command)


def test_exists() -> None:
    collection = Collection("a")
    field = "f"
    value = "1"
    operator = "="
    filter = FilterOperator(field=field, value=value, operator=operator)
    command = commands.Exists(collection=collection, filter=filter)
    reader.exists.return_value = {"exists": True, "position": 1}
    found = db.exists(collection=collection, filter=filter)
    assert found is not None
    assert command.data == {
        "collection": str(collection),
        "filter": {"field": field, "operator": operator, "value": value},
    }
    reader.exists.called_with(command)


def test_count() -> None:
    collection = Collection("a")
    field = "f"
    value = "1"
    operator = "="
    filter = FilterOperator(field=field, value=value, operator=operator)
    command = commands.Count(collection=collection, filter=filter)
    reader.count.return_value = {"count": True, "position": 1}
    count = db.count(collection=collection, filter=filter)
    assert count is not None
    assert command.data == {
        "collection": str(collection),
        "filter": {"field": field, "operator": operator, "value": value},
    }
    reader.exists.called_with(command)


def test_min() -> None:
    collection = Collection("a")
    field = "f"
    value = "1"
    operator = "="
    filter = FilterOperator(field=field, value=value, operator=operator)
    command = commands.Min(collection=collection, filter=filter, field=field)
    reader.min.return_value = {"min": 1, "position": 1}
    agg = db.min(collection=collection, filter=filter, field=field)
    assert agg is not None
    assert command.data == {
        "collection": str(collection),
        "filter": {"field": field, "operator": operator, "value": value},
        "field": field,
    }
    reader.exists.called_with(command)


def test_max() -> None:
    collection = Collection("a")
    field = "f"
    value = "1"
    operator = "="
    filter = FilterOperator(field=field, value=value, operator=operator)
    command = commands.Max(collection=collection, filter=filter, field=field)
    reader.max.return_value = {"max": 1, "position": 1}
    agg = db.max(collection=collection, filter=filter, field=field)
    assert agg is not None
    assert command.data == {
        "collection": str(collection),
        "filter": {"field": field, "operator": operator, "value": value},
        "field": field,
    }
    reader.exists.called_with(command)
