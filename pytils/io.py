
import bz2
import gzip
import queue
import sys


def stdin_generator():
    for line in sys.stdin:
        yield line


def file_generator(input_file):
    def opener():
        if input_file.endswith("bz2"):
            return bz2.BZ2File(input_file)
        else:
            try:
                return open(input_file, "r", encoding="utf-8")
            except UnicodeDecodeError as e:
                return gzip.open(input_file, "rt", encoding="utf-8")

    with opener() as fh:
        for line in fh.readlines():
            if isinstance(line, bytes):
                line = line.decode("utf-8")

            yield line


class Streamer:
    def __init__(self, processor):
        self.processor = processor
        self.output = queue.Queue

    def _process_generator(self, generator):
        for item in generator:
            self.processor(item)

    def from_generator(self, generator):
        thread = threading.Thread(target=self._process_generator, args=[data, dir_path, converter])
        thread.daemon = False
        thread.start()

        while True:
            item = self.output.get()

            if item is not None:
                yield item

