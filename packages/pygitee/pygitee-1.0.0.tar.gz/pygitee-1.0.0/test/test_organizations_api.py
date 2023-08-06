# coding: utf-8


from __future__ import absolute_import

import unittest

from gitee.api.organizations_api import OrganizationsApi  # noqa: E501


class TestOrganizationsApi(unittest.TestCase):
    """OrganizationsApi unit test stubs"""

    def setUp(self):
        self.api = OrganizationsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_delete_v5_orgs_org_memberships_username(self):
        """Test case for delete_v5_orgs_org_memberships_username

        移除授权用户所管理组织中的成员  # noqa: E501
        """
        pass

    def test_delete_v5_user_memberships_orgs_org(self):
        """Test case for delete_v5_user_memberships_orgs_org

        退出一个组织  # noqa: E501
        """
        pass

    def test_get_v5_orgs_org(self):
        """Test case for get_v5_orgs_org

        获取一个组织  # noqa: E501
        """
        pass

    def test_get_v5_orgs_org_followers(self):
        """Test case for get_v5_orgs_org_followers

        列出指定组织的所有关注者  # noqa: E501
        """
        pass

    def test_get_v5_orgs_org_members(self):
        """Test case for get_v5_orgs_org_members

        列出一个组织的所有成员  # noqa: E501
        """
        pass

    def test_get_v5_orgs_org_memberships_username(self):
        """Test case for get_v5_orgs_org_memberships_username

        获取授权用户所属组织的一个成员  # noqa: E501
        """
        pass

    def test_get_v5_user_memberships_orgs(self):
        """Test case for get_v5_user_memberships_orgs

        列出授权用户在所属组织的成员资料  # noqa: E501
        """
        pass

    def test_get_v5_user_memberships_orgs_org(self):
        """Test case for get_v5_user_memberships_orgs_org

        获取授权用户在一个组织的成员资料  # noqa: E501
        """
        pass

    def test_get_v5_user_orgs(self):
        """Test case for get_v5_user_orgs

        列出授权用户所属的组织  # noqa: E501
        """
        pass

    def test_get_v5_users_username_orgs(self):
        """Test case for get_v5_users_username_orgs

        列出用户所属的组织  # noqa: E501
        """
        pass

    def test_patch_v5_orgs_org(self):
        """Test case for patch_v5_orgs_org

        更新授权用户所管理的组织资料  # noqa: E501
        """
        pass

    def test_patch_v5_user_memberships_orgs_org(self):
        """Test case for patch_v5_user_memberships_orgs_org

        更新授权用户在一个组织的成员资料  # noqa: E501
        """
        pass

    def test_post_v5_users_organization(self):
        """Test case for post_v5_users_organization

        创建组织  # noqa: E501
        """
        pass

    def test_put_v5_orgs_org_memberships_username(self):
        """Test case for put_v5_orgs_org_memberships_username

        增加或更新授权用户所管理组织的成员  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
