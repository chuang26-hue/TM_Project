# Tracing NTM Behavior Project

**Course**: Theory of Computing (Fall 2024)  
**Member**: Phoebe Huang  

---

## Overview
This project simulates the behavior of a Non-Deterministic Turing Machine (NTM) defined by a `.csv` file. The machine decides the language **A = {0<sup>2<sup>n</sup></sup> | n ≥ 0}**, the set of all strings of 0s whose length is a power of 2. The simulation processes various input strings, traces state transitions, and determines whether each string is accepted, rejected, or if execution times out. It also computes metrics such as the depth of exploration, the number of configurations explored, and the average non-determinism.

---

## Objectives
- Simulate the behavior of an NTM for various input strings.
- Trace state transitions and output detailed paths to acceptance, rejection, or timeout.
- Analyze computational paths and provide metrics on depth, configurations explored, and non-determinism.

---

## Files
### Code
- **traceNTM_phoebe.py**: Python script that simulates the NTM using breadth-first search (BFS).

### Input / Test
- **input.txt**: Specifies:
  - The NTM `.csv` file.
  - Input strings to simulate.
  - Maximum depth and step limits for exploration.
- **NTM.csv**: Defines the NTM, including:
  - States, input/output alphabets, start state, accept/reject states, and transitions.

### Output
- **output_phoebe.txt**: Contains:
  - Simulation results (accept/reject/timeout).
  - Step-by-step paths traversed during simulation.
  - Summary metrics (depth, configurations explored, and average non-determinism).

---

## Results Summary Table

| Machine (NTM CSV File) | Input String           | Result      | Depth | Configurations Explored | Avg Non-Determinism (Configs / Depth) |
|-------------------------|------------------------|-------------|-------|--------------------------|---------------------------------------|
| NTM.csv                | 0                     | Accept      | 2     | 3                        | 1.50                                  |
| NTM.csv                | 00                    | Accept      | 7     | 8                        | 1.14                                  |
| NTM.csv                | 000                   | Reject      | 3     | 4                        | 1.33                                  |
| NTM.csv                | 0000                  | Accept      | 21    | 22                       | 1.05                                  |
| NTM.csv                | 00000                 | Reject      | 5     | 6                        | 1.20                                  |
| NTM.csv                | 000000                | Reject      | 18    | 19                       | 1.06                                  |
| NTM.csv                | 0000000               | Reject      | 7     | 8                        | 1.14                                  |
| NTM.csv                | 00000000              | Accept      | 57    | 58                       | 1.02                                  |
| NTM.csv                | 0000000000000000      | Timed Out   | 100   | 100                      | 1.00                                  |

---

## Metrics Explanation
- **Depth**: Number of levels in the tree of configurations explored.
- **Configurations Explored**: Total number of configurations visited during the simulation.
- **Average Non-Determinism**: Ratio of configurations explored to depth, representing the branching factor of the NTM at each level.

---

## Development and Testing
### How the Code Was Developed
- **Planning**: Broke the requirements into tasks like parsing the NTM, simulating transitions, and logging results.
- **Incremental Development**: Implemented features step-by-step, starting with parsing and adding branching logic and limits.
- **Testing**: Verified functionality with test cases at each stage.
- **Debugging**: Used error handling, assertions, and logging to fix issues like incorrect state transitions and infinite loops.

### Test Cases and Observations
- **Test Cases**: Used input strings `0`, `00`, `000`, ..., `00000000`, and `0000000000000000` to evaluate correctness.
  - Valid strings (lengths are powers of 2) verified the program’s ability to trace paths to acceptance.
  - Invalid strings tested rejection paths.
  - Long strings confirmed proper handling of timeout scenarios.
- **Results**:
  - For valid inputs, paths to acceptance were traced correctly.
  - Invalid inputs were rejected as expected.
  - Timeout limits worked for very long inputs.
  - Metrics accurately reflected exploration behavior.

---

## Discussion of Results
- **Correctness**: The program accurately simulated NTM behavior, identifying acceptance, rejection, or timeout for each input.
- **Performance**: Handled short and long inputs efficiently, demonstrating scalability within defined limits.
- **Edge Cases**: Handled invalid strings and timeout cases gracefully.

---

## Improvements for Future Work
- **Visualization**: Add a feature to graphically visualize state transitions and paths.
- **Comprehensive Testing**: Expand test cases to include empty strings and unexpected symbols.
- **Additional Metrics**: Include branching factor per state and analyze time complexity.

---

## Usage Instructions
1. **Setup**: Ensure the directory structure (code, input, output) is in place.
2. **Input File**: Edit `input/input.txt` to specify:
   - The NTM file name.
   - Input strings for testing.
   - Limits for depth and steps.
3. **Run Program**: Execute the command:

   ```bash
   python3 traceNTM_phoebe.py
