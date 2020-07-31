
import random


def randomize(list_or_stream, buffer_size=100):
    item_buffer = {}

    for item in list_or_stream:
        if len(item_buffer) < buffer_size:
            item_buffer[len(item_buffer)] = item
        else:
            choice = random.randint(0, len(item_buffer) - 1)
            yield item_buffer[choice]
            item_buffer[choice] = item

    while len(item_buffer) > 0:
        choice = random.randint(0, len(item_buffer) - 1)
        yield item_buffer[choice]
        last = len(item_buffer) - 1

        if choice == last:
            del item_buffer[choice]
        else:
            item_buffer[choice] = item_buffer[last]
            del item_buffer[last]


