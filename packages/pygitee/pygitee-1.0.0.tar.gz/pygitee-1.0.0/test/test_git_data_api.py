# coding: utf-8


from __future__ import absolute_import

import unittest

from gitee.api.git_data_api import GitDataApi  # noqa: E501


class TestGitDataApi(unittest.TestCase):
    """GitDataApi unit test stubs"""

    def setUp(self):
        self.api = GitDataApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_v5_repos_owner_repo_git_blobs_sha(self):
        """Test case for get_v5_repos_owner_repo_git_blobs_sha

        获取文件Blob  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_git_trees_sha(self):
        """Test case for get_v5_repos_owner_repo_git_trees_sha

        获取目录Tree  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
