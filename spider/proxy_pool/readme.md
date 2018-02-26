简单代理池，但是免费代理能用的比较少，能用速度快的非常少。
1.api.py用于将redis中存储的代理抛出在端口。\
2.crawler.py用于爬取网站免费代理。\
3.db主要是redis相关操作。\
4.getter主要是启动crawler.py中所有爬虫。\
5.tester用于测试代理是否可用。\
5.scheduler是核心调度器，用于启动生产器，测试器，接口。
