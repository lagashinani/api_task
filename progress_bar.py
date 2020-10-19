def my_progress_bar(lst):
    print("[" + "_" * (len(lst)) + "]", end="", flush=True)
    for i, elem in enumerate(lst):
        yield elem
        print("\r" * (2 + len(lst)), end="", flush=True)
        print("[" + "#" * (i + 1) + "_" * (len(lst) - i - 1) + "]", end="", flush=True)
    print("")