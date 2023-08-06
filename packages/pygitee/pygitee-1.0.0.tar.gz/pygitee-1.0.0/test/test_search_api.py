# coding: utf-8


from __future__ import absolute_import

import unittest

from gitee.api.search_api import SearchApi  # noqa: E501


class TestSearchApi(unittest.TestCase):
    """SearchApi unit test stubs"""

    def setUp(self):
        self.api = SearchApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_v5_search_issues(self):
        """Test case for get_v5_search_issues

        搜索 Issues  # noqa: E501
        """
        pass

    def test_get_v5_search_repositories(self):
        """Test case for get_v5_search_repositories

        搜索仓库  # noqa: E501
        """
        pass

    def test_get_v5_search_users(self):
        """Test case for get_v5_search_users

        搜索用户  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
