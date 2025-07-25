import collections
import time

import pandas as pd
import matplotlib.pyplot as plt
import plib
from icecream import ic

with open("Modern Talking.txt", "r", encoding="utf-8") as f:
    text = f.read()

text += text


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


list_threads = []
list_par = []
list_rust = []
list_collection = []

# Collect timings
for i in range(1, 31):
    list_threads.append(pref0(plib.thread_counter, text))
    list_par.append(pref0(plib.par_counter, text))
    list_rust.append(pref0(plib.counter, text))
    list_collection.append(pref1(collections.Counter, text))

# Prepare benchmark data
langs = ["Python Collections", "Rust Single-threaded", "Rust Rayon", "Rust Threads"]
d = dict(zip(langs, [list_collection, list_rust, list_par, list_threads]))
df = pd.DataFrame(d)

# X-axis (input size)
x = [i for i in range(1, 31)]  # in 'k chars'

# Create main plot with subplots
fig, axs = plt.subplots(1, 2, figsize=(16, 6), gridspec_kw={"width_ratios": [3, 1]})

# --- Left: Line Plot for Performance ---
axs[0].plot(
    x, list_collection, label="Python Collections.Counter", linestyle="--", marker="o"
)
axs[0].plot(x, list_rust, label="Rust Single-threaded", linestyle="--", marker="o")
axs[0].plot(x, list_par, label="Rust Rayon (Parallel)", linestyle="--", marker="o")
axs[0].plot(x, list_threads, label="Rust Manual Threads", linestyle="--", marker="o")

axs[0].set_title("Performance Over Increasing Input Size")
axs[0].set_xlabel("Input Size (Thousands of Characters)")
axs[0].set_ylabel("Execution Time (seconds)")
axs[0].legend()
axs[0].grid(True)

# --- Right: Bar Plot for Mean and Std ---
means = df.mean()
stds = df.std()

axs[1].barh(
    langs, means, xerr=stds, color=["gray", "orange", "green", "blue"], alpha=0.7
)
axs[1].set_title("Mean Execution Time ± Std")
axs[1].set_xlabel("Time (seconds)")
axs[1].invert_yaxis()  # To match legend order

# Layout and save
fig.suptitle("Word Counter Performance Benchmark", fontsize=14)
plt.figtext(
    0.5,
    -0.05,
    "Left: Execution time vs. input size. Right: Average performance with standard deviation error bars.\n"
    "Measured: Python collections.Counter, Rust (single-threaded), Rayon (parallel), and manual threads.",
    wrap=True,
    horizontalalignment="center",
    fontsize=10,
)

plt.tight_layout()
plt.subplots_adjust(top=0.85, bottom=0.2)
plt.savefig("word_counter_benchmark_with_stats.png", dpi=300)
plt.show()

# ic(plib.thread_counter(text)['jesus'])
# ic(plib.par_counter(text)['jesus'])
# ic(plib.counter(text)['jesus'])
# ic(collections.Counter(text.split())['jesus'])
x = plib.thread_counter(text)
# for k, v in collections.Counter(text.split()).items():
#     if (i := x.get(k, 0)) != v:
#         ic(k, v, i)
