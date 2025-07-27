from tqdm import trange
from random import randint, random, uniform

def random_distribution(n: int) -> list[float]:
    v = [randint(1, int(1e6)) for i in range(n)]

    tot = sum(v)
    p = [v[i] / tot for i in range(n)]

    return p

def list_to_str(a: list[int|float]) -> str:
    return " ".join([str(a[i]) for i in range(len(a))]) + "\n"


def generate_test_case(output_file: str):
    x_lower = int(1e3)
    x_upper = int(1e4)
    n_upper = 100
    m_upper = 5
    a_i_upper = 100

    x = uniform(x_lower, x_upper)
    n = randint(1, n_upper)
    m = randint(1, m_upper)
    a = [randint(1, a_i_upper) for _ in range(n)]
    d = [[randint(1, a[i]) for _ in range(m)] for i in range(n)]
    p = [random_distribution(m) for i in range(n)]

    with open(output_file, "w") as f:
        f.write(f"{round(x, 6)} {n} {m}\n")
        f.write(list_to_str(a))

        for i in range(n):
            f.write(list_to_str(p[i]))

        for i in range(n):
            f.write(list_to_str(d[i]))

if __name__ == "__main__":
    NUM_TEST_CASES = 25
    print(f"Generating {NUM_TEST_CASES} test cases...")
    for i in trange(NUM_TEST_CASES):
        output_file = f"test_cases/input_{i + 1}.txt"
        generate_test_case(output_file)