from html.parser import HTMLParser


class Node:
    def __init__(self, parent, attrs):
        self.parent = parent
        self.level = parent.level+1 if parent else 0
        self.relative = 0
        self.attrs = attrs or dict()
        self.data = None
        self.nodes = list()

    def __getattr__(self, val):
        return self.attrs.get(val)

    def __iter__(self):
        yield from self.nodes

    def walk(self):
        for node in self:
            yield node
            yield from node.walk()

    def walk_relative(self):
        relative = self.level+1
        for node in self:
            node.relative = relative
            yield node
            node.relative = 0
            for child in node.walk():
                child.relative = relative
                yield child
                child.relative = 0

    @staticmethod
    def select(node, **kw):
        for k in ('id', 'class'):
            k_ = f'{k}_'
            if k_ in kw:
                kw[k] = kw.pop(k_)
        tag = kw.get('tag')
        if tag:
            kw['tag'] = tag.lower()
        items = kw.items()
        get = node.attrs.get
        return all(get(k)==v for k, v in items)

    def __call__(self, select=None, **kw):
        if kw:
            select = select or self.select
            for node in self.walk():
                if select(node, **kw):
                    yield node
        else:
            yield from self.walk()

    def __str__(self):
        indent = '    '*(self.level-self.relative)
        attrs = ', '.join(f'{k}={v}' for k, v in self.attrs.items() if k!='tag')
        return f'{indent}{self.tag} {attrs}'

    def dump(self, nodes=True, datas=True):
        for node in self.walk_relative():
            if nodes:
                print(node)
            if datas and node.data:
                print(node.data)


class HTML(HTMLParser):
    def __init__(self, src, **kw):
        super().__init__(**kw)
        self.root = self.current = Node(None, None)
        self.feed(src)
        self.close()

    def handle_starttag(self, tag, attrs):
        if self.current.tag in ('img', 'link', 'meta'):
            # missing end tag
            self.handle_endtag(self.current.tag)

        kw = dict(attrs)
        kw['tag'] = tag.lower()
        child = Node(self.current, kw)
        self.current.nodes.append(child)
        self.current = child

    def handle_data(self, data):
        if self.current and data.strip():
            self.current.data = data

    def handle_endtag(self, tag):
        if self.current.tag!=tag:
            # missing end tag
            self.handle_endtag(self.current.tag)
        self.current = self.current.parent

    def __iter__(self):
        yield from self.root

    def __call__(self, **kw):
        yield from self.root(**kw)

    @property
    def head(self):
        return next(self(tag='head'))

    @property
    def body(self):
        return next(self(tag='body'))
