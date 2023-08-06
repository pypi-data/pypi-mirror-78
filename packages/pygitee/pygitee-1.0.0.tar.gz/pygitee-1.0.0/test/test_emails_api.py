# coding: utf-8


from __future__ import absolute_import

import unittest

from gitee.api.emails_api import EmailsApi  # noqa: E501


class TestEmailsApi(unittest.TestCase):
    """EmailsApi unit test stubs"""

    def setUp(self):
        self.api = EmailsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_v5_emails(self):
        """Test case for get_v5_emails

        获取授权用户的全部邮箱  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
