import requests, json
from lxml import html

class HackerNews(object):
    
    def __init__(self):
        self.__session = requests.session()
        self.reload()
        
    def reload(self):
        getfeed = self.__session.get("http://news.ycombinator.com/")
        dom_obj = html.fromstring(getfeed.text)
        self.titles = self.__buildlist(dom_obj)
        
    def __buildlist(self,domobj):
        titles, ranks, urls = self.__titles(domobj.cssselect("td[class=title]"))
        scores, authors, comments = self.__subtext(domobj.cssselect("tr>td[class=subtext]"))
        fulllist = []
        for i in range(0,len(ranks)):
            pass
            #title, points, author, comment_num, rank
            titleitem = Title(title=titles[i],points=scores[i],author=authors[i],comment_num=comments[i],rank=ranks[i],url=urls[i])
            fulllist.append(titleitem)
            
        return fulllist
        
    def __subtext(self,domobj):
        scores = []
        authors = []
        comments = []
        for i in domobj:
            scores.append(i.cssselect("span")[0].text_content().replace('points', '').strip())
            authors.append(i.cssselect("a")[0].text_content().strip())
            comments.append(i.cssselect("a")[1].text_content().replace('comments','').strip())
            
        return scores, authors, comments
        
    
    def __titles(self,domobj):
        titles = []
        urls = []
        ranks = []
        num = True
        for text in domobj:
            if num == True:
                ranks.append(text.text_content()[:-1])
                num = False
            elif num == False:
                titles.append(text.cssselect('a')[0].text_content())
                urls.append(text.cssselect('a')[0].get('href'))
                num = True
        ranks = ranks[:-1] #get rid of the 'More' item
        return titles,ranks,urls
        
class Title(object):
    
    def __init__(self, title, points, author, comment_num, rank, url):
        self.title = title
        self.url = url
        self.points = points
        self.author = author
        self.comment_num = comment_num
        self.rank = rank
        
    def dump_json(self):
        return json.dumps({'title': self.title, 'url':self.url, 'points': self.points, 'author':self.author, 'comments_total': self.comment_num, 'rank': self.rank})
        