# Grid Load

## Overview

Grid Load is a project designed to optimize the charging schedules for a fleet of electric cars. The system accounts for station capacities, charging requirements for various trips, and cost constraints over 100 nights.

## Project Structure

- **tools/**
  - [`grader.py`](tools/grader.py): Manages evaluation of the charging schedule.
  - [`generator.py`](tools/generator.py): Generates input data for testing.
- **solutions/**
  - [`baseline.cpp`](solutions/baseline.cpp): Contains a barebones implementation of the charging algorithm.
- **task.md**: Provides a complete description of the problem with mathematical formulations and constraints.

## Problem Description

Bob's charging stations face constraints on energy drawn from the grid and must ensure that cars can complete their trips without incurring high costs.  
The goal is to minimize the total cost of charging while meeting the energy requirements for each car's trip.

View the full problem description with rendered formulas in [`task.md`](task.md).

## Usage

1. The system reads the static input.
2. For each night, dynamic input is processed.
3. The algorithm outputs a charging schedule that minimizes the total cost while meeting trip energy requirements.
4. The schedule is printed to standard output to be evaluated.

## Build & Run

Compile

```bash
g++ -O2 -o solution solutions/baseline.cpp
```

Generate test cases

```bash
python tools/generator.py
```

Run the grader

```bash
python tools/grader.py
```

## Results

| Name         | Cost per Car per Night |
|--------------|-------------------------|
| Baseline     |                  26.4368|
