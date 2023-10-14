<h1 align="center">NotionX</h1>

<div align="center">

[![codecov](https://codecov.io/gh/JezaChen/mumu-notion/branch/master/graph/badge.svg?token=QKE5Z5JS04)](https://codecov.io/gh/JezaChen/mumu-notion)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/notionx?style=flat-square)
![GitHub](https://img.shields.io/github/license/jezachen/mumu-notion)

</div>

`NotionX`，一个简单易用的Notion客户端。

## 已经实现的功能

- 支持最新的Notion API：代码使用了`2022-06-28`的Notion版本。
- 完整的API覆盖：已封装Notion API官方文档的所有方法(https://developers.notion.com/reference/)。
- 简单的请求校验：在本地能校验用户的请求是否合法，目前支持最外层的参数的字段校验（如用户提供的参数是否完整、是否存在不包含于API文档中的参数），而值校验以及嵌套的参数校验还在开发中。
- 同步的Client请求，使用httpx进行同步的HTTP请求，异步请求功能正在开发中。
- 完整的代码示例，覆盖了100%的客户端方法，以及90%以上的代码。
- 完整的测试，覆盖了98%+的客户端代码。

## 安装需求

- Python >= 3.7
- httpx >= 0.23.0

## 安装

使用`pip`安装即可：

```shell
pip install notionx
```

## 用法

使用NotionX前，需要创建 Integration Token, 并分享至少一个页面给该Integration。

- 创建方式：https://www.notion.so/my-integrations/
- Notion关于创建和分享页面至Integration的官方教程：https://developers.notion.com/docs/getting-started

### Client的初始化

通过传入包含`auth_token`（上述Integration的Token，以`secret_`开头）的字典（**字典参数风格**），以实现Notion Client的初始化：

```Python
from notionx import Client

client = Client({
    "auth_token": "your_integration_token"
})
```

还有另一个初始化的方式，以**关键字参数风格**传入：

```Python
from notionx import Client

client = Client(
    auth_token="your_integration_token"
)
```

字典参数风格和关键字参数风格还适用于客户端的各个方法，我们将在后面给出两种风格的调用方式。

> 💡注意！！
>
> 为了避免Integration Token的泄漏，我们不建议将token明文硬编码在代码里。最好将其写入环境变量中，再通过以下方式初始化：
> ```Python
> import os
> from notionx import Client
>
> token = os.getenv("NOTION_AUTH_TOKEN")
> client = Client(
>     auth_token=token
> )
> ```

除`auth_token`之外，Client还有多个**可选的**初始化参数，其参数名和含义如下表所示：

|       参数名        | 类型    |              默认值              |                描述                 |
|:----------------:|-------|:-----------------------------:|:---------------------------------:|
|   `auth_token`   | `str` |           **没有默认值**           |         Integration Token         |
| `notion_version` | `str` |        `"2022-06-28"`         |            Notion的版本号             |
|    `base_url`    | `str` | `"https://api.notion.com/v1"` |           发送API请求的根URL            |
|   `timeout_ms`   | `int` |           `90_000`            | 在发出`RequestTimeoutError`之前要等待的毫秒数 |

### How-tos

详细内容见[Wiki 页面](https://github.com/JezaChen/mumu-notion/wiki/How-tos-(%E4%B8%AD%E6%96%87%E7%89%88))。

## 代码示例

我们提供了代码示例，其覆盖了客户端的所有方法，且数据来源于Notion的官方文档。

另见：https://github.com/JezaChen/mumu-notion/tree/master/examples/official_guides
