# coding: utf-8


from __future__ import absolute_import

import unittest

from gitee.api.enterprises_api import EnterprisesApi  # noqa: E501


class TestEnterprisesApi(unittest.TestCase):
    """EnterprisesApi unit test stubs"""

    def setUp(self):
        self.api = EnterprisesApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_delete_v5_enterprises_enterprise_members_username(self):
        """Test case for delete_v5_enterprises_enterprise_members_username

        移除企业成员  # noqa: E501
        """
        pass

    def test_delete_v5_enterprises_enterprise_week_reports_report_id_comments_id(self):
        """Test case for delete_v5_enterprises_enterprise_week_reports_report_id_comments_id

        删除周报某个评论  # noqa: E501
        """
        pass

    def test_get_v5_enterprise_enterprise_pull_requests(self):
        """Test case for get_v5_enterprise_enterprise_pull_requests

        企业Pull Reuqest 列表  # noqa: E501
        """
        pass

    def test_get_v5_enterprises_enterprise(self):
        """Test case for get_v5_enterprises_enterprise

        获取一个企业  # noqa: E501
        """
        pass

    def test_get_v5_enterprises_enterprise_members(self):
        """Test case for get_v5_enterprises_enterprise_members

        列出企业的所有成员  # noqa: E501
        """
        pass

    def test_get_v5_enterprises_enterprise_members_username(self):
        """Test case for get_v5_enterprises_enterprise_members_username

        获取企业的一个成员  # noqa: E501
        """
        pass

    def test_get_v5_enterprises_enterprise_users_username_week_reports(self):
        """Test case for get_v5_enterprises_enterprise_users_username_week_reports

        个人周报列表  # noqa: E501
        """
        pass

    def test_get_v5_enterprises_enterprise_week_reports(self):
        """Test case for get_v5_enterprises_enterprise_week_reports

        企业成员周报列表  # noqa: E501
        """
        pass

    def test_get_v5_enterprises_enterprise_week_reports_id(self):
        """Test case for get_v5_enterprises_enterprise_week_reports_id

        周报详情  # noqa: E501
        """
        pass

    def test_get_v5_enterprises_enterprise_week_reports_id_comments(self):
        """Test case for get_v5_enterprises_enterprise_week_reports_id_comments

        某个周报评论列表  # noqa: E501
        """
        pass

    def test_get_v5_user_enterprises(self):
        """Test case for get_v5_user_enterprises

        列出授权用户所属的企业  # noqa: E501
        """
        pass

    def test_patch_v5_enterprises_enterprise_week_report_id(self):
        """Test case for patch_v5_enterprises_enterprise_week_report_id

        编辑周报  # noqa: E501
        """
        pass

    def test_post_v5_enterprises_enterprise_members(self):
        """Test case for post_v5_enterprises_enterprise_members

        添加或邀请企业成员  # noqa: E501
        """
        pass

    def test_post_v5_enterprises_enterprise_week_report(self):
        """Test case for post_v5_enterprises_enterprise_week_report

        新建周报  # noqa: E501
        """
        pass

    def test_post_v5_enterprises_enterprise_week_reports_id_comment(self):
        """Test case for post_v5_enterprises_enterprise_week_reports_id_comment

        评论周报  # noqa: E501
        """
        pass

    def test_put_v5_enterprises_enterprise_members_username(self):
        """Test case for put_v5_enterprises_enterprise_members_username

        修改企业成员权限或备注  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
