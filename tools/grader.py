import os
import subprocess
import numpy as np

from tqdm import trange, tqdm

MINUTES = 8 * 60
DAYS = 100
PRICE_UPPER = 1
EXTERNAL_PRICE_UPPER = 5
FLOATING_POINT_EPSILON = 1e-3

def read_input(filename):
    with open(filename) as f:
        x, n, m = map(float, f.readline().split())
        x = float(x)
        n, m = int(n), int(m)
        
        a = list(map(int, f.readline().split()))
        p = [list(map(float, f.readline().split())) for _ in range(n)]
        d = [list(map(int, f.readline().split())) for _ in range(n)]

    return x, n, m, a, p, d

def run_solution(x, n, m, a, p, d, solution_cmd, input_filepath="input.txt"):
    process = subprocess.Popen(
        solution_cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=2
    )

    p = np.array(p, dtype=float)
    a = np.array(a, dtype=float)

    # Write the static input
    with open(input_filepath, "r") as f:
        static_input = f.read()
    process.stdin.write(static_input)
    process.stdin.flush()

    total_cost = 0.0
    remain_charge = np.array([u / 2 for u in a])

    for day in trange(DAYS, desc="Days: ", leave=False):
        # Write the dynamic input
        price = np.random.uniform(1, PRICE_UPPER, size=MINUTES)
        external_price = np.random.uniform(max(price), EXTERNAL_PRICE_UPPER)

        write_input = " ".join(map(str, price)) + "\n"
        write_input += str(external_price) + "\n"
        write_input += " ".join(map(str, remain_charge)) + "\n"

        process.stdin.write(write_input)
        process.stdin.flush()

        # Read the schedule
        s = np.zeros((n, MINUTES), dtype=float)
        for i in range(n):
            line = process.stdout.readline()
            if not line:
                raise RuntimeError("Solution terminated early.")
            
            row = np.fromstring(line, dtype=float, sep=' ')
            if len(row) != MINUTES:
                raise RuntimeError(f"Expected {MINUTES} values, got {len(row)}.")
            
            s[i] = row

        if s.min() < -FLOATING_POINT_EPSILON:
            raise RuntimeError(f"Negative values in schedule: {s.min()}.")

        # Update remaining charge
        remain_charge += s.sum(axis=1)

        if remain_charge.max() > x + FLOATING_POINT_EPSILON:
            raise RuntimeError(f"Charge {remain_charge.max()} exceeds maximum capacity {x}.")

        if (remain_charge > a + FLOATING_POINT_EPSILON).any():
            raise RuntimeError(f"Charge {remain_charge} exceeds initial capacities {a}.")

        # Calculate costs
        charge_cost = s.sum(axis=0) * price
        total_cost += charge_cost.sum()

        trips = np.array([np.random.choice(d[i], 1, p=p[i]) for i in range(n)]).flatten()
        penalty = np.maximum(trips - remain_charge, 0) * external_price
        total_cost += penalty.sum()


        remain_charge = np.clip(remain_charge - trips, 0, None)


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

