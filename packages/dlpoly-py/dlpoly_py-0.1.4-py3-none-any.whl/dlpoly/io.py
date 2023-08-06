
class Output():
    __version__ = "0"

    def __init__(self, source=None):
        if source is not None:
            self.source = source
            self.read(source)

    def read(self, source="OUTPUT"):
        """ Read an OUTPUT file into memory """
        with open(source, 'r') as f:
            a = f.readline().split()[0]

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        output = Output(sys.argv[1])
    else:
        output = Output()
