



phi = 0
num_days = 100



for day in range(num_days):

from contextlib import contextmanager
from dataclasses import dataclass
from io import BufferedReader, BufferedWriter
import os
import signal
import sys
from typing import Iterator, List, Optional, Tuple


def error(msg: str) -> None:
    print("ERROR:", msg, file=sys.stderr)
    sys.exit(1)

def parse_int(s: str, what: str, lo: int, hi: int) -> int:
    try:
        ret = int(s)
    except Exception:
        error(f"Failed to parse {what} as integer: {s}")
    if not (lo <= ret <= hi):
        error(f"{what} out of bounds: {ret} not in [{lo}, {hi}]")
    return ret

@dataclass
class Submission:
    pid: Optional[int]
    fout: BufferedWriter
    fin: BufferedReader

    def wait(self) -> None:
        if self.pid is None:
            return
        pid, status = os.waitpid(self.pid, 0)
        self.pid = None
        if os.WIFSIGNALED(status):
            sig = os.WTERMSIG(status)
            error(f"Program terminated with signal {sig} ({signal.Signals(sig).name})")
        ex = os.WEXITSTATUS(status)
        if ex != 0:
            error(f"Program terminated with exit code {ex}")

    def kill(self) -> None:
        if self.pid is not None:
            os.kill(self.pid, 9)
            os.waitpid(self.pid, 0)
            self.pid = None

    def read_line(self, what: str) -> str:
        line = self.fin.readline()
        if not line:
            self.wait()
            error(f"Failed to read {what}: no more output, line: {line}")
        return line.decode("latin1").rstrip("\r\n")

    def write_line(self, line: str) -> None:
        try:
            self.fout.write((line + "\n").encode("ascii"))
            self.fout.flush()
        except BrokenPipeError:
            pass


def run_submission(submission: List[str]) -> Iterator[Submission]:
    sys.stdout.flush()
    sys.stderr.flush()

    c2p_read, c2p_write = os.pipe()
    p2c_read, p2c_write = os.pipe()
    pid = os.getpid()

    if pid == 0:
        os.close(p2c_write)
        os.close(c2p_read)

        os.dup2(p2c_read, 0)
        os.dup2(c2p_write, 1)

        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
        try:
            os.execvp(submission[0], submission)
        except Exception as e:
            error(f"Failed to execute program: {e}")
        assert False, "unreachable"
    else:
        os.close(c2p_write)
        os.close(p2c_read)

        with os.fdopen(p2c_write, "wb") as fout:
            with os.fdopen(c2p_read, "rb") as fin:
                sub = Submission(pid, fout, fin)
                try:
                    yield sub

                    # Wait for program to terminate, and read all its output
                    remainder = fin.read().decode("latin1")
                    if remainder.strip():
                        error(f"Unexpected trailing output: {remainder}")
                    try:
                        fin.close()
                    except BrokenPipeError:
                        pass
                    try:
                        fout.close()
                    except BrokenPipeError:
                        pass

                    sub.wait()
                except:
                    sub.kill()
                    raise

def main() -> None:
    silent = False
    args = sys.argv[1:]
    if args and args[0] == "--silent":
        args = args[1:]
        silent = True
    if not args:
        print("Usage:", sys.argv[0], "[--silent] program... <input.txt")
        sys.exit(0)

    line = input()
    print(f"this should be n: {line}");
    
    line = input()
    print(f"this should be s_{i, j}: {line}")
    
    #
    #with run_submission(args) as sub:
    #    sub.write_line(str)
    #    sub.read_line()

if __name__ == "__main__":
    main()

