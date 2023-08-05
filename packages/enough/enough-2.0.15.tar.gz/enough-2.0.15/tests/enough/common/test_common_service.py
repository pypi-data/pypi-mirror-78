import os
import pytest
import requests_mock as requests_mock_module
import shutil

from enough import settings
from enough.common import service


@pytest.mark.skipif('SKIP_OPENSTACK_INTEGRATION_TESTS' in os.environ,
                    reason='skip integration test')
def test_openstack_create_or_update(tmpdir, openstack_name, requests_mock):
    shutil.copy('infrastructure_key', f'{tmpdir}/infrastructure_key')
    shutil.copy('infrastructure_key.pub', f'{tmpdir}/infrastructure_key.pub')
    requests_mock.post(requests_mock_module.ANY, status_code=201)
    requests_mock.get(requests_mock_module.ANY, status_code=200)
    domain = f'enough.test'
    s = service.ServiceOpenStack(str(tmpdir), settings.SHARE_DIR, **{
        'driver': 'openstack',
        'playbook': os.path.abspath('tests/enough/common/test_common_service/enough-playbook.yml'),
        'domain': domain,
        'name': 'essential',
        'cloud': 'production',
    })
    s.dotenough.set_certificate('ownca')
    s.dotenough.set_clouds_file('inventory/group_vars/all/clouds.yml')
    r = s.create_or_update()
    assert r['fqdn'] == f'essential.{domain}'
    # the second time around the hosts.yml are reused
    r = s.create_or_update()
    assert r['fqdn'] == f'essential.{domain}'


def test_service_from_host():
    s = service.Service(settings.CONFIG_DIR, settings.SHARE_DIR, domain='test.com')
    assert s.service_from_host('icinga-host') is None
    assert s.service_from_host('cloud-host') == 'cloud'
    assert s.service_from_host('unknown-host') is None


def test_set_service_info():
    s = service.Service(settings.CONFIG_DIR, settings.SHARE_DIR, domain='test.com')
    assert 'bind-host' in s.service2hosts['bind']
    assert len(s.service2hosts['bind']) > 0
    assert ['bind-host'] == s.service2group['bind']


def test_update_vpn_dependencies():
    s = service.Service(settings.CONFIG_DIR, settings.SHARE_DIR, domain='test.com')
    assert s.hosts_with_internal_network(['bind-host']) == []
    assert 'website-host' not in s.service2hosts['openvpn']
    assert 'website-host' not in s.service2hosts['weblate']
    s.ansible.set_inventories(['tests/enough/common/test_common_service/vpn_inventory'])
    s.set_service_info()
    assert 'website-host' in s.service2hosts['openvpn']
    assert s.hosts_with_internal_network(['icinga-host']) == ['icinga-host']
    s.update_vpn_dependencies()
    assert 'website-host' not in s.service2hosts['weblate']
    assert 'weblate-host' in s.service2hosts['weblate']


def test_ensure_non_empty_service_group(tmpdir):
    name = 'wekan'
    s = service.Service(tmpdir, settings.SHARE_DIR,
                        name=name,
                        domain='test.com')
    with pytest.raises(service.Service.NoHost):
        s.ensure_non_empty_service_group()
    host = 'HOST'
    s = service.Service(tmpdir, settings.SHARE_DIR,
                        name=name,
                        host=host,
                        domain='test.com')
    hosts = s.ensure_non_empty_service_group()
    assert hosts == [host]
    assert hosts == s.ensure_non_empty_service_group()
