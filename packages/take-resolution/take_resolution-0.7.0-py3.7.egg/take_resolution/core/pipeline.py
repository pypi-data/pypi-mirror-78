__author__ = 'Gabriel Salgado and Moises Mendes'
__version__ = '0.1.0'

import typing as tp
import importlib as il

MapData = tp.Dict[str, tp.Any]
Output = tp.Dict[str, MapData]


class InvalidSettingError(Exception):
    pass


class AbsentInputError(Exception):
    pass


class Pipeline(object):
    """Pipeline
    
    Wraps a sequential process with inputs, functions and outputs.
    On method run, run all functions and format output data into layers.
    
    Each function is given by a node described on setting.
    Node description also includes input and output.
    Inputs can be pipeline input (input), parameter from conf (params) or data from another node or pipeline (data).
    Output is save only as data (data).
    
    After run all nodes, pipeline output is formatted as given in setting.
    It maps each layer into data (data) directed to that layer.
    """
    
    def __init__(self, setting: MapData, input: MapData, params: MapData, data: MapData) -> None:
        super().__init__()
        self.setting = setting
        self.input = input
        self.params = params
        self.data = data
    
    def format(self) -> Output:
        """Format data into pipeline output, defined in settings, following data layers.
        
        Formatted pipeline output is as:
        ```python
        {
            "raw": {...},
            "intermediate": {...},
            "primary": {...},
            "features": {...},
            "model_input": {...},
            "models": {...},
            "model_output": {...},
            "reporting": {...},
        }
        ```
        
        :return: Formatted data into layers.
        :rtype: ``dict`` from ``str`` to ``dict`` from ``str`` to ``any``
        """
        return {
            layer: {name: self.data[name] for name in names}
            for layer, names in self.setting['output'].items()
        }
    
    def get(self, path: tp.Union[str, tp.List[str]]) -> tp.Any:
        """Get value from input, params or data.
        
        :param path: Path with prefix "input." or "params." or no prefix (data) or a group.
        :type path: ``str`` or ``list`` of ``str``
        :return: Respective value.
        :rtype: ``any``
        """
        if isinstance(path, list):
            return list(map(self.get, path))
        split = path.split('.', 1)
        if len(split) == 2:
            source, name = split
            if source == 'input':
                try:
                    return self.input[name]
                except KeyError:
                    raise AbsentInputError(f'Not found name {name} on pipeline input.')
            elif source == 'params':
                return self.params[name]
            raise InvalidSettingError(f'Unknown prefix {source} with name {name}.')
        name = split[0]
        return self.data[name]
    
    def get_args(self, paths: tp.List[str]) -> tp.List[tp.Any]:
        """Get values for node function input.
        
        :param paths: Defines path for each value. See `Pipeline.get`.
        :type paths: ``list`` of ``str``
        :return: Input for node function.
        :rtype: ``list`` of ``any``
        """
        return list(map(self.get, paths))
    
    def run(self) -> Output:
        """Run pipeline nodes and returns pipeline formatted output.
        
        :return: Pipeline output.
        :rtype: ``dict`` from ``str`` to ``dict`` from ``str`` to ``any``
        """
        self.run_nodes()
        return self.format()
    
    def run_node(self, node: MapData) -> None:
        """Run a node.
        
        :param node: Node setting as `{'input': [...], 'output': '...', 'function': '...'}`.
        :type node: ``dict`` from ``str`` to ``any``
        :return: Node output value.
        :rtype: ``any``
        """
        input = self.get_args(node['input'])
        function = self.load(node['function'])
        output = function(*input)
        self.set(node['output'], output)
    
    def run_nodes(self) -> None:
        """Run pipeline nodes."""
        for node in self.setting['nodes']:
            self.run_node(node)
    
    def set(self, path: str, value: tp.Any) -> None:
        """Set a value as data.
        
        :param path: Path for data.
        :type path: ``str``
        :param value: Value to set.
        :type value: ``any``
        """
        self.data[path] = value
    
    @staticmethod
    def load(path: str) -> tp.Callable:
        """Load a function by import for node.
        
        :param path: Path with package, module and function name.
        :type path: ``str``
        :return: Imported function.
        :rtype: ``callable``
        """
        module_name, name = path.rsplit('.', 1)
        module = il.import_module(module_name)
        return getattr(module, name)
