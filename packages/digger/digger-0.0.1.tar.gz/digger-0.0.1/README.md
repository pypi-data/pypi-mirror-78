# Digger

## 安装

```shell script
pip install digger
```

## 使用

```python
from digger import Digger

digger = Digger()
digger.specify_words(['北京', '中国梦'])
digger(['http://example.com/1', 'http://example.com/2'], merge_result=False)
```

## Webserver

```shell script
# bash
digger webserver
```