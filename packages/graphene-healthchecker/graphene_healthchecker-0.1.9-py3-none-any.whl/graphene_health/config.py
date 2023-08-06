import os
import yaml
import collections
import logging

log = logging.getLogger(__name__)

# Recursive dictionary merge
# Copyright (C) 2016 Paul Durivage <pauldurivage+github@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


def dict_merge(dct, merge_dct):
    """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
        updating only top-level keys, dict_merge recurses down into dicts
        nested to an arbitrary depth, updating keys. The ``merge_dct`` is
        merged into ``dct``.
        :param dct: dict onto which the merge is executed
        :param merge_dct: dct merged into dct
        :return: None
    """
    for k, v in merge_dct.items():
        if (
            k in dct
            and isinstance(dct[k], dict)
            and isinstance(merge_dct[k], collections.Mapping)
        ):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]


class ConfigClass(dict):
    """ This wrapper class allows easy loading and overloading variables of our
        configuration
    """

    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__

    def load_yaml(self, *args):
        o = open(os.path.join(*args))
        d = yaml.load(o.read(), Loader=yaml.SafeLoader)
        dict_merge(self, d)


# load defaults
config = ConfigClass()
config.load_yaml(os.path.dirname(os.path.realpath(__file__)), "config-defaults.yaml")
try:
    config.load_yaml(os.getcwd(), "config.yaml")
except Exception:  # pragma: no cover
    log.info("No config.yaml found in root directory! Using defaults ...")
