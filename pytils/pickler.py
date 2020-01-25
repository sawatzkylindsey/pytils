
import logging
import os
import pickle
import queue
import random
import threading

from pytils import check


EXTENSION = ".pickle"
LENGTH_FILE = "length.txt"
# 2147483648 - 1
MAX_BYTES = (2**31) - 1
# 100 MB = 100 * 1024 KB
TARGET_FILE_SIZE = 100 * 1024 * 1024
STREAM_TARGET_FILE_SIZE = 10 * 1024 * 1024
STREAM_MAX_BATCH = 2000


def save(data, dir_path, converter=None):
    os.makedirs(dir_path, exist_ok=True)

    if isinstance(data, queue.Queue):
        thread = threading.Thread(target=_save_stream, args=[data, dir_path, converter])
        # Non-daemon threads will keep the program running until they finish (as per documentation).
        thread.daemon = False
        thread.start()
    else:
        _save(data, dir_path, converter)


def _save_stream(data, dir_path, converter):
    check.check_instance(data, queue.Queue)
    batch = []
    batch_size = None
    i = 0
    try_size = 10
    total_size = 0

    while True:
        item = data.get()

        if item is not None:
            batch += [item]

            # If we're still building out the sample.
            if batch_size is None:
                # Only try to discover the batch_size every so often.
                if len(batch) % try_size == 0:
                    average = _average_size(batch, converter)
                    sample_size = average * len(batch)

                    if sample_size > STREAM_TARGET_FILE_SIZE:
                        batch_size = max(1, int(STREAM_TARGET_FILE_SIZE / average))

                if len(batch) > 2 * try_size:
                    # Notice we don't need to worry about this growing too large, because the next check upper bounds the batch size.
                    try_size = try_size * 2

                if batch_size is None and len(batch) == STREAM_MAX_BATCH:
                    # The batch is plenty large enough - just set it here.
                    batch_size = STREAM_MAX_BATCH
            else:
                # The batch_size has been determined.
                while len(batch) > batch_size:
                    bytes_out = pickle.dumps(_convert(converter, batch[:batch_size]))
                    _write_bytes(bytes_out, dir_path, i)
                    i += 1
                    batch = batch[batch_size:]
                    total_size += batch_size
        else:
            # The data stream is complete - flush the remaining data.
            if len(batch) > 0:
                bytes_out = pickle.dumps(_convert(converter, batch))
                _write_bytes(bytes_out, dir_path, i)
                total_size += len(batch)

            with open(os.path.join(dir_path, LENGTH_FILE), "w") as fh:
                fh.write("%d" % total_size)

            logging.debug("Completed pickling stream for '%s' (%d items)." % (dir_path, total_size))
            break


def _save(data, dir_path, converter):
    check.check_list(data)

    if len(data) > 0:
        sample_size = max(1, int(0.1 * len(data)))
        sample_indices = set()

        while len(sample_indices) < sample_size:
            sample_indices.add(random.randint(0, len(data) - 1))

        sample = [data[index] for index in sample_indices]
        average = _average_size(sample, converter)
        batch_size = max(1, int(TARGET_FILE_SIZE / average))

        for i, offset in enumerate(range(0, len(data), batch_size)):
            bytes_out = pickle.dumps(_convert(converter, data[offset:offset + batch_size]))
            _write_bytes(bytes_out, dir_path, i)
    else:
        _write_bytes(pickle.dumps([]), dir_path, 0)

    with open(os.path.join(dir_path, LENGTH_FILE), "w") as fh:
        fh.write("%d" % len(data))

    logging.debug("Completed pickling for '%s' (%d items)." % (dir_path, len(data)))


def _average_size(sample, converter):
    batch = [i for i in sample]
    average = None

    while average is None:
        try:
            batch_size = len(pickle.dumps(_convert(converter, batch)))
            average = batch_size / float(len(batch))
        except MemoryError as e:
            batch = batch[:int(len(batch) / 2.0)]

    return average


def _convert(converter, batch):
    return batch if converter is None else [converter(b) for b in batch]


def _write_bytes(bytes_out, dir_path, index):
    write_path = os.path.join(dir_path, str(index) + EXTENSION)

    # TODO
    #if os.path.exists(write_path):
    #    raise ValueError("cannot overwrite existing file: %s" % write_path)

    with open(write_path, "wb") as fh:
        while len(bytes_out) > 0:
            fh.write(bytes_out[:MAX_BYTES])
            bytes_out = bytes_out[MAX_BYTES:]


def length(dir_path, allow_not_found=False):
    try:
        with open(os.path.join(dir_path, LENGTH_FILE), "r") as fh:
            return int(fh.readline())
    except FileNotFoundError as e:
        if allow_not_found:
            return None
        else:
            raise e


def load(dir_path, allow_not_found=False, converter=None):
    try:
        sub_files = os.listdir(dir_path)
    except FileNotFoundError as e:
        if allow_not_found:
            return None
        else:
            raise e

    filtered_sub_files = filter(lambda item: item.endswith(EXTENSION), sub_files)

    for sub_file in sorted(filtered_sub_files, key=lambda item: int(item[:item.index(EXTENSION)])):
        file_path = os.path.join(dir_path, sub_file)
        size = os.path.getsize(file_path)

        with open(file_path, "rb") as fh:
            bytes_in = bytearray(0)

            for i in range(0, size, MAX_BYTES):
                bytes_in += fh.read(MAX_BYTES)

            for item in pickle.loads(bytes_in):
                if converter is None:
                    yield item
                else:
                    result = converter(item)

                    if result is not None:
                        yield result

