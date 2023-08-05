from json.decoder import JSONDecodeError
import os
from .exceptions import *
from .loaders import Loaders
from copy import deepcopy


class ConstantLoader:

    def __init__(self, load_from, **kwargs):

        safe_load_yaml = kwargs.get("safe_load_yaml", True)
        loader = kwargs.get("loader")

        if type(load_from) == str:
            # assume that the input is a file path and parse contents

            if not os.path.exists(load_from):
                # Provided string does not represent a valid filepath so try to parse the string
                file_contents = load_from
            else:
                file_contents = open(load_from).read()

            if loader is None:

                from_json = None
                from_yaml = None

                # Test load JSON
                try:
                    from_json = Loaders.json(file_contents)
                except JSONDecodeError:
                    pass

                if from_json is None:
                    # Not JSON. Test load YAML.

                    if safe_load_yaml:
                        from_yaml = Loaders.yaml_safe(file_contents)
                    else:
                        from_yaml = Loaders.yaml_unsafe(file_contents)

                    if type(from_yaml) is dict:  # Data successfully parsed
                        self.data = from_yaml
                    else:
                        raise ValueError("Provided string is not a filepath, valid JSON nor valid YAML.")
                else:
                    if type(from_json) != dict:
                        raise TypeError("Type {} cannot be used".format(type(from_json)))
                    self.data = from_json

            else:
                custom_loader_output = loader(file_contents)
                if custom_loader_output is None:
                    raise ValueError("Custom loader function returned no value")
                if type(custom_loader_output) != dict:
                    raise ValueError("Custom loader function returned incorrect type (must be dict,"
                                     .format(type(custom_loader_output)))
                else:
                    self.data = custom_loader_output

        elif type(load_from) == dict:
            # preloaded JSON or YAML or whatever
            self.data = deepcopy(load_from)
        else:
            # invalid type, cannot be used
            raise TypeError("Type {} cannot be used".format(type(load_from)))

    def _resolve_path(self, path):
        """
        Get value of specified path in array/dict

        :param path: list of JSON arguments, for example j["thing"][1]["hello"] would be ["thing", 1, "hello"]
        :param obj: used for recursion. Defaults to self.data
        :return: none if not found otherwise values
        :raises: KeyError if the path is not found
        """

        if len(path) == 0:
            return self.data
        else:
            t = self.data
            for i in range(len(path) - 1):
                t = t[path[i]]
            return t[path[-1]]

    def _write_path(self, value, path):
        """
        Write value to path specified

        :param value: value to write
        :param path: path to write to
        :param : object path is in
        """

        if len(path) == 0:
            if type(value) != dict:
                raise TypeError("Writing value {} to path {} will cause the base value to not be a dictionary")
            else:
                self.data = value
        else:
            t = self.data
            for i in range(len(path) - 1):
                try:
                    t = t[path[i]]
                except KeyError:
                    t[path[i]] = {}
                    t = t[path[i]]
            t[path[-1]] = value

    def default(self, path, default_value=None):
        """
        Determines if a default should be used depending on if the specified path can be found in the loaded_settings
        object

        :param path: path to search
        :param default_value: default value to use
        :return: chosen value (default or loaded from specified path)
        """

        if type(path) == str:
            path = (path,)

        try:
            return self._resolve_path(path)
        except LookupError:
            self._write_path(default_value, path)
            return default_value

    def required(self, path):
        """
        Raises if path cannot be resolved using resolve_path, otherwise returns the value

        :param path: path to search for
        :return: value from loaded_settings
        """

        if type(path) == str:
            path = (path,)

        try:
            return self._resolve_path(path)
        except LookupError:
            raise RequiredSettingNotFoundException(path)
