from anchonkiboy import top,top_maxpow
from sys import argv as args
try:
    if args[1] in {"f","fast","-f"}:
        top(20)
    else:
        top_maxpow(20)
except:
    top_maxpow(20)
