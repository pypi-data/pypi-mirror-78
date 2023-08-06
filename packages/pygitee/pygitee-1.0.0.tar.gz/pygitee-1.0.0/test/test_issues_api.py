# coding: utf-8


from __future__ import absolute_import

import unittest

import gitee
from gitee.api.issues_api import IssuesApi  # noqa: E501


class TestIssuesApi(unittest.TestCase):
    """IssuesApi unit test stubs"""

    def setUp(self):
        self.api = IssuesApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_delete_v5_repos_owner_repo_issues_comments_id(self):
        """Test case for delete_v5_repos_owner_repo_issues_comments_id

        删除Issue某条评论  # noqa: E501
        """
        pass

    def test_get_v5_enterprises_enterprise_issues(self):
        """Test case for get_v5_enterprises_enterprise_issues

        获取某个企业的所有Issues  # noqa: E501
        """
        pass

    def test_get_v5_enterprises_enterprise_issues_number(self):
        """Test case for get_v5_enterprises_enterprise_issues_number

        获取企业的某个Issue  # noqa: E501
        """
        pass

    def test_get_v5_enterprises_enterprise_issues_number_comments(self):
        """Test case for get_v5_enterprises_enterprise_issues_number_comments

        获取企业某个Issue所有评论  # noqa: E501
        """
        pass

    def test_get_v5_enterprises_enterprise_issues_number_labels(self):
        """Test case for get_v5_enterprises_enterprise_issues_number_labels

        获取企业某个Issue所有标签  # noqa: E501
        """
        pass

    def test_get_v5_issues(self):
        """Test case for get_v5_issues

        获取当前授权用户的所有Issues  # noqa: E501
        """
        pass

    def test_get_v5_orgs_org_issues(self):
        """Test case for get_v5_orgs_org_issues

        获取当前用户某个组织的Issues  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_issues_number_operate_logs(self):
        """Test case for get_v5_repos_owner_issues_number_operate_logs

        获取某个Issue下的操作日志  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_issues(self):
        """Test case for get_v5_repos_owner_repo_issues

        仓库的所有Issues  # noqa: E501
        """
        # create an instance of the API class
        api_instance = gitee.IssuesApi(gitee.ApiClient())
        print(api_instance.get_v5_repos_owner_repo_issues("kingreatwill", "kingreatwill"))
        pass

    def test_get_v5_repos_owner_repo_issues_comments(self):
        """Test case for get_v5_repos_owner_repo_issues_comments

        获取仓库所有Issue的评论  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_issues_comments_id(self):
        """Test case for get_v5_repos_owner_repo_issues_comments_id

        获取仓库Issue某条评论  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_issues_number(self):
        """Test case for get_v5_repos_owner_repo_issues_number

        仓库的某个Issue  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_issues_number_comments(self):
        """Test case for get_v5_repos_owner_repo_issues_number_comments

        获取仓库某个Issue所有的评论  # noqa: E501
        """
        pass

    def test_get_v5_user_issues(self):
        """Test case for get_v5_user_issues

        获取授权用户的所有Issues  # noqa: E501
        """
        pass

    def test_patch_v5_repos_owner_issues_number(self):
        """Test case for patch_v5_repos_owner_issues_number

        更新Issue  # noqa: E501
        """
        pass

    def test_patch_v5_repos_owner_repo_issues_comments_id(self):
        """Test case for patch_v5_repos_owner_repo_issues_comments_id

        更新Issue某条评论  # noqa: E501
        """
        pass

    def test_post_v5_repos_owner_issues(self):
        """Test case for post_v5_repos_owner_issues

        创建Issue  # noqa: E501
        """
        pass

    def test_post_v5_repos_owner_repo_issues_number_comments(self):
        """Test case for post_v5_repos_owner_repo_issues_number_comments

        创建某个Issue评论  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
