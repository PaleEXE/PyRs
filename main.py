import collections
import time

import pandas as pd
import matplotlib.pyplot as plt
import plib
from icecream import ic

with open('Modern Talking.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# text += text


def pref0(fun, *args):
    start = time.perf_counter()
    fun(*args)
    end = time.perf_counter()
    return end - start


def pref1(fun, *args):
    start = time.perf_counter()
    fun(args[0].split())
    end = time.perf_counter()
    return end - start


def py_counter(words):
    rizz = {}
    for word in words:
        rizz[word] = rizz.get(word, 0) + 1
    return rizz


list_threads = []
list_par = []
list_rust = []
list_collection = []
for i in range(1, 60):
    txt = text[:50_000 * i]
    list_threads.append(pref0(plib.thread_counter, txt))
    list_par.append(pref0(plib.par_counter, txt))
    list_rust.append(pref0(plib.counter, txt))
    list_collection.append(pref1(collections.Counter, txt))


plt.plot(list_collection)
plt.plot(list_rust)
plt.plot(list_par)
plt.plot(list_threads)
langs = ['Collections', 'Rust', 'Rayon', 'Rust Threads']
plt.legend(langs)
plt.show()
#
# d = dict(zip(langs, [list_collection, list_rust, list_par, list_threads]))
# df = pd.DataFrame(d)
#
# print("Mean\n", df.mean(), sep="")
# print("STD\n", df.std(), sep="")

# ic(plib.thread_counter(text)['jesus'])
# ic(plib.par_counter(text)['jesus'])
# ic(plib.counter(text)['jesus'])
# ic(collections.Counter(text.split())['jesus'])
x = plib.thread_counter(text)
# for k, v in collections.Counter(text.split()).items():
#     if (i := x.get(k, 0)) != v:
#         ic(k, v, i)



