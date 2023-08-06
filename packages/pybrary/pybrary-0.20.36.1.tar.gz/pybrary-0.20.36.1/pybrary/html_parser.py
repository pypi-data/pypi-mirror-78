from html.parser import HTMLParser


class Node:
    def __init__(self, parent, attrs):
        self.parent = parent
        self.relative = 0
        self.attrs = attrs or dict()
        self.data = None
        self.nodes = list()
        self.open = True

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

    @property
    def level(self):
        return self.parent.level+1 if self.parent else 0

    @property
    def ancestors(self):
        if not self.parent: return []
        return [self.parent] + self.parent.ancestors

    @property
    def lineage(self):
        return ' '.join([self.tag or '']+[a.tag or '' for a in self.ancestors])

    def ancestor(self, tag):
        for a in self.ancestors:
            if a.tag==tag: return a

    def close(self, parent=None):
        parent = parent or self
        for node in self():
            if node.open:
                node.parent = parent
                node.close(parent)
        self.open = False

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
    ignore = 'hr br u b'.split()

    def __init__(self, src, **kw):
        super().__init__(**kw)
        self.root = self.current = Node(None, None)
        self.feed(src)
        self.close()

    def handle_starttag(self, tag, attrs):
        if tag in HTML.ignore: return

        kw = dict(attrs)
        kw['tag'] = tag.lower()
        child = Node(self.current, kw)
        if self.current:
            self.current.nodes.append(child)
        self.current = child

    def handle_data(self, data):
        if self.current and data.strip():
            self.current.data = data

    def handle_endtag(self, tag):
        if tag in HTML.ignore: return
        if self.current:
            if self.current.tag == tag:
                self.current.close()
                self.current = self.current.parent
            else:
                self.current = self.current.ancestor(tag)
                if self.current:
                    self.current.close()

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
