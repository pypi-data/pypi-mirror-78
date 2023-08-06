# pygitee

#### 介绍
pygitee 是封装了gitee的OpenAPI的python库.

#### 安装教程
pip install pygitee

#### 使用说明

```python
from gitee import Gitee
g = Gitee()
# g = Gitee(access_token='xxx')
print(g.get_issues().list('kingreatwill', 'kingreatwill'))
```