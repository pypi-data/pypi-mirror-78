__author__ = 'Gabriel Salgado'
__version__ = '0.1.1'

import typing as tp
import pytest
import pandas as pd
import networkx as nx
import take_resolution as tr


@pytest.fixture
def bot_flow():
    return {
        'settings': {
            'flow': {
                'states': [
                    {
                        'id': 'start',
                        'outputs': [
                            {
                                'stateId': 'coffee'
                            },
                            {
                                'stateId': 'tea'
                            },
                            {
                                'stateId': 'vodka'
                            }
                        ]
                    },
                    {
                        'id': 'coffee',
                        'outputs': [
                            {
                                'stateId': 'sugar'
                            },
                            {
                                'stateId': 'error'
                            }
                        ]
                    },
                    {
                        'id': 'tea',
                        'outputs': [
                            {
                                'stateId': 'sugar'
                            },
                            {
                                'stateId': 'error'
                            }
                        ]
                    },
                    {
                        'id': 'vodka',
                        'outputs': [
                            {
                                'stateId': 'end'
                            },
                            {
                                'stateId': 'error'
                            }
                        ]
                    },
                    {
                        'id': 'sugar',
                        'outputs': [
                            {
                                'stateId': 'end'
                            },
                            {
                                'stateId': 'error'
                            }
                        ]
                    },
                    {
                        'id': 'error',
                        'outputs': [
                            {
                                'stateId': 'start'
                            },
                            {
                                'stateId': 'end'
                            }
                        ]
                    },
                    {
                        'id': 'end',
                        'outputs': []
                    }
                ]
            }
        }
    }


@pytest.fixture
def bot_states():
    return {
        'start': ['coffee', 'tea', 'vodka'],
        'coffee': ['sugar', 'error'],
        'tea': ['sugar', 'error'],
        'vodka': ['end', 'error'],
        'sugar': ['end', 'error'],
        'error': ['start', 'end'],
        'end': []
    }


@pytest.mark.parametrize('df_element', [
    (pd.DataFrame({'column': ['element']}), 'element'),
    (pd.DataFrame({'what': ['x']}), 'x'),
    (pd.DataFrame({'number': ['123']}), '123'),
    (pd.DataFrame({'drink': ['coffee']}), 'coffee')
])
def test_get_element(df_element):
    df, expected_element = df_element
    element = tr.bot_flow.get_element(df)
    assert isinstance(element, str)
    assert element == expected_element


@pytest.mark.parametrize('string_dct', [
    ('{"name": "bot", "id": 1234, "messages": 5000}', {'name': 'bot', 'id': 1234, 'messages': 5000}),
    ('{"field1": 1.2345, "field2": {"subfield": 0}}', {'field1': 1.2345, 'field2': {'subfield': 0}}),
    ('{"option1": "coffee", "option2": "vodka"}', {'option1': 'coffee', 'option2': 'vodka'})
])
def test_load_json(string_dct):
    string, expected_dct = string_dct
    dct = tr.bot_flow.load_json(string)
    assert isinstance(dct, dict)
    assert dct == expected_dct


def test_map_states(bot_flow: tp.Dict[str, tp.Any], bot_states: tp.Dict[str, tp.List[str]]):
    states = tr.bot_flow.map_states(bot_flow)
    assert isinstance(states, dict)
    assert states, bot_states


def test_build_graph(bot_states: tp.Dict[str, tp.List[str]]):
    graph = tr.bot_flow.build_graph(bot_states)
    assert isinstance(graph, nx.DiGraph)
    assert list(sorted(bot_states.keys())) == list(sorted(graph.nodes))
    for source, target in graph.edges:
        assert target in bot_states[source]
