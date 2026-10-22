# Deadlock Detection Simulator

A desktop application for demonstrating **operating-system deadlock detection**. It combines a Python Tkinter graphical user interface (GUI) with a C-based detection engine. Enter process/resource data, run the algorithm, and inspect whether the system is safe or which processes remain unable to finish.

## Features

- Configure the number of processes and resource types.
- Enter a **Resource Allocation Matrix**, **Request Matrix**, and **Available Resources** vector.
- Detect whether all processes can finish using the current available resources.
- Display a safe sequence when the system is safe.
- Identify processes that remain unfinished when deadlock is detected.
- View the C backend's detection steps and run the analysis again.
- Validate input sizes and reject empty, non-integer, or negative values.

## Project structure

```text
deadlock/
├── detection.c     # C implementation of the deadlock-detection algorithm
├── detection.exe   # Prebuilt Windows backend executable
├── gui.py          # Python Tkinter graphical interface
└── README.md       # Project documentation
```

## Requirements

- **Python 3** (Tkinter is included with many Python installations).
- A C compiler such as **GCC** if you need to rebuild the backend or run on a non-Windows platform.
- **Windows:** the included `detection.exe` can be used directly.
- **Linux/macOS:** compile `detection.c` to an executable named `detection` in the same directory as `gui.py`.

## Run the application

### Windows

1. Extract the project folder.
2. Ensure `gui.py` and `detection.exe` are in the same directory.
3. Open a terminal in that directory.
4. Run:

   ```bash
   python gui.py
   ```

### Linux

Install Python 3, Tkinter, and GCC if they are not already installed. On Debian/Ubuntu, for example:

```bash
sudo apt install python3 python3-tk gcc
```

Then, from the project directory:

```bash
gcc detection.c -o detection
chmod +x detection
python3 gui.py
```

### macOS

Make sure Python 3 with Tk support and a C compiler are installed, then run:

```bash
gcc detection.c -o detection
chmod +x detection
python3 gui.py
```

If Tkinter is missing from your Python installation, install a Python distribution that includes Tcl/Tk support.

## How to use

1. Launch the GUI.
2. Under **System Setup**, enter the number of processes and resource types, then select **Create System**.
3. Fill in the **Resource Allocation** matrix. Each cell represents the number of instances of a resource type currently held by a process.
4. Fill in the **Resource Requests** matrix. Each cell represents the additional instances of a resource type that the process is currently requesting.
5. Enter the **Available Resources** vector, representing the number of currently free instances of each resource type.
6. Select **Detect Deadlock**.
7. Review the result:
   - **System is safe:** all processes can finish in the simulated order; the GUI displays a safe sequence.
   - **Deadlock detected:** one or more processes remain unfinished; the GUI lists those processes.
8. Use **View Detection Steps** to inspect the backend output, **Run Detection Again** to repeat the analysis, or **Clear** to reset the input values.

Newly created matrix and available-resource fields default to `0`. Replace these defaults with the data for your scenario before running detection.

## Input limits and validation

- Processes: **1–1000**
- Resource types: **1–10**
- Allocation, request, and available-resource values must be non-negative integers.
- The allocation and request matrices must each contain one row per process and one column per resource type.

Make sure the values describe a consistent system. In particular, the available vector should represent resources currently free, and the request matrix should represent each process's outstanding request.

## Algorithm overview

The C backend uses a standard deadlock-detection-style work/finish procedure:

1. Initialize `Work` to the `Available` vector.
2. Mark every process as unfinished.
3. Find an unfinished process whose outstanding request is less than or equal to `Work` for every resource type.
4. Assume that process can finish, then add its allocated resources back to `Work` and mark it finished.
5. Repeat while at least one process can be marked finished during a pass.
6. If every process finishes, report a safe sequence. Otherwise, report the processes still marked unfinished as deadlocked.

The algorithm checks resource vectors component by component. For process `Pi`, it can proceed when:

```text
Request[i][j] <= Work[j] for every resource type j
```

When it proceeds, the simulated update is:

```text
Work[j] = Work[j] + Allocation[i][j]
```

**Terminology note:** this project reports a safe sequence when all processes can finish under the supplied state. When some processes cannot finish, it labels the remaining unfinished processes as deadlocked. As with resource-allocation models generally, interpret the result in the context of the accuracy and assumptions of the input data.

## How the GUI and C backend work together

- `gui.py` collects and validates the values entered by the user.
- The GUI serializes the data in this order: process count, resource count, allocation matrix, request matrix, and available vector.
- It starts the backend executable as a subprocess and sends the serialized input through standard input.
- `detection.c` runs the algorithm and writes its progress and final result to standard output.
- The GUI captures the output and presents a summary, including the safe sequence or unfinished processes.

Keep the backend executable in the **same directory** as `gui.py`. On Windows, its expected name is `detection.exe`; on Linux/macOS, the expected name is `detection`.

## Example input

For two processes and one resource type, an illustrative input state might be:

| Item | R1 |
|---|---:|
| P1 allocation | 1 |
| P2 allocation | 0 |
| P1 request | 0 |
| P2 request | 1 |
| Available | 0 |

In this example, P1 can finish immediately because it requests no additional resources. Its allocated resource is then returned to `Work`, allowing P2 to finish. The resulting safe sequence is `P1 → P2`.

## Troubleshooting

- **“Backend not found”**: confirm that the executable is named correctly and is beside `gui.py`. Recompile `detection.c` if necessary.
- **`gcc` is not recognized**: install GCC or another C compiler and ensure it is available on your terminal's `PATH`.
- **Tkinter import/display errors**: verify that your Python installation includes Tk support and that your environment has a graphical display.
- **Invalid input messages**: use whole numbers that are zero or greater, and ensure all matrix cells are filled.
- **No GUI window appears**: run `python gui.py` from a terminal to see any Python error messages.

## Limitations

- The application is a local educational simulator, not an operating-system process monitor.
- The program evaluates the state supplied by the user; it does not inspect real processes or resource usage.
- The implementation uses fixed array limits of 1000 processes and 10 resource types.
- The backend's input handling uses `scanf`; the GUI validates its own input before sending it to the backend.

## License

No license information was included with the supplied project files. Add a `LICENSE` file if you intend to distribute the project and want to specify reuse terms.
