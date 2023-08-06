from dataclasses import dataclass


@dataclass
class Issue(object):
    id: int  # issue id
    number: str  # issue number
    html_url: str  # issue url
    state: str  # issue state  open（开启的）, progressing(进行中), closed（关闭的）, rejected（拒绝的）
    title: str  # issue title
    body: str  # issue body
    labels: str  # 用逗号分开的标签，名称要求长度在 2-20 之间且非特殊字符。如: bug,performance


def github_01():
    from github import Github
    g = Github("access_token")
    for repo in g.get_user().get_repos():
        print(repo.name)

def gitee_01():
    import gitee
    api_instance = gitee.IssuesApi(gitee.ApiClient())
    print(api_instance.get_v5_repos_owner_repo_issues("kingreatwill", "kingreatwill"))