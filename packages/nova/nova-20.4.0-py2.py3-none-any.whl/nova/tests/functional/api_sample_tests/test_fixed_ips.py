# Copyright 2014 IBM Corp.
#
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


from nova.tests.functional.api import client as api_client
from nova.tests.functional import api_samples_test_base


class FixedIpTest(api_samples_test_base.ApiSampleTestBase):
    api_major_version = 'v2'

    def test_fixed_ip_reserve(self):
        ex = self.assertRaises(api_client.OpenStackApiException,
                               self.api.api_post,
                               '/os-fixed-ips/192.168.1.1/action',
                               {"reserve": None})
        self.assertEqual(410, ex.response.status_code)

    def test_get_fixed_ip(self):
        ex = self.assertRaises(api_client.OpenStackApiException,
                               self.api.api_get, '/os-fixed-ips/192.168.1.1')
        self.assertEqual(410, ex.response.status_code)
