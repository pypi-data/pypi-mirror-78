__author__ = 'Gabriel Salgado and Moises Mendes'
__version__ = '0.11.0'

import typing as tp
import collections as cl

from take_resolution.utils import load_params
from take_resolution.utils import load_pipelines
from take_resolution.core import Pipeline

MapData = tp.Dict[str, tp.Any]
Output = tp.Dict[str, MapData]


class AbsentPipelineError(Exception):
    pass


def run(pipeline_name: tp.Optional[str] = None, **input: tp.Any) -> Output:
    """Run TakeResolution.
    
    :param pipeline_name: Pipeline to run. If not given, run all pipelines.
    :type pipeline_name: ``str``
    :param input: Pipeline input.
    :type input: ``any``
    :return: Pipeline output.
    :rtype: ``dict`` from ``str`` to ``dict`` from ``str`` to ``any``
    """
    data = dict()
    params = load_params()
    pipelines = load_pipelines()
    
    if pipeline_name is None:
        output = cl.defaultdict(dict)
        for pipeline_name, setting in pipelines.items():
            pipeline = Pipeline(setting, input, params, data)
            pipeline_output = pipeline.run()
            for layer, layer_output in pipeline_output.items():
                output[layer].update(layer_output)
        return dict(output)
    
    try:
        setting = pipelines[pipeline_name]
    except KeyError:
        raise AbsentPipelineError(f'Not found pipeline named {pipeline_name} on pipelines settings.')
    else:
        data.update(input)
        return Pipeline(setting, input, params, data).run()
