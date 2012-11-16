```python
from HN import news

x = news.HackerNews()
for item in x.titles:
	print repr(item.title) + '\t' + item.points
```