from gitee.consts import *
from gitee.issue import Issue


class Gitee(object):
    def __init__(
            self,
            access_token=None,
            base_url=DEFAULT_BASE_URL,
            per_page=DEFAULT_PER_PAGE,
    ):
        self.access_token = access_token
        self.base_url = base_url
        self.per_page = per_page

    def get_issues(self):
        return Issue(access_token=self.access_token, base_url=self.base_url, per_page=self.per_page)
