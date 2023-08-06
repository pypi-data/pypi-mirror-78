from gitee import core
from gitee.gitee_object import GiteeObject, Response


class Issue(GiteeObject):
    # 仓库的所有Issues
    def repos_owner_repo_issues_url(self, owner, repo):
        return '/repos/{owner}/{repo}/issues'.format(owner=owner, repo=repo)

    # 仓库的某个Issue
    def repos_owner_repo_issues_one_url(self, owner, repo, number):
        return self.repos_owner_repo_issues_url(owner=owner, repo=repo) + '/' + number

    # 创建Issue
    def repos_owner_issues_url(self, owner):
        return '/repos/{owner}/issues'.format(owner=owner)

    # 更新Issue
    def repos_owner_issues_update_url(self, owner, number):
        return self.repos_owner_issues_url(owner=owner) + '/' + number

    def list(self, owner, repo, state='open', sort='created', direction='desc', page=1, per_page=0,
             **kwargs) -> Response:
        """getV5ReposOwnerRepoIssues

        :calls: `GET /repos/{owner}/{repo}/issues`
        :param owner: 仓库所属空间地址(企业、组织或个人的地址path)
        :type owner: str
        :param repo: 仓库路径(path)
        :type repo: str
        :param state: 仓库路径(path)
        :type state: str
        :param sort: 排序依据: 创建时间(created)，更新时间(updated)。默认: created
        :type sort: str
        :param direction: 排序方式: 升序(asc)，降序(desc)。默认: desc
        :type direction: str
        :param page: 当前的页码
        :type page: int
        :param per_page: 每页的数量，最大为 100,默认20
        :type per_page: int

        :param \*\*kwargs: getV5ReposOwnerRepoIssues

        :return: :class:`Response <Response>` object
        :rtype: Response
        """
        if per_page <= 0:
            per_page = self.per_page
        args = core.params(locals())
        return self.do_get(self.repos_owner_repo_issues_url(owner, repo), args)

    def get(self, owner, repo, number):
        """getV5ReposOwnerRepoIssuesNumber

        :calls: `GET /repos/{owner}/{repo}/issues/{number}`
        :param owner: 仓库所属空间地址(企业、组织或个人的地址path)
        :type owner: str
        :param repo: 仓库路径(path)
        :type repo: str
        :param number: Issue 编号(区分大小写，无需添加 # 号)
        :type number: str
        :return: :class:`Response <Response>` object
        :rtype: Response
        """
        return self.do_get(self.repos_owner_repo_issues_one_url(owner, repo, number))

    def create(self, owner, repo, title, **kwargs):
        """postV5ReposOwnerIssues

        :calls: `POST /repos/{owner}/issues`
        :param owner: 仓库所属空间地址(企业、组织或个人的地址path)
        :type owner: str
        :param repo: 仓库路径(path)
        :type repo: str
        :param title: Issue标题
        :type title: str
        :return: :class:`Response <Response>` object
        :rtype: Response
        """
        args = core.params(locals())
        return self.do_post(self.repos_owner_issues_url(owner), args)

    def update(self, owner, repo, number, **kwargs):
        """patchV5ReposOwnerIssuesNumber

        :calls: `POST /repos/{owner}/issues/{number}`
        :param owner: 仓库所属空间地址(企业、组织或个人的地址path)
        :type owner: str
        :param repo: 仓库路径(path)
        :type repo: str
        :param number: Issue 编号(区分大小写，无需添加 # 号)
        :type number: str
        :return: :class:`Response <Response>` object
        :rtype: Response
        """
        args = core.params(locals())
        return self.do_patch(self.repos_owner_issues_update_url(owner, number), args)
