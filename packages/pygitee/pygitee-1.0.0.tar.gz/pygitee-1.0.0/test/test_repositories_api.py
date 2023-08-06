# coding: utf-8


from __future__ import absolute_import

import unittest

from gitee.api.repositories_api import RepositoriesApi  # noqa: E501


class TestRepositoriesApi(unittest.TestCase):
    """RepositoriesApi unit test stubs"""

    def setUp(self):
        self.api = RepositoriesApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_delete_v5_repos_owner_repo(self):
        """Test case for delete_v5_repos_owner_repo

        删除一个仓库  # noqa: E501
        """
        pass

    def test_delete_v5_repos_owner_repo_branches_branch_protection(self):
        """Test case for delete_v5_repos_owner_repo_branches_branch_protection

        取消保护分支的设置  # noqa: E501
        """
        pass

    def test_delete_v5_repos_owner_repo_collaborators_username(self):
        """Test case for delete_v5_repos_owner_repo_collaborators_username

        移除仓库成员  # noqa: E501
        """
        pass

    def test_delete_v5_repos_owner_repo_comments_id(self):
        """Test case for delete_v5_repos_owner_repo_comments_id

        删除Commit评论  # noqa: E501
        """
        pass

    def test_delete_v5_repos_owner_repo_contents_path(self):
        """Test case for delete_v5_repos_owner_repo_contents_path

        删除文件  # noqa: E501
        """
        pass

    def test_delete_v5_repos_owner_repo_keys_enable_id(self):
        """Test case for delete_v5_repos_owner_repo_keys_enable_id

        停用仓库公钥  # noqa: E501
        """
        pass

    def test_delete_v5_repos_owner_repo_keys_id(self):
        """Test case for delete_v5_repos_owner_repo_keys_id

        删除一个仓库公钥  # noqa: E501
        """
        pass

    def test_delete_v5_repos_owner_repo_releases_id(self):
        """Test case for delete_v5_repos_owner_repo_releases_id

        删除仓库Release  # noqa: E501
        """
        pass

    def test_get_v5_enterprises_enterprise_repos(self):
        """Test case for get_v5_enterprises_enterprise_repos

        获取企业的所有仓库  # noqa: E501
        """
        pass

    def test_get_v5_orgs_org_repos(self):
        """Test case for get_v5_orgs_org_repos

        获取一个组织的仓库  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo(self):
        """Test case for get_v5_repos_owner_repo

        获取用户的某个仓库  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_branches(self):
        """Test case for get_v5_repos_owner_repo_branches

        获取所有分支  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_branches_branch(self):
        """Test case for get_v5_repos_owner_repo_branches_branch

        获取单个分支  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_collaborators(self):
        """Test case for get_v5_repos_owner_repo_collaborators

        获取仓库的所有成员  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_collaborators_username(self):
        """Test case for get_v5_repos_owner_repo_collaborators_username

        判断用户是否为仓库成员  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_collaborators_username_permission(self):
        """Test case for get_v5_repos_owner_repo_collaborators_username_permission

        查看仓库成员的权限  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_comments(self):
        """Test case for get_v5_repos_owner_repo_comments

        获取仓库的Commit评论  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_comments_id(self):
        """Test case for get_v5_repos_owner_repo_comments_id

        获取仓库的某条Commit评论  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_commits(self):
        """Test case for get_v5_repos_owner_repo_commits

        仓库的所有提交  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_commits_ref_comments(self):
        """Test case for get_v5_repos_owner_repo_commits_ref_comments

        获取单个Commit的评论  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_commits_sha(self):
        """Test case for get_v5_repos_owner_repo_commits_sha

        仓库的某个提交  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_compare_base___head(self):
        """Test case for get_v5_repos_owner_repo_compare_base___head

        两个Commits之间对比的版本差异  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_contents_path(self):
        """Test case for get_v5_repos_owner_repo_contents_path

        获取仓库具体路径下的内容  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_contributors(self):
        """Test case for get_v5_repos_owner_repo_contributors

        获取仓库贡献者  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_forks(self):
        """Test case for get_v5_repos_owner_repo_forks

        查看仓库的Forks  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_keys(self):
        """Test case for get_v5_repos_owner_repo_keys

        获取仓库已部署的公钥  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_keys_available(self):
        """Test case for get_v5_repos_owner_repo_keys_available

        获取仓库可部署的公钥  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_keys_id(self):
        """Test case for get_v5_repos_owner_repo_keys_id

        获取仓库的单个公钥  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_pages(self):
        """Test case for get_v5_repos_owner_repo_pages

        获取Pages信息  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_readme(self):
        """Test case for get_v5_repos_owner_repo_readme

        获取仓库README  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_releases(self):
        """Test case for get_v5_repos_owner_repo_releases

        获取仓库的所有Releases  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_releases_id(self):
        """Test case for get_v5_repos_owner_repo_releases_id

        获取仓库的单个Releases  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_releases_latest(self):
        """Test case for get_v5_repos_owner_repo_releases_latest

        获取仓库的最后更新的Release  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_releases_tags_tag(self):
        """Test case for get_v5_repos_owner_repo_releases_tags_tag

        根据Tag名称获取仓库的Release  # noqa: E501
        """
        pass

    def test_get_v5_repos_owner_repo_tags(self):
        """Test case for get_v5_repos_owner_repo_tags

        列出仓库所有的tags  # noqa: E501
        """
        pass

    def test_get_v5_user_repos(self):
        """Test case for get_v5_user_repos

        列出授权用户的所有仓库  # noqa: E501
        """
        pass

    def test_get_v5_users_username_repos(self):
        """Test case for get_v5_users_username_repos

        获取某个用户的公开仓库  # noqa: E501
        """
        pass

    def test_patch_v5_repos_owner_repo(self):
        """Test case for patch_v5_repos_owner_repo

        更新仓库设置  # noqa: E501
        """
        pass

    def test_patch_v5_repos_owner_repo_comments_id(self):
        """Test case for patch_v5_repos_owner_repo_comments_id

        更新Commit评论  # noqa: E501
        """
        pass

    def test_patch_v5_repos_owner_repo_releases_id(self):
        """Test case for patch_v5_repos_owner_repo_releases_id

        更新仓库Release  # noqa: E501
        """
        pass

    def test_post_v5_enterprises_enterprise_repos(self):
        """Test case for post_v5_enterprises_enterprise_repos

        创建企业仓库  # noqa: E501
        """
        pass

    def test_post_v5_orgs_org_repos(self):
        """Test case for post_v5_orgs_org_repos

        创建组织仓库  # noqa: E501
        """
        pass

    def test_post_v5_repos_owner_repo_branches(self):
        """Test case for post_v5_repos_owner_repo_branches

        创建分支  # noqa: E501
        """
        pass

    def test_post_v5_repos_owner_repo_commits_sha_comments(self):
        """Test case for post_v5_repos_owner_repo_commits_sha_comments

        创建Commit评论  # noqa: E501
        """
        pass

    def test_post_v5_repos_owner_repo_contents_path(self):
        """Test case for post_v5_repos_owner_repo_contents_path

        新建文件  # noqa: E501
        """
        pass

    def test_post_v5_repos_owner_repo_forks(self):
        """Test case for post_v5_repos_owner_repo_forks

        Fork一个仓库  # noqa: E501
        """
        pass

    def test_post_v5_repos_owner_repo_keys(self):
        """Test case for post_v5_repos_owner_repo_keys

        为仓库添加公钥  # noqa: E501
        """
        pass

    def test_post_v5_repos_owner_repo_pages_builds(self):
        """Test case for post_v5_repos_owner_repo_pages_builds

        请求建立Pages  # noqa: E501
        """
        pass

    def test_post_v5_repos_owner_repo_releases(self):
        """Test case for post_v5_repos_owner_repo_releases

        创建仓库Release  # noqa: E501
        """
        pass

    def test_post_v5_repos_owner_repo_tags(self):
        """Test case for post_v5_repos_owner_repo_tags

        创建一个仓库的 Tag  # noqa: E501
        """
        pass

    def test_post_v5_user_repos(self):
        """Test case for post_v5_user_repos

        创建一个仓库  # noqa: E501
        """
        pass

    def test_put_v5_repos_owner_repo_branches_branch_protection(self):
        """Test case for put_v5_repos_owner_repo_branches_branch_protection

        设置分支保护  # noqa: E501
        """
        pass

    def test_put_v5_repos_owner_repo_clear(self):
        """Test case for put_v5_repos_owner_repo_clear

        清空一个仓库  # noqa: E501
        """
        pass

    def test_put_v5_repos_owner_repo_collaborators_username(self):
        """Test case for put_v5_repos_owner_repo_collaborators_username

        添加仓库成员  # noqa: E501
        """
        pass

    def test_put_v5_repos_owner_repo_contents_path(self):
        """Test case for put_v5_repos_owner_repo_contents_path

        更新文件  # noqa: E501
        """
        pass

    def test_put_v5_repos_owner_repo_keys_enable_id(self):
        """Test case for put_v5_repos_owner_repo_keys_enable_id

        启用仓库公钥  # noqa: E501
        """
        pass

    def test_put_v5_repos_owner_repo_reviewer(self):
        """Test case for put_v5_repos_owner_repo_reviewer

        修改代码审查设置  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
