import os
from inspect import getmodule, signature
from argparse import ArgumentParser

import json


class Grain(ArgumentParser):
    def __init__(self, polyaxon_exp=None, *args, **kwargs):
        super(Grain, self).__init__(*args, **kwargs)
        self.polyaxon_exp = polyaxon_exp

        self.add_argument('--sensor',
                          type=str,
                          required=True,
                          help='Sensor in use (sentinel-2, landsat, planet)')

        self.add_argument('--band_ids',
                          type=self._band_ids_sep,
                          required=True,
                          help='Sensor band ids used in experiment')

        self.add_argument('--input_shape',
                          type=self._input_shape_sep,
                          required=True,
                          help='patch size for training process')

        self.add_argument('--resolution',
                          type=int,
                          required=True,
                          help='resolution of training process tensor')

    def parse_args(self, args=None, namespace=None):
        args, argv = self.parse_known_args(args, namespace)
        if argv:
            msg = ('unrecognized arguments: %s')
            self.error(msg % ' '.join(argv))

        if self.polyaxon_exp:
            self.polyaxon_exp.log_inputs(**vars(args))

        return args

    def parse_args_from_json(self, json_file):
        with open(json_file, 'r') as fin:
            metadata = json.load(fin)
            self.set_defaults(**metadata)

            args = self.parse_args([
                '--sensor', metadata['sensor'], '--band_ids',
                metadata['band_ids'], '--input_shape', metadata['input_shape'],
                '--resolution',
                str(metadata['resolution'])
            ])
            return args
        return None

    def load_model(self, model_cls, **kwargs):
        """Logs and instantiates a model with a variable number of keyword arguments

        Parameters
        ----------
        model_cls : torch.nn.modules.module.Module
            A pytorch model class to instantiate.
        **kwargs :
            all model positional arguments

        Returns
        -------
        type
            Description of returned object.

        """
        if self.polyaxon_exp:
            self._log_model(model_cls, **kwargs)
        return model_cls(**kwargs)

    @staticmethod
    def _band_ids_sep(band_ids):
        if isinstance(band_ids, list):
            return band_ids
        return band_ids.split(',')

    @staticmethod
    def _input_shape_sep(input_shape):
        if isinstance(input_shape, list):
            return input_shape
        return list(map(int, input_shape.split(',')))

    def _log_model(self, model_cls, **kwargs):
        model_module = getmodule(model_cls).__name__
        model_path = os.path.relpath(getmodule(model_cls).__file__)
        model_name = model_cls.__name__
        s = signature(model_cls)

        self.polyaxon_exp.log_inputs(
            model_path=model_path,
            model_name=model_name,
            model_module=model_module,
            model_args=kwargs,
        )
