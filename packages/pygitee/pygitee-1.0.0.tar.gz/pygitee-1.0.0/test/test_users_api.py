# coding: utf-8


from __future__ import absolute_import

import unittest

from gitee.api.users_api import UsersApi  # noqa: E501


class TestUsersApi(unittest.TestCase):
    """UsersApi unit test stubs"""

    def setUp(self):
        self.api = UsersApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_delete_v5_user_following_username(self):
        """Test case for delete_v5_user_following_username

        取消关注一个用户  # noqa: E501
        """
        pass

    def test_delete_v5_user_keys_id(self):
        """Test case for delete_v5_user_keys_id

        删除一个公钥  # noqa: E501
        """
        pass

    def test_get_v5_user(self):
        """Test case for get_v5_user

        获取授权用户的资料  # noqa: E501
        """
        pass

    def test_get_v5_user_followers(self):
        """Test case for get_v5_user_followers

        列出授权用户的关注者  # noqa: E501
        """
        pass

    def test_get_v5_user_following(self):
        """Test case for get_v5_user_following

        列出授权用户正关注的用户  # noqa: E501
        """
        pass

    def test_get_v5_user_following_username(self):
        """Test case for get_v5_user_following_username

        检查授权用户是否关注了一个用户  # noqa: E501
        """
        pass

    def test_get_v5_user_keys(self):
        """Test case for get_v5_user_keys

        列出授权用户的所有公钥  # noqa: E501
        """
        pass

    def test_get_v5_user_keys_id(self):
        """Test case for get_v5_user_keys_id

        获取一个公钥  # noqa: E501
        """
        pass

    def test_get_v5_user_namespace(self):
        """Test case for get_v5_user_namespace

        获取授权用户的一个 Namespace  # noqa: E501
        """
        pass

    def test_get_v5_user_namespaces(self):
        """Test case for get_v5_user_namespaces

        列出授权用户所有的 Namespace  # noqa: E501
        """
        pass

    def test_get_v5_users_username(self):
        """Test case for get_v5_users_username

        获取一个用户  # noqa: E501
        """
        pass

    def test_get_v5_users_username_followers(self):
        """Test case for get_v5_users_username_followers

        列出指定用户的关注者  # noqa: E501
        """
        pass

    def test_get_v5_users_username_following(self):
        """Test case for get_v5_users_username_following

        列出指定用户正在关注的用户  # noqa: E501
        """
        pass

    def test_get_v5_users_username_following_target_user(self):
        """Test case for get_v5_users_username_following_target_user

        检查指定用户是否关注目标用户  # noqa: E501
        """
        pass

    def test_get_v5_users_username_keys(self):
        """Test case for get_v5_users_username_keys

        列出指定用户的所有公钥  # noqa: E501
        """
        pass

    def test_patch_v5_user(self):
        """Test case for patch_v5_user

        更新授权用户的资料  # noqa: E501
        """
        pass

    def test_post_v5_user_keys(self):
        """Test case for post_v5_user_keys

        添加一个公钥  # noqa: E501
        """
        pass

    def test_put_v5_user_following_username(self):
        """Test case for put_v5_user_following_username

        关注一个用户  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
