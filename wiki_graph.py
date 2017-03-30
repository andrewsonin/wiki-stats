from array import array
from statistics import mean, stdev


class WikiGraph:
    def __init__(self, filename=None):
        self.titles = []
        self.edges = array('L', [])
        self.weights = array('L', [])
        self.offset = array('L', [0])
        self.redirects = array('l', [])
        if filename:
            self.load_from_file(filename)

    def load_from_file(self, file_name):
        print('Загружаю граф из файла:', file_name)
        file = open(file_name, 'r', encoding='utf8')
        vtx, edges = tuple(map(int, file.readline().split()))
        for cur_id in range(vtx):
            self.titles.append(file.readline().strip())
            weight, redirect, links = tuple(map(int, file.readline().split()))
            self.offset.append(self.offset[-1] + links)
            self.weights.append(weight)
            for i in range(links):
                self.edges.append(int(file.readline().strip()))
            if redirect:
                self.redirects.append(self.edges[-1])
            else:
                self.redirects.append(-1)
        print('Граф загружен')

    def check_redirection(self, _id):
        if self.redirects[_id] != -1:
            _id = self.redirects[_id]
        return _id

    def get_number_of_links_from(self, _id):
        # _id = self.check_redirection(_id)
        return self.offset[_id + 1] - self.offset[_id]

    def get_links_from(self, _id):
        # _id = self.check_redirection(_id)
        return self.edges[self.offset[_id]:self.offset[_id + 1]]

    def get_id(self, title):
        return self.titles.index(title)

    def get_number_of_pages(self):
        return len(self.redirects)

    def is_redirect(self, _id):
        if self.redirects[_id] == 1:
            return True
        return False

    def get_title(self, _id):
        return self.titles[_id]

    def get_page_size(self, _id):
        return self.weights[_id]

    def dfs(self, start, end, path=None, used=None):
        if used is None:
            used = set()
            print('Выполняю поиск в глубину')
        if path is None:
            path = []
        used.add(start)
        path.append(start)
        for neighbour in self.get_links_from(start):
            if neighbour == end:
                pth = [self.get_title(x) for x in path]
                print('Поиск в глубину закончен. Найден путь:\n' + ', '.join(map(str, pth)))
                return pth
            if neighbour not in used:
                tmp = self.dfs(neighbour, end, path, used)
                if tmp:
                    return tmp
        path.pop()
        return None

    def bfs(self, start, end):
        print('Выполняю поиск в ширину')
        start, end = self.check_id_is_int(start, end)
        paths = dict()
        paths[start] = [start]
        queue = [start]
        while queue:
            cur = queue.pop(0)
            for neighbour in self.get_links_from(cur):
                if neighbour == end:
                    pth = [self.get_title(x) for x in paths[cur] + [end]]
                    print('Поиск в ширину закончен. Найден путь:\n' + ', '.join(map(str, pth)))
                    return pth
                if neighbour not in paths:
                    paths[neighbour] = paths[cur] + [neighbour]
                    queue.append(neighbour)
        print('Поиск в ширину закончен. Путь не найден')
        return None

    def check_id_is_int(self, *args):
        args = list(args)
        for i in range(len(args)):
            tmp = args[i]
            if type(tmp) == str:
                args[i] = self.get_id(tmp)
            elif not type(tmp) == int:
                raise TypeError
        return args

    def stat_report(self, report=True):
        graph_len = self.get_number_of_pages()
        redirect_articles = graph_len - self.redirects.count(-1)
        links = array('L', [self.get_number_of_links_from(_id) for _id in range(graph_len)])
        min_num = min(links)
        num_min_num = links.count(min_num)
        max_num = max(links)
        num_max_num = links.count(max_num)
        max_links_article = self.get_title(links.index(max_num))
        average_num = mean(links)
        st_dev_num = stdev(links)

        links = array('L', [0] * graph_len)
        for i in range(graph_len):
            links[self.edges[i]] += 1
        min_count_of_links = min(links)
        pages_with_no_out_links = links.count(min_count_of_links)
        max_count_of_links = max(links)
        pages_with_max_out_links = links.count(max_count_of_links)
        page_with_max_out_links = self.get_title(links.index(max_count_of_links))
        average_out = mean(links)
        st_dev_out = stdev(links)

        links = array('L', [0] * graph_len)
        for i in range(graph_len):
            if self.redirects[i] != -1:
                links[self.redirects[i]] += 1
        min_redirects = min(links)
        pages_with_min_redirects = links.count(min_redirects)
        max_redirects = max(links)
        pages_with_max_redirects = links.count(max_redirects)
        page_with_max_redirects = self.get_title(links.index(max_redirects))
        average_redirect = mean(links)
        st_dev_redirect = stdev(links)

        if report:
            print('Количество статей с перенаправлением:', redirect_articles,
                  '(' + str(round(100 * redirect_articles / graph_len, 2)) + '%)')
            print('Минимальное количество ссылок из статьи:', min_num)
            print('Количество статей с минимальным количеством ссылок:', num_min_num)
            print('Максимальное количество ссылок из статьи:', max_num)
            print('Количество статей с максимальным количеством ссылок:', num_max_num)
            print('Статья с наибольшим количеством ссылок:', max_links_article)
            print('Среднее количество ссылок:', round(average_num, 2), '(ср. откл.', str(round(st_dev_num, 2)) + ')')

            print('Минимальное количество внешних ссылок на статью:', min_count_of_links)
            print('Количество статей с минимальным количеством внешних ссылок:', pages_with_no_out_links)
            print('Максимальное количество внешних ссылок на статью:', max_count_of_links)
            print('Количество статей с максимальным количеством внешних ссылок:', pages_with_max_out_links)
            print('Статья с наибольшим количеством внешних ссылок:', page_with_max_out_links)
            print('Среднее количество внешних ссылок на статью:', round(
                average_out, 2), '(ср. откл.', str(round(st_dev_out, 2)) + ')')

            print('Минимальное количество перенаправлений на статью:', min_redirects)
            print('Количество статей с минимальным количеством внешних перенаправлений:', pages_with_min_redirects)
            print('Максимальное количество перенаправлений на статью:', max_redirects)
            print('Количество статей с максимальным количеством внешних перенаправлений:', pages_with_max_redirects)
            print('Статья с наибольшим количеством внешних перенаправлений:', page_with_max_redirects)
            print('Среднее количество внешних перенаправлений на статью:', round(average_redirect, 2),
                  '(ср. откл.', str(round(st_dev_redirect, 2)) + ')')
