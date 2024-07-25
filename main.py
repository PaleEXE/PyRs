import time
import collections

import plib
from icecream import ic

with open('Modern Talking.txt', 'r') as f:
    text = f.read()


def pref(fun, *args):
    start = time.perf_counter()
    fun(*args)
    end = time.perf_counter()
    return end - start


def py_counter(words):
    rizz = {}
    for word in words:
        rizz[word] = rizz.get(word, 0) + 1
    return rizz


lp = []
lc = []

for i in range(10):
    lc.append(pref(collections.Counter, text.split()))
    lp.append(pref(plib.par_counter, text))

tc = ic(sum(lc)/len(lc))
tp = ic(sum(lp)/len(lp))
ic(tc / tp)
plib.show("Majd")



