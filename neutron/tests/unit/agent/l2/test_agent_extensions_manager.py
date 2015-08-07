#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock
from oslo_config import cfg

from neutron.agent.l2 import agent_extensions_manager
from neutron.tests import base


class TestAgentExtensionsManager(base.BaseTestCase):

    def setUp(self):
        super(TestAgentExtensionsManager, self).setUp()
        mock.patch('neutron.agent.l2.extensions.qos_agent.QosAgentExtension',
                   autospec=True).start()
        conf = cfg.CONF
        agent_extensions_manager.register_opts(conf)
        cfg.CONF.set_override('extensions', ['qos'], 'agent')
        self.manager = agent_extensions_manager.AgentExtensionsManager(conf)

    def _get_extension(self):
        return self.manager.extensions[0].obj

    def test_initialize(self):
        self.manager.initialize()
        ext = self._get_extension()
        self.assertTrue(ext.initialize.called)

    def test_handle_port(self):
        context = object()
        data = object()
        self.manager.handle_port(context, data)
        ext = self._get_extension()
        ext.handle_port.assert_called_once_with(context, data)