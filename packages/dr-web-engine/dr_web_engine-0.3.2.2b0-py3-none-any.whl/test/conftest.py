from web_engine.engine.JsonQuery import JsonQuery
from web_engine.engine.CoreEngine import CoreEngine
from web_engine.interfaces.Parser import Parser

from unittest.mock import Mock

import pytest
import pathlib


@pytest.fixture
def config_reader():
    """JsonQuery loaded from  trader.extract.json file in the test directory path"""
    return JsonQuery(json_query_path=f"{pathlib.Path(__file__).parent.absolute()}/trader.extract.json")


@pytest.fixture
def simple_config():
    json_query = {
        "_doc": "https://www.checkatrade.com/trades/WayreHouseElectricalServices",
        "h1": "//h1/text()"
    }
    return JsonQuery(json_query=json_query)


@pytest.fixture
def dict_config_reader():
    """JsonQuery loaded from dictionary"""
    json_query = {
        "_doc": "https://www.checkatrade.com/trades/WayreHouseElectricalServices",
        "data": {
            "ld_data": "//head/script[@type=\"application/ld+json\"][1]"
        }, "reviews": [{
            "_doc": "https://www.checkatrade.com/trades/WayreHouseElectricalServices/reviews",
            "_base_path": "//div[contains(@class, 'ReviewsPage__Content')]//div[contains(@class, 'ReviewsItem__Wrapper')]",
            "_key": "review",
            "_pre_remove": "//*[contains(@class,'alert-box')]",
            "_follow": "//a[contains(@class,\"Chevrons__Wrapper\")][2]/@href",
            "_follow_action": "//a[contains(@class,\"Chevrons__Wrapper\")][2]{click }",
            "title": "//h3[contains(@class, 'ReviewsItem__Title')]",
            "score": "//*[name()='svg']//text()[normalize-space()]",
            "verified": "//div[contains(@class, 'ReviewsItem__Verified')]/text()[normalize-space()]",
            "content": "//p[contains(@class, 'ReviewsItem__P')]",
            "review_by": "//div[contains(@class, 'ReviewsItem__Byline')]/text()[normalize-space()]"
        }]}

    return JsonQuery(json_query=json_query)



