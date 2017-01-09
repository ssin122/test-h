# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from pyramid import security
import mock
import pytest

from h.groups import util


def test_world_group_acl():
    group = util.WorldGroup('example.com')

    assert group.__acl__() == [
        (security.Allow, security.Everyone, 'read'),
        (security.Allow, 'authority:example.com', 'write'),
        security.DENY_ALL,
    ]


@pytest.mark.usefixtures('group_service')
class TestFetchGroup(object):
    def test_it_returns_correct_group_for_world_group(self, pyramid_request):
        group = util.fetch_group(pyramid_request, '__world__')
        assert isinstance(group, util.WorldGroup)

    def test_it_fetches_group(self, pyramid_request, group_service):
        util.fetch_group(pyramid_request, 'abcde')

        group_service.fetch.assert_called_once_with('abcde')

    def test_it_returns_fetched_group(self, pyramid_request, group_service):
        result = util.fetch_group(pyramid_request, 'abcde')
        assert result == group_service.fetch.return_value

    @pytest.fixture
    def group_service(self, pyramid_config):
        service = mock.Mock(spec_set=['fetch'])
        service.fetch.return_value = None
        pyramid_config.register_service(service, name='group')
        return service
