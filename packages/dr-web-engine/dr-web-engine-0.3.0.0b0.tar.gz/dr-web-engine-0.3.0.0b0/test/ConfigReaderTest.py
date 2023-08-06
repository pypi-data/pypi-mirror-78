from web_engine.engine.JsonQuery import JsonQuery
import pytest
import pathlib


@pytest.fixture
def ex_config_reader():
    """Expected to raise a generic exception when file path is not found"""
    with pytest.raises(Exception):
        return JsonQuery(json_query_path=f"{pathlib.Path(__file__)}/NOFILE")


def test_reader(config_reader):
    """test that file has been loaded and element _doc is present"""
    doc = config_reader.prop._doc.get()
    print(doc)
    assert doc and len(doc) > 0


def test_no_file_reader(ex_config_reader):
    """test that a managed exception is thrown"""
    pass


def test_json_query_from_dict(dict_config_reader):
    """test that JsonQuery from dictionary has been loaded and element _doc is present"""
    assert dict_config_reader.prop._doc.get()


def test_query_items(config_reader: JsonQuery):
    """test that filters and actions are removed and only query_items are returned"""
    items = config_reader.query_items
    assert len(items) > 0
    assert "_key" not in items
    assert "_doc" not in items
    assert len([x for x in items if x.startswith("_")]) == 0


def test_pre_filter_items(dict_config_reader):
    """test  that _pre_ filters are returned"""
    items = JsonQuery(json_query=dict_config_reader.prop.reviews.get()[0]).pre_filters
    assert len(items) > 0, "Items was empty"
    assert "_pre_remove" in items[0].keys(), "Key _pre_remove not found in filters"

