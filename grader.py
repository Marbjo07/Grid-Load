import subprocess
import random
from tqdm import trange

MINUTES = 8 * 60
DAYS = 100

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
    r = random.random()
    total = 0
    for idx, prob in enumerate(p_row):
        total += prob
        if r <= total:
            return idx
    return len(p_row) - 1

def run_solution(x, n, m, a, p, d, solution_cmd):
    print("Opened Subprocess")
    process = subprocess.Popen(
        solution_cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    with open("input.txt") as f:
        static_input = f.read()
    process.stdin.write(static_input)
    process.stdin.flush()

    phi = 0.0
    remain_charge = [el / 2 for el in a]

    for day in trange(DAYS, desc="Days: "):
        # Send current charge
        process.stdin.write(" ".join(map(str, remain_charge)) + "\n")
        process.stdin.flush()


        # Read schedule
        s = []
        for i in range(n):
            line = process.stdout.readline()
            if not line:
                raise RuntimeError("Solution terminated early.")
            row = list(map(float, line.strip().split()))
            if len(row) != MINUTES:
                raise RuntimeError(f"Expected {MINUTES} values, got {len(row)}.")
            s.append(row)
        
        for j in range(MINUTES):
            total = sum(s[i][j] for i in range(n))
            if total > x + 1e-6:
                raise ValueError(f"Exceeded max output x={x} at minute {j}: total={total}")


        # Simulate
        new_remain = [0] * n
        for i in range(n):
            charge = [remain_charge[i]]
            for j in range(MINUTES):
                charge.append(charge[-1] + s[i][j])
            trip = sample_trip(p[i])
            required = d[i][trip]

            # Find earliest minute with enough charge
            t = next((t for t in range(MINUTES+1) if charge[t] >= required), MINUTES)
            phi += t

            # Update remaining charge
            new_remain[i] = max(charge[-1] - required, 0)

        remain_charge = new_remain

    process.stdin.close()
    return_code = process.wait(timeout=2)
    if return_code != 0:
        stderr_output = process.stderr.read()
        raise RuntimeError(f"Solution exited with code {return_code}:\n{stderr_output}")

    return phi

def main():
    x, n, m, a, p, d = read_input("input.txt")
    phi = run_solution(x, n, m, a, p, d, ["./main.exe"])
    print(f"Penalty (lower is better): {phi:.4f}")

if __name__ == "__main__":
    main()

