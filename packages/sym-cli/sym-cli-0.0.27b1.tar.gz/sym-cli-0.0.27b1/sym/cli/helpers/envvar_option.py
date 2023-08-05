import os

from click import Option
from click_option_group import GroupedOption

from ..helpers.util import wrap

_used = {}


def get_used():
    return _used


def _value_from_envvar(self, value):
    if value:
        for envvar in wrap(self.envvar):
            if envvar in os.environ:
                _used[envvar] = (self.name, value)
                break
    return value


class EnvvarOption(Option):
    def value_from_envvar(self, ctx):
        value = super().value_from_envvar(ctx)
        return _value_from_envvar(self, value)


class EnvvarGroupedOption(GroupedOption):
    def value_from_envvar(self, ctx):
        value = super().value_from_envvar(ctx)
        return _value_from_envvar(self, value)

