import attr

@attr.s
class SuccessMeasurer(object):
    @property
    def testing(self):
        return 'this connected'
