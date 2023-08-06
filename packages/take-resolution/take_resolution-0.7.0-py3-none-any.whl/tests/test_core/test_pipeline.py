__author__ = 'Gabriel Salgado and Moises Mendes'
__version__ = '0.1.0'

import typing as tp

import pytest
import pytest_mock as pm

from take_resolution.core import Pipeline
from take_resolution.core import InvalidSettingError
from take_resolution.core import AbsentInputError

MapData = tp.Dict[str, tp.Any]
Attributes = tp.Tuple[MapData, MapData, MapData, MapData]


@pytest.fixture
def attributes(mocker: pm.MockFixture) -> Attributes:
    setting = mocker.Mock(spec=MapData)
    input = mocker.Mock(spec=MapData)
    params = mocker.Mock(spec=MapData)
    data = mocker.Mock(spec=MapData)
    return setting, input, params, data


@pytest.fixture
def pipeline(attributes: Attributes) -> Pipeline:
    setting, input, params, data = attributes
    return Pipeline(setting, input, params, data)


def test_pipeline(attributes: Attributes) -> None:
    setting, input, params, data = attributes
    
    pipeline = Pipeline(setting, input, params, data)
    
    assert pipeline.setting is setting
    assert pipeline.input is input
    assert pipeline.params is params
    assert pipeline.data is data


@pytest.mark.parametrize('data_output_expected', [
    [
        {'name1': 1, 'name2': 12.5},
        {'raw': ['name1'], 'features': ['name2']},
        {'raw': {'name1': 1}, 'features': {'name2': 12.5}}
    ]
])
def test_pipeline_format(data_output_expected: tp.Tuple[MapData, MapData, MapData], pipeline: Pipeline) -> None:
    data, output, expected = data_output_expected
    setting = {'output': output}
    pipeline.data = data
    pipeline.setting = setting
    
    result = pipeline.format()
    
    assert result == expected


@pytest.mark.parametrize('name', ['name'])
def test_pipeline_get_input(mocker: pm.MockFixture, pipeline: Pipeline, name: str) -> None:
    path = f'input.{name}'
    expected = mocker.Mock()
    input = {name: expected}
    pipeline.input = input
    
    result = pipeline.get(path)
    
    assert result is expected


@pytest.mark.parametrize('name', ['name'])
def test_pipeline_get_absent_input(pipeline: Pipeline, name: str) -> None:
    path = f'input.{name}'
    input = {}
    pipeline.input = input
    
    exc_info = pytest.raises(AbsentInputError, pipeline.get, path)
    
    assert exc_info.value.args[0] == f'Not found name {name} on pipeline input.'


@pytest.mark.parametrize('name', ['name'])
def test_pipeline_get_params(mocker: pm.MockFixture, pipeline: Pipeline, name: str) -> None:
    path = f'params.{name}'
    expected = mocker.Mock()
    params = {name: expected}
    pipeline.params = params
    
    result = pipeline.get(path)
    
    assert result is expected


@pytest.mark.parametrize('name', ['name'])
def test_pipeline_get_data(mocker: pm.MockFixture, pipeline: Pipeline, name: str) -> None:
    path = f'{name}'
    expected = mocker.Mock()
    data = {name: expected}
    pipeline.data = data
    
    result = pipeline.get(path)
    
    assert result is expected


@pytest.mark.parametrize('name', ['name'])
@pytest.mark.parametrize('prefix', ['coffee'])
def test_pipeline_get_invalid(pipeline: Pipeline, name: str, prefix: str) -> None:
    path = f'{prefix}.{name}'
    
    exc_info = pytest.raises(InvalidSettingError, pipeline.get, path)
    
    assert exc_info.value.args[0] == f'Unknown prefix {prefix} with name {name}.'


@pytest.mark.parametrize('paths', [['name1', 'name2']])
def test_pipeline_get_group(mocker: pm.MockFixture, pipeline: Pipeline, paths: tp.List[str]) -> None:
    data = {name: mocker.Mock() for name in paths}
    pipeline.data = data
    expected = [data[name] for name in paths]
    
    result = pipeline.get(paths)
    
    assert result == expected


@pytest.mark.parametrize('name', ['name'])
def test_pipeline_get_args(mocker: pm.MockFixture, pipeline: Pipeline, name: str) -> None:
    n_elements = 3
    paths = [mocker.Mock() for _ in range(n_elements)]
    expected = [mocker.Mock() for _ in range(n_elements)]
    expected_get_calls = [mocker.call(path) for path in paths]
    
    get = mocker.Mock(side_effect=expected)
    pipeline.get = get
    
    result = pipeline.get_args(paths)
    
    assert result == expected
    get.assert_has_calls(expected_get_calls)


def test_run(mocker: pm.MockFixture, pipeline: Pipeline) -> None:
    expected = mocker.Mock()
    run_nodes = mocker.Mock()
    format = mocker.Mock(return_value=expected)
    pipeline.run_nodes = run_nodes
    pipeline.format = format
    
    result = pipeline.run()
    
    assert result is expected
    run_nodes.assert_called_once_with()
    format.assert_called_once_with()


def test_pipeline_run_node(mocker: pm.MockFixture, pipeline: Pipeline) -> None:
    node_input = mocker.Mock()
    node_function = mocker.Mock()
    node_output = mocker.Mock()
    node = {
        'input': node_input,
        'function': node_function,
        'output': node_output
    }
    input = [mocker.Mock()]
    output = mocker.Mock()
    function = mocker.Mock(return_value=output)
    get_args = mocker.Mock(return_value=input)
    load = mocker.Mock(return_value=function)
    set = mocker.Mock()
    pipeline.get_args = get_args
    pipeline.load = load
    pipeline.set = set
    
    pipeline.run_node(node)
    
    get_args.assert_called_once_with(node_input)
    load.assert_called_once_with(node_function)
    function.assert_called_once_with(*input)
    set.assert_called_once_with(node_output, output)


def test_pipeline_run_nodes(mocker: pm.MockFixture, pipeline: Pipeline) -> None:
    n_elements = 3
    nodes = [mocker.Mock() for _ in range(n_elements)]
    setting = {'nodes': nodes}
    expected_calls = [mocker.call(node) for node in nodes]
    run_node = mocker.Mock()
    pipeline.setting = setting
    pipeline.run_node = run_node
    
    pipeline.run_nodes()
    
    run_node.assert_has_calls(expected_calls)


def test_pipeline_set(mocker: pm.MockFixture, pipeline: Pipeline) -> None:
    path = mocker.Mock(spec=str)
    value = mocker.Mock()
    data = dict()
    pipeline.data = data
    
    pipeline.set(path, value)
    
    assert path in pipeline.data
    assert pipeline.data[path] is value


@pytest.mark.parametrize('path', [
    'time.time',
    'json.load',
    'os.path.join'
])
def test_pipeline_load(mocker: pm.MockFixture, path: str) -> None:
    time = mocker.Mock()
    mocker.patch(path, time)
    
    function = Pipeline.load(path)
    
    assert function is time
