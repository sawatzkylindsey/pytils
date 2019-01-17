

def dict_as_str(d, use_key=True, reverse=False):
    out = []

    for item in sorted(d.items(), key=lambda item: item[0] if use_key else item[1], reverse=reverse):
        out.append("%s: %s" % (item[0], item[1]))

    return "{%s}" % ", ".join(out)


def flat_map(sequence):
    return [i for item in sequence for i in item]

