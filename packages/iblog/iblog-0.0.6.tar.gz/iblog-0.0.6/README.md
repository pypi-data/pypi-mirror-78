# blog
blog
## github issues
可以用issues来写blog
优点：
- 支持回复
- 支持tag
- 可以计划
- 支持订阅
- 全文检索

缺点：
- 任何人都可以新建issue（有好处也有不好的）

> 感觉很棒

## 设计
- a 提供api供其它服务调用的方式来操作issue
- b 提供MQ消费者的方式来操作issue
- c 提供定时任务来操作issue

### 思考
#### 直接创建一个网站首页

获取api显示
> https://api.github.com/repos/lzh2nix/articles/issues?page=2
> 在上面的api header中有以下信息
> link: <https://api.github.com/repositories/112858035/issues?page=1>; rel="prev", <https://api.github.com/repositories/112858035/issues?page=3>; rel="next", <https://api.github.com/repositories/112858035/issues?page=3>; rel="last", <https://api.github.com/repositories/112858035/issues?page=1>; rel="first"

> https://developer.github.com/v3/issues/

https://github.com/josegonzalez/python-github-backup

https://github.com/IQAndreas/github-issues-import

https://github.com/devspace/awesome-github-templates

[ABAP开发的Github issue备份工具](https://zhuanlan.zhihu.com/p/206986949)

> gitee 也有对应的api：https://gitee.com/api/v5/swagger#/getV5ReposOwnerRepoIssuesComments

#### 开发一个同步工具
利用issues的api

评论可以单向同步到自己的blog系统



### 提高 API 访问次数的配额
默认情况下你是用匿名权限访问 github 接口的， github 的访问限制是一个小时最多 60 次请求，这显然是不够的，如何提高限制呢？

1. 到个人设置下的 Personal access tokens 页（https://github.com/settings/tokens ），如下图，点击右上角的 Generate new token



2. 填写名称，只勾选 public_repo,然后保存，github 会生成一个可访问你公开项目的 access_token，将它填入到配置文件的 access_token 的值中，并取消注释。 

3. 打开 app.js,取消掉第 17 行和 88 行的注释，保存后重新上传即可

 data:{
     // access_token:_config['access_token']
 },


```
python setup.py check
python setup.py sdist bdist_wheel
python setup.py install
twine upload dist/*

python -m iblog -h
or
iblog -h
```