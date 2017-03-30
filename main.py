from wiki_graph import WikiGraph

wk = WikiGraph('wiki.txt')
wk.bfs('Московский_физико-технический_институт', 'Python')
wk.stat_report()
