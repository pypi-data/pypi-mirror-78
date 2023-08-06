# coding: utf-8


from __future__ import absolute_import

import unittest

from gitee.api.miscellaneous_api import MiscellaneousApi  # noqa: E501


class TestMiscellaneousApi(unittest.TestCase):
    """MiscellaneousApi unit test stubs"""

    def setUp(self):
        self.api = MiscellaneousApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_v5_emojis(self):
        """Test case for get_v5_emojis

        列出可使用的 Emoji  # noqa: E501
        """
        pass

    def test_get_v5_gitignore_templates(self):
        """Test case for get_v5_gitignore_templates

        列出可使用的 .gitignore 模板  # noqa: E501
        """
        pass

    def test_get_v5_gitignore_templates_name(self):
        """Test case for get_v5_gitignore_templates_name

        获取一个 .gitignore 模板  # noqa: E501
        """
        pass

    def test_get_v5_gitignore_templates_name_raw(self):
        """Test case for get_v5_gitignore_templates_name_raw

        获取一个 .gitignore 模板原始文件  # noqa: E501
        """
        pass

    def test_get_v5_licenses(self):
        """Test case for get_v5_licenses

        列出可使用的开源许可协议  # noqa: E501
        """
        pass

    def test_get_v5_licenses_license(self):
        """Test case for get_v5_licenses_license

        获取一个开源许可协议  # noqa: E501
        """
        pass

    def test_get_v5_licenses_license_raw(self):
        """Test case for get_v5_licenses_license_raw

        获取一个开源许可协议原始文件  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_license(self):
        """Test case for get_v5_repos_owner_repo_license

        获取一个仓库使用的开源许可协议  # noqa: E501
        """
        pass

    def test_post_v5_markdown(self):
        """Test case for post_v5_markdown

        渲染 Markdown 文本  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
