# vim:set ts=4 sw=4 et nowrap syntax=python ff=unix:
#
# Copyright 2020 Mark Crewson <mark@crewson.net>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ..builder.base import BaseLockLoader
from ..framew.cmdapplication import Subcommand
from ..framew.outputter import SingleOutputter
from ..forge import Forge

##############################################################################


class InfoCommand (Subcommand):
    """
    Display information about the modpack.
    """

    name = 'info'

    def setup(self):
        super(InfoCommand, self).setup()
        self.lockloader = BaseLockLoader()
        self.outputter = SingleOutputter()

    def get_cmdline_parser(self):
        parser = super(InfoCommand, self).get_cmdline_parser()
        self.lockloader.add_cmdline_args(parser)
        self.outputter.add_argument_group(parser)
        return parser

    def run_command(self, arguments):
        self.lockloader.setup_packlocks(arguments)
        packlock = self.lockloader.packlock

        metadata = packlock.get_all_metadata()
        keys = [k for k in metadata.keys()]
        vals = [v for v in metadata.values()]

        if packlock.get_metadata('forge_version') is not None:
            forge = Forge(packlock.get_metadata('minecraft_version'),
                          packlock.get_metadata('forge_version'),
                          None)
            keys.append('forge_jarfile')
            vals.append(forge.get_server_jar_filename())

        self.outputter.produce_output(arguments, keys, vals)
