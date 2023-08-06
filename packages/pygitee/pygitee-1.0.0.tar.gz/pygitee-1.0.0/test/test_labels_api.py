# coding: utf-8


from __future__ import absolute_import

import unittest

from gitee.api.labels_api import LabelsApi  # noqa: E501


class TestLabelsApi(unittest.TestCase):
    """LabelsApi unit test stubs"""

    def setUp(self):
        self.api = LabelsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_delete_v5_repos_owner_repo_issues_number_labels(self):
        """Test case for delete_v5_repos_owner_repo_issues_number_labels

        删除Issue所有标签  # noqa: E501
        """
        pass

    def test_delete_v5_repos_owner_repo_issues_number_labels_name(self):
        """Test case for delete_v5_repos_owner_repo_issues_number_labels_name

        删除Issue标签  # noqa: E501
        """
        pass

    def test_delete_v5_repos_owner_repo_labels_name(self):
        """Test case for delete_v5_repos_owner_repo_labels_name

        删除一个仓库任务标签  # noqa: E501
        """
        pass

    def test_get_v5_enterprises_enterprise_labels(self):
        """Test case for get_v5_enterprises_enterprise_labels

        获取企业所有标签  # noqa: E501
        """
        pass

    def test_get_v5_enterprises_enterprise_labels_name(self):
        """Test case for get_v5_enterprises_enterprise_labels_name

        获取企业某个标签  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_issues_number_labels(self):
        """Test case for get_v5_repos_owner_repo_issues_number_labels

        获取仓库任务的所有标签  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_labels(self):
        """Test case for get_v5_repos_owner_repo_labels

        获取仓库所有任务标签  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_labels_name(self):
        """Test case for get_v5_repos_owner_repo_labels_name

        根据标签名称获取单个标签  # noqa: E501
        """
        pass

    def test_patch_v5_repos_owner_repo_labels_original_name(self):
        """Test case for patch_v5_repos_owner_repo_labels_original_name

        更新一个仓库任务标签  # noqa: E501
        """
        pass

    def test_post_v5_repos_owner_repo_issues_number_labels(self):
        """Test case for post_v5_repos_owner_repo_issues_number_labels

        创建Issue标签  # noqa: E501
        """
        pass

    def test_post_v5_repos_owner_repo_labels(self):
        """Test case for post_v5_repos_owner_repo_labels

        创建仓库任务标签  # noqa: E501
        """
        pass

    def test_put_v5_repos_owner_repo_issues_number_labels(self):
        """Test case for put_v5_repos_owner_repo_issues_number_labels

        替换Issue所有标签  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
