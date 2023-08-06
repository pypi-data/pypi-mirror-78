# coding: utf-8


from __future__ import absolute_import

import unittest

from gitee.api.milestones_api import MilestonesApi  # noqa: E501


class TestMilestonesApi(unittest.TestCase):
    """MilestonesApi unit test stubs"""

    def setUp(self):
        self.api = MilestonesApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_delete_v5_repos_owner_repo_milestones_number(self):
        """Test case for delete_v5_repos_owner_repo_milestones_number

        删除仓库单个里程碑  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_milestones(self):
        """Test case for get_v5_repos_owner_repo_milestones

        获取仓库所有里程碑  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_milestones_number(self):
        """Test case for get_v5_repos_owner_repo_milestones_number

        获取仓库单个里程碑  # noqa: E501
        """
        pass

    def test_patch_v5_repos_owner_repo_milestones_number(self):
        """Test case for patch_v5_repos_owner_repo_milestones_number

        更新仓库里程碑  # noqa: E501
        """
        pass

    def test_post_v5_repos_owner_repo_milestones(self):
        """Test case for post_v5_repos_owner_repo_milestones

        创建仓库里程碑  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
