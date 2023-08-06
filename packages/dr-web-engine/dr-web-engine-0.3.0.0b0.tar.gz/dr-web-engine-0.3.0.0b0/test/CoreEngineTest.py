from web_engine.engine.CoreEngine import CoreEngine

import pytest
from unittest.mock import Mock

parser = Mock()
parser.get_doc_element.return_value = "<html><body>Hello</body></html>"
parser.get_doc_element_by_filter.return_value = "<html><body>Hello</body></html>"
parser.get_element.return_value = []


@pytest.fixture
def engine(dict_config_reader):
    core_engine = CoreEngine(parser=parser, query=dict_config_reader, log=None, context=None)
    return core_engine


def test_main_process(engine):
    result = engine.process()
    assert engine.parser.get_doc_element.called, "Method get_doc_element was not called"
    assert engine.parser.get_doc_element_by_filter.called, "Method get_doc_element_by_filter not called"
    assert engine.parser.get_element.called, "Method get_element not called"
    assert result


def test_process_doc(engine, simple_config):
    main_content = "<html><body><h1>Expected Result</h1></body><html>"
    engine.parser.get_doc_element.return_value = main_content
    engine.parser.get_element.return_value = [main_content]
    engine.parser.get_items.return_value = "Expected Result"
    result = engine._process_doc(simple_config)
    assert len(result) == 1, f"Wrong array length: expected 1, return {len(result)}"
    assert result[0]["h1"] == "Expected Result", "Failed to get the expected h1 return"


def test_process_item(engine, simple_config):
    engine.parser.get_items.side_effect = lambda x, _: "Expected Result" if x == simple_config.prop.h1.get() else ""
    result = engine._process_item("h1", simple_config.prop.h1.get(), "")
    assert result["h1"] == "Expected Result"


