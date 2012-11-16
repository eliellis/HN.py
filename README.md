```python
from HN import HN as news

x = news.HackerNews()
for item in x.titles:
	print repr(item.title) + '\t' + item.points
```