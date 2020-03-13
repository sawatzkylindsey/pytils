
import json
import inspect

print("# COPIED VIA INSPECT")
print("".join(inspect.getsourcelines(json.encoder._make_iterencode)[0]))

