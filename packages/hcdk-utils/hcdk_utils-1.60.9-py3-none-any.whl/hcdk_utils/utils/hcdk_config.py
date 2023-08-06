import deepmerge
import io
import os
import yaml


class HcdkConfig(object):
    sentia = ''
    client = ''

    def __init__(
        self,
        sentia_folder: str = 'config/sentia',
        client_folder: str = 'config/client'
    ) -> None:
        self.sentia = sentia_folder
        self.client = client_folder
        self.merger = deepmerge.Merger(
            # pass in a list of tuple, with the
            # strategies you are looking to apply
            # to each type.
            [
                (list, ["override"]),
                (dict, ["merge"])
            ],
            # next, choose the fallback strategies,
            # applied to all other types:
            ["override"],
            # finally, choose the strategies in
            # the case where the types conflict:
            ["override"]
        )

    def _config_path(
        self,
        place: str,
        config: str,
        sub: str,
        environment: str
    ) -> io.TextIOWrapper:
        config_file = os.path.join(getattr(self, place), config)
        if sub:
            config_file = os.path.join(config_file, sub)
        config_file = os.path.join(config_file, f'{environment}.yml')

        if os.path.isfile(config_file):
            config_file = open(
                os.path.join(config_file),
                'r'
            )
            return config_file

        return None

    def get_config(
        self,
        config: str,
        environment: str,
        sub: str = None
    ) -> dict:
        sentia_config_file = self._config_path(
            place='sentia',
            config=config,
            sub=sub,
            environment=environment
        )
        sentia_config = {}
        if sentia_config_file:
            sentia_config = yaml.safe_load(sentia_config_file)

        client_config_file = self._config_path(
            place='client',
            config=config,
            sub=sub,
            environment=environment
        )
        client_config = {}
        if client_config_file:
            client_config = yaml.safe_load(client_config_file)

        return self.merger.merge(client_config, sentia_config)
