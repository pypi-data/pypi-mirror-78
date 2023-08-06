__author__ = 'Moises Mendes and Gabriel Salgado'
__version__ = '0.6.0'
__all__ = [
    'get_element',
    'load_json',
    'map_states',
    'build_graph'
]

import typing as tp
import json

import networkx as nx

from take_resolution.utils import DF


def get_element(df: DF) -> str:
    """Get the unique element on dataframe.
    
    :param df: Dataframe.
    :type df: ``pandas.DataFrame``
    :return: Unique element on dataframe.
    :rtype: ``str``
    """
    return df.values[0, 0]


def load_json(string: str) -> tp.Dict[str, tp.Any]:
    """Load dict data from JSON string.
    
    :param string: String with JSON content.
    :type string: ``str``
    :return: Data from JSON string.
    :rtype: ``dict`` from ``str`` to ``any``
    """
    return json.loads(string)


def map_states(bot_flow: tp.Dict[str, tp.Any]) -> tp.Dict[str, tp.List[str]]:
    """Build a map from each state on bot to a list of all possible next state.
    
    :param bot_flow: Bot flow as dict from JSON string.
    :type bot_flow: ``dict`` from ``str`` to ``any``
    :return: Map from state to all possible next states.
    :rtype: ``dict`` from ``str`` to ``list`` of ``str``
    """
    return {
        state['id']: [
            output['stateId']
            for output in state['outputs']
        ]
        for state in bot_flow['settings']['flow']['states']
    }


def build_graph(data: tp.Dict[str, tp.List[str]]) -> nx.DiGraph:
    """Build a directional graph instance.
    
    :param data: Data mapping state to all possible next states.
    :type data: ``dict`` from ``str`` to ``list`` of ``str``
    :return: Directional graph instance.
    :rtype: ``networkx.DiGraph``
    """
    return nx.DiGraph(data)
