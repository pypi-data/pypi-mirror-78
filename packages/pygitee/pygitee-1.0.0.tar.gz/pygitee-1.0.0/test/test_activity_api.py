# coding: utf-8


from __future__ import absolute_import

import unittest

from gitee.api.activity_api import ActivityApi  # noqa: E501


class TestActivityApi(unittest.TestCase):
    """ActivityApi unit test stubs"""

    def setUp(self):
        self.api = ActivityApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_delete_v5_user_starred_owner_repo(self):
        """Test case for delete_v5_user_starred_owner_repo

        取消 star 一个仓库  # noqa: E501
        """
        pass

    def test_delete_v5_user_subscriptions_owner_repo(self):
        """Test case for delete_v5_user_subscriptions_owner_repo

        取消 watch 一个仓库  # noqa: E501
        """
        pass

    def test_get_v5_networks_owner_repo_events(self):
        """Test case for get_v5_networks_owner_repo_events

        列出仓库的所有公开动态  # noqa: E501
        """
        pass

    def test_get_v5_notifications_count(self):
        """Test case for get_v5_notifications_count

        获取授权用户的通知数  # noqa: E501
        """
        pass

    def test_get_v5_notifications_messages(self):
        """Test case for get_v5_notifications_messages

        列出授权用户的所有私信  # noqa: E501
        """
        pass

    def test_get_v5_notifications_messages_id(self):
        """Test case for get_v5_notifications_messages_id

        获取一条私信  # noqa: E501
        """
        pass

    def test_get_v5_notifications_threads(self):
        """Test case for get_v5_notifications_threads

        列出授权用户的所有通知  # noqa: E501
        """
        pass

    def test_get_v5_notifications_threads_id(self):
        """Test case for get_v5_notifications_threads_id

        获取一条通知  # noqa: E501
        """
        pass

    def test_get_v5_orgs_org_events(self):
        """Test case for get_v5_orgs_org_events

        列出组织的公开动态  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_events(self):
        """Test case for get_v5_repos_owner_repo_events

        列出仓库的所有动态  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_notifications(self):
        """Test case for get_v5_repos_owner_repo_notifications

        列出一个仓库里的通知  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_stargazers(self):
        """Test case for get_v5_repos_owner_repo_stargazers

        列出 star 了仓库的用户  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_subscribers(self):
        """Test case for get_v5_repos_owner_repo_subscribers

        列出 watch 了仓库的用户  # noqa: E501
        """
        pass

    def test_get_v5_user_starred(self):
        """Test case for get_v5_user_starred

        列出授权用户 star 了的仓库  # noqa: E501
        """
        pass

    def test_get_v5_user_starred_owner_repo(self):
        """Test case for get_v5_user_starred_owner_repo

        检查授权用户是否 star 了一个仓库  # noqa: E501
        """
        pass

    def test_get_v5_user_subscriptions(self):
        """Test case for get_v5_user_subscriptions

        列出授权用户 watch 了的仓库  # noqa: E501
        """
        pass

    def test_get_v5_user_subscriptions_owner_repo(self):
        """Test case for get_v5_user_subscriptions_owner_repo

        检查授权用户是否 watch 了一个仓库  # noqa: E501
        """
        pass

    def test_get_v5_users_username_events(self):
        """Test case for get_v5_users_username_events

        列出用户的动态  # noqa: E501
        """
        pass

    def test_get_v5_users_username_events_orgs_org(self):
        """Test case for get_v5_users_username_events_orgs_org

        列出用户所属组织的动态  # noqa: E501
        """
        pass

    def test_get_v5_users_username_events_public(self):
        """Test case for get_v5_users_username_events_public

        列出用户的公开动态  # noqa: E501
        """
        pass

    def test_get_v5_users_username_received_events(self):
        """Test case for get_v5_users_username_received_events

        列出一个用户收到的动态  # noqa: E501
        """
        pass

    def test_get_v5_users_username_received_events_public(self):
        """Test case for get_v5_users_username_received_events_public

        列出一个用户收到的公开动态  # noqa: E501
        """
        pass

    def test_get_v5_users_username_starred(self):
        """Test case for get_v5_users_username_starred

        列出用户 star 了的仓库  # noqa: E501
        """
        pass

    def test_get_v5_users_username_subscriptions(self):
        """Test case for get_v5_users_username_subscriptions

        列出用户 watch 了的仓库  # noqa: E501
        """
        pass

    def test_patch_v5_notifications_messages_id(self):
        """Test case for patch_v5_notifications_messages_id

        标记一条私信为已读  # noqa: E501
        """
        pass

    def test_patch_v5_notifications_threads_id(self):
        """Test case for patch_v5_notifications_threads_id

        标记一条通知为已读  # noqa: E501
        """
        pass

    def test_post_v5_notifications_messages(self):
        """Test case for post_v5_notifications_messages

        发送私信给指定用户  # noqa: E501
        """
        pass

    def test_put_v5_notifications_messages(self):
        """Test case for put_v5_notifications_messages

        标记所有私信为已读  # noqa: E501
        """
        pass

    def test_put_v5_notifications_threads(self):
        """Test case for put_v5_notifications_threads

        标记所有通知为已读  # noqa: E501
        """
        pass

    def test_put_v5_repos_owner_repo_notifications(self):
        """Test case for put_v5_repos_owner_repo_notifications

        标记一个仓库里的通知为已读  # noqa: E501
        """
        pass

    def test_put_v5_user_starred_owner_repo(self):
        """Test case for put_v5_user_starred_owner_repo

        star 一个仓库  # noqa: E501
        """
        pass

    def test_put_v5_user_subscriptions_owner_repo(self):
        """Test case for put_v5_user_subscriptions_owner_repo

        watch 一个仓库  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
