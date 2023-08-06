# coding: utf-8


from __future__ import absolute_import

import unittest

from gitee.api.pull_requests_api import PullRequestsApi  # noqa: E501


class TestPullRequestsApi(unittest.TestCase):
    """PullRequestsApi unit test stubs"""

    def setUp(self):
        self.api = PullRequestsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_delete_v5_repos_owner_repo_pulls_comments_id(self):
        """Test case for delete_v5_repos_owner_repo_pulls_comments_id

        删除评论  # noqa: E501
        """
        pass

    def test_delete_v5_repos_owner_repo_pulls_number_assignees(self):
        """Test case for delete_v5_repos_owner_repo_pulls_number_assignees

        取消用户审查 Pull Request  # noqa: E501
        """
        pass

    def test_delete_v5_repos_owner_repo_pulls_number_labels_name(self):
        """Test case for delete_v5_repos_owner_repo_pulls_number_labels_name

        删除 Pull Request 标签  # noqa: E501
        """
        pass

    def test_delete_v5_repos_owner_repo_pulls_number_testers(self):
        """Test case for delete_v5_repos_owner_repo_pulls_number_testers

        取消用户测试 Pull Request  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_pulls(self):
        """Test case for get_v5_repos_owner_repo_pulls

        获取Pull Request列表  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_pulls_comments(self):
        """Test case for get_v5_repos_owner_repo_pulls_comments

        获取该仓库下的所有Pull Request评论  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_pulls_comments_id(self):
        """Test case for get_v5_repos_owner_repo_pulls_comments_id

        获取Pull Request的某个评论  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_pulls_number(self):
        """Test case for get_v5_repos_owner_repo_pulls_number

        获取单个Pull Request  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_pulls_number_comments(self):
        """Test case for get_v5_repos_owner_repo_pulls_number_comments

        获取某个Pull Request的所有评论  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_pulls_number_commits(self):
        """Test case for get_v5_repos_owner_repo_pulls_number_commits

        获取某Pull Request的所有Commit信息。最多显示250条Commit  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_pulls_number_files(self):
        """Test case for get_v5_repos_owner_repo_pulls_number_files

        Pull Request Commit文件列表。最多显示300条diff  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_pulls_number_issues(self):
        """Test case for get_v5_repos_owner_repo_pulls_number_issues

        获取 Pull Request 关联的 issues  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_pulls_number_labels(self):
        """Test case for get_v5_repos_owner_repo_pulls_number_labels

        获取某个 Pull Request 的所有标签  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_pulls_number_merge(self):
        """Test case for get_v5_repos_owner_repo_pulls_number_merge

        判断Pull Request是否已经合并  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_pulls_number_operate_logs(self):
        """Test case for get_v5_repos_owner_repo_pulls_number_operate_logs

        获取某个Pull Request的操作日志  # noqa: E501
        """
        pass

    def test_patch_v5_repos_owner_repo_pulls_comments_id(self):
        """Test case for patch_v5_repos_owner_repo_pulls_comments_id

        编辑评论  # noqa: E501
        """
        pass

    def test_patch_v5_repos_owner_repo_pulls_number(self):
        """Test case for patch_v5_repos_owner_repo_pulls_number

        更新Pull Request信息  # noqa: E501
        """
        pass

    def test_patch_v5_repos_owner_repo_pulls_number_assignees(self):
        """Test case for patch_v5_repos_owner_repo_pulls_number_assignees

        重置 Pull Request 审查 的状态  # noqa: E501
        """
        pass

    def test_patch_v5_repos_owner_repo_pulls_number_testers(self):
        """Test case for patch_v5_repos_owner_repo_pulls_number_testers

        重置 Pull Request 测试 的状态  # noqa: E501
        """
        pass

    def test_post_v5_repos_owner_repo_pulls(self):
        """Test case for post_v5_repos_owner_repo_pulls

        创建Pull Request  # noqa: E501
        """
        pass

    def test_post_v5_repos_owner_repo_pulls_number_assignees(self):
        """Test case for post_v5_repos_owner_repo_pulls_number_assignees

        指派用户审查 Pull Request  # noqa: E501
        """
        pass

    def test_post_v5_repos_owner_repo_pulls_number_comments(self):
        """Test case for post_v5_repos_owner_repo_pulls_number_comments

        提交Pull Request评论  # noqa: E501
        """
        pass

    def test_post_v5_repos_owner_repo_pulls_number_labels(self):
        """Test case for post_v5_repos_owner_repo_pulls_number_labels

        创建 Pull Request 标签  # noqa: E501
        """
        pass

    def test_post_v5_repos_owner_repo_pulls_number_review(self):
        """Test case for post_v5_repos_owner_repo_pulls_number_review

        处理 Pull Request 审查  # noqa: E501
        """
        pass

    def test_post_v5_repos_owner_repo_pulls_number_test(self):
        """Test case for post_v5_repos_owner_repo_pulls_number_test

        处理 Pull Request 测试  # noqa: E501
        """
        pass

    def test_post_v5_repos_owner_repo_pulls_number_testers(self):
        """Test case for post_v5_repos_owner_repo_pulls_number_testers

        指派用户测试 Pull Request  # noqa: E501
        """
        pass

    def test_put_v5_repos_owner_repo_pulls_number_labels(self):
        """Test case for put_v5_repos_owner_repo_pulls_number_labels

        替换 Pull Request 所有标签  # noqa: E501
        """
        pass

    def test_put_v5_repos_owner_repo_pulls_number_merge(self):
        """Test case for put_v5_repos_owner_repo_pulls_number_merge

        合并Pull Request  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
