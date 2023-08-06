#
# Copyright (C) 2020 Prof_Bloodstone.
#
# This file is part of mineager
# (see https://github.com/Prof-Bloodstone/Mineager).
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
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#
from . import Config
from . import Plugin

import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class YamlConfig(Config):

    def load(self) -> list[Plugin]:
        with self._file.open('r') as stream:
            data = yaml.safe_load(stream, Loader=Loader)
        return self.parse_plugins(data)

    def save(self, data) -> None:
        dump = yaml.dump(
            data,
            Dumper=Dumper,
            # Always use block-styled instead of collection-styled dump
            default_flow_style=False
        )
        with self._file.open('w') as f:
            f.write(dump)
