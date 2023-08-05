from icinga2api.exceptions import Icinga2ApiException
from tests.icinga_helper import IcingaHelper
import pytest

testinfra_hosts = ['ansible://icinga-host']


class TestChecks(IcingaHelper):

    def test_icinga_host(self):
        objects = self.get_client().objects
        r = objects.get('Host', 'bind-host')
        assert r['attrs']['name'] == 'bind-host'
        with pytest.raises(Icinga2ApiException):
            objects.get('Host', 'deleted-host')

    def test_disk(self):
        assert self.is_service_ok('website-host!disk')
        assert self.is_service_ok('packages-host!disk')

    def test_icinga_ntp_time(self):
        assert self.is_service_ok('website-host!systemd-timesyncd is working')

    def test_memory(self):
        assert self.is_service_ok('icinga-host!memory')
        assert self.is_service_ok('website-host!memory')
