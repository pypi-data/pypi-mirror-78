# coding: utf-8


from __future__ import absolute_import

import unittest

from gitee.api.gists_api import GistsApi  # noqa: E501


class TestGistsApi(unittest.TestCase):
    """GistsApi unit test stubs"""

    def setUp(self):
        self.api = GistsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_delete_v5_gists_gist_id_comments_id(self):
        """Test case for delete_v5_gists_gist_id_comments_id

        删除代码片段的评论  # noqa: E501
        """
        pass

    def test_delete_v5_gists_id(self):
        """Test case for delete_v5_gists_id

        删除指定代码片段  # noqa: E501
        """
        pass

    def test_delete_v5_gists_id_star(self):
        """Test case for delete_v5_gists_id_star

        取消Star代码片段  # noqa: E501
        """
        pass

    def test_get_v5_gists(self):
        """Test case for get_v5_gists

        获取代码片段  # noqa: E501
        """
        pass

    def test_get_v5_gists_gist_id_comments(self):
        """Test case for get_v5_gists_gist_id_comments

        获取代码片段的评论  # noqa: E501
        """
        pass

    def test_get_v5_gists_gist_id_comments_id(self):
        """Test case for get_v5_gists_gist_id_comments_id

        获取单条代码片段的评论  # noqa: E501
        """
        pass

    def test_get_v5_gists_id(self):
        """Test case for get_v5_gists_id

        获取单条代码片段  # noqa: E501
        """
        pass

    def test_get_v5_gists_id_commits(self):
        """Test case for get_v5_gists_id_commits

        获取代码片段的commit  # noqa: E501
        """
        pass

    def test_get_v5_gists_id_forks(self):
        """Test case for get_v5_gists_id_forks

        获取 Fork 了指定代码片段的列表  # noqa: E501
        """
        pass

    def test_get_v5_gists_id_star(self):
        """Test case for get_v5_gists_id_star

        判断代码片段是否已Star  # noqa: E501
        """
        pass

    def test_get_v5_gists_starred(self):
        """Test case for get_v5_gists_starred

        获取用户Star的代码片段  # noqa: E501
        """
        pass

    def test_patch_v5_gists_gist_id_comments_id(self):
        """Test case for patch_v5_gists_gist_id_comments_id

        修改代码片段的评论  # noqa: E501
        """
        pass

    def test_patch_v5_gists_id(self):
        """Test case for patch_v5_gists_id

        修改代码片段  # noqa: E501
        """
        pass

    def test_post_v5_gists(self):
        """Test case for post_v5_gists

        创建代码片段  # noqa: E501
        """
        pass

    def test_post_v5_gists_gist_id_comments(self):
        """Test case for post_v5_gists_gist_id_comments

        增加代码片段的评论  # noqa: E501
        """
        pass

    def test_post_v5_gists_id_forks(self):
        """Test case for post_v5_gists_id_forks

        Fork代码片段  # noqa: E501
        """
        pass

    def test_put_v5_gists_id_star(self):
        """Test case for put_v5_gists_id_star

        Star代码片段  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
