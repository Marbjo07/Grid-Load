import os
import random
import subprocess
from tqdm import trange, tqdm
from random import uniform, random

MINUTES = 8 * 60
DAYS = 100
price_upper = 1
external_price_upper = 5

def read_input(filename):
    with open(filename) as f:
        x, n, m = map(float, f.readline().split())
        x = float(x)
        n, m = int(n), int(m)
        
        a = list(map(int, f.readline().split()))
        p = [list(map(float, f.readline().split())) for _ in range(n)]
        d = [list(map(int, f.readline().split())) for _ in range(n)]

    return x, n, m, a, p, d

def sample_trip(p_row):
    r = random()
    total = 0
    for idx, prob in enumerate(p_row):
        total += prob
        if r <= total:
            return idx
    return len(p_row) - 1

def run_solution(x, n, m, a, p, d, solution_cmd, input_filepath="input.txt"):
    process = subprocess.Popen(
        solution_cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    with open(input_filepath, "r") as f:
        static_input = f.read()
    process.stdin.write(static_input)
    process.stdin.flush()

    total_cost = 0.0
    remain_charge = [u / 2 for u in a]

    for day in trange(DAYS, desc="Days: ", leave=False):
        # Send current charge
        price = [uniform(1, price_upper) for _ in range(MINUTES)]
        external_price = uniform(max(price), external_price_upper)

        write_input = " ".join(map(str, price)) + "\n"
        write_input += str(external_price) + "\n"
        write_input += " ".join(map(str, remain_charge)) + "\n"

        process.stdin.write(write_input)
        process.stdin.flush()

        # Read schedule s (n rows, each with MINUTES values)
        s = [0] * n
        for i in range(n):
            line = process.stdout.readline()
            if not line:
                raise RuntimeError("Solution terminated early.")
            
            row = list(map(float, line.strip().split()))
            if len(row) != MINUTES:
                raise RuntimeError(f"Expected {MINUTES} values, got {len(row)}.")

            s[i] = row

        for i in range(n):
            charge = remain_charge[i]
            if charge > a[i]:
                raise RuntimeError(f"Charge {charge} exceeds capacity {a[i]} for station {i}.")

            mu_cost = 0.0
            for j in range(MINUTES):
                mu_cost += s[i][j] * price[j]
                charge += s[i][j]
            
            final_charge = charge
            trip = sample_trip(p[i])
            required = d[i][trip]
            
            penalty = max(required - final_charge, 0) * external_price
            total_cost += mu_cost + penalty
            
            remain_charge[i] = max(final_charge - required, 0)

    process.stdin.close()
    return_code = process.wait(timeout=2)

    if return_code != 0:
        stderr_output = process.stderr.read()
        raise RuntimeError(f"Solution exited with code {return_code}:\n{stderr_output}")

    return total_cost

def main():

    test_dir = "test_cases"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    total_cost = 0.0

    num_tests = len([name for name in os.listdir(test_dir) if name.endswith(".txt")])
    if num_tests == 0:
        print("No test cases found.")
        return
    
    print(f"Found {num_tests} test cases in {test_dir}")

    pbar = tqdm(os.listdir(test_dir))
    for idx, filename in enumerate(pbar):
        if not filename.endswith(".txt"):
            continue
        
        input_file = os.path.join(test_dir, filename)
        pbar.set_description(f"Processing {filename}")

        x, n, m, a, p, d = read_input(input_file)
        period_cost = run_solution(x, n, m, a, p, d, ["./solution"], input_file)
        total_cost += period_cost / n / DAYS

        pbar.set_postfix({"Cost": f"{total_cost / (idx + 1):.4f}"})

    average_cost = total_cost / num_tests
    print(f"Total Average Cost per Car per Night: {average_cost:.4f}")

if __name__ == "__main__":
    main()

