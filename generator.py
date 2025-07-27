from random import randint, random


def random_distribution(n: int) -> list[float]:
    v = [randint(1, 1e6) for i in range(n)]

    tot = sum(v)
    p = [v[i] / tot for i in range(n)]

    return p

def list_to_str(a: list[int|float]) -> str:
    return " ".join([str(a[i]) for i in range(len(a))]) + "\n"

n_upper = 1e5
x_upper = 10

x = 10 #random() * randint(1, x_upper)
n = 1000# randint(1, n_upper)
m = randint(1, 5)

a = [randint(1, 100) for _ in range(n)]
d = [[randint(1, a[i]) for _ in range(m)] for i in range(n)]
p = [random_distribution(m) for i in range(n)]


output_file = "input.txt"

with open(output_file, "w") as f:
    f.write(f"{round(x, 6)} {n} {m}\n")
    f.write(list_to_str(a))
    for i in range(n):
        f.write(list_to_str(p[i]))
    
    for i in range(n):
        f.write(list_to_str(d[i]))

