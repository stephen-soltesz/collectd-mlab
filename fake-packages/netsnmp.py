"""A fake minimal version of netsnmp module."""


class Session(object):

    def __init__(self, *args, **kwargs):  # pragma: no cover
        pass

    def get(self, *args, **kwargs):  # pragma: no cover
        pass

    def walk(self, *args, **kwargs):  # pragma: no cover
        pass


class Varbind(object):

    def __init__(self, tag, val=None, **kwargs):
        self.tag = tag
        self.val = val
        self.iid = None


class VarList(list):

    def __init__(self, *args, **kwargs):
        super(VarList, self).__init__(args)
