# Deadlock Detection and Recovery Simulator

## Project Title

**Deadlock Detection and Recovery Simulator Using C Data Structures and
Python Streamlit GUI**

### Alternative Title

**Deadlock Detection, Recovery and Resource Allocation Simulator Using C
and Python**

------------------------------------------------------------------------

# 1. Project Overview

This project is an Operating Systems + Data Structures simulator.

It simulates multiple processes competing for limited resources. The
system:

1.  Accepts processes and resources.
2.  Accepts resource allocation and resource requests.
3.  Detects whether the system is in a safe state or deadlock.
4.  Identifies processes involved in the deadlock.
5.  Attempts to recover from the deadlock.
6.  Releases or reallocates resources.
7.  Runs detection again.
8.  Shows whether the deadlock was successfully resolved.
9.  Visualizes the complete process using a Python Streamlit GUI.

## Core Architecture

-   **C = Core Operating System logic, data structures, detection and
    recovery**
-   **Python = Streamlit GUI, visualization, simulation control and
    analysis**

------------------------------------------------------------------------

# 2. Technology Stack

  ---------------------------------------------------------------------
  Technology                         Purpose
  ---------------------------------- ----------------------------------
  C                                  Core detection and recovery engine

  C Data Structures                  Arrays, matrices, structures,
                                     queues and graph-related logic

  Python                             Controller and application logic

  Streamlit                          Web-based GUI

  ctypes                             Communication between Python and
                                     compiled C engine

  NetworkX                           Resource Allocation Graph

  Matplotlib / Plotly                Charts and visualizations

  Git/GitHub                         Team collaboration and version
                                     control

  psutil                             Real OS process and resource
                                     monitoring
  ---------------------------------------------------------------------

## C-Python Communication

Preferred architecture:

``` text
Streamlit GUI
      ↓
Python Controller
      ↓
ctypes
      ↓
Compiled C Engine
      ↓
Detection / Recovery
      ↓
Result
      ↓
Streamlit GUI
```

------------------------------------------------------------------------

# 3. Main Objective

The objective is to build an interactive simulator that demonstrates how
operating systems detect and recover from deadlocks.

The application should:

-   Model processes and resources.
-   Represent resource allocation.
-   Represent resource requests.
-   Detect deadlocks.
-   Generate safe sequences.
-   Identify deadlocked processes.
-   Show resource dependencies.
-   Apply recovery methods.
-   Select a suitable victim process.
-   Release or preempt resources.
-   Re-run detection after recovery.
-   Show the final system state.

------------------------------------------------------------------------

# 4. Core Operating System Concepts

The project demonstrates:

-   Processes
-   Resources
-   Resource allocation
-   Resource requests
-   Waiting
-   Deadlock
-   Safe state
-   Unsafe state
-   Safe sequence
-   Resource Allocation Graph
-   Deadlock detection
-   Deadlock recovery
-   Process termination
-   Resource preemption

------------------------------------------------------------------------

# 5. Data Structures

## Arrays

Used for:

-   Process IDs
-   Resource IDs
-   Available resources
-   Work array
-   Finish array

Example:

``` c
int Available[MAX_RESOURCES];
int Work[MAX_RESOURCES];
bool Finish[MAX_PROCESSES];
```

## 2D Arrays / Matrices

Used for:

-   Allocation Matrix
-   Request Matrix

Example:

``` text
Allocation

       R1 R2 R3
P1      1  0  0
P2      0  1  0
P3      0  0  1
```

``` text
Request

       R1 R2 R3
P1      0  1  0
P2      0  0  1
P3      1  0  0
```

## Structures

Used to store process information.

Example:

``` c
typedef struct {
    int pid;
    int allocation[MAX_RESOURCES];
    int request[MAX_RESOURCES];
    int priority;
    int active;
} Process;
```

## Queue

Used during detection for processes that can potentially finish.

Example:

``` text
P1 → P4 → P2 → P3
```

## Graph

Used to represent the Resource Allocation Graph.

``` text
Process → Resource
Resource → Process
```

## Linked List

Optional. Can be used for:

-   Waiting processes
-   Deadlocked processes
-   Recovery history

------------------------------------------------------------------------

# 6. Deadlock Detection

The main detection algorithm uses:

-   Allocation
-   Request
-   Available
-   Work
-   Finish

## Basic Flow

``` text
Available
   ↓
Work = Available
   ↓
Find process where Request <= Work
   ↓
Pretend process finishes
   ↓
Work = Work + Allocation
   ↓
Mark process finished
   ↓
Repeat
   ↓
Processes that cannot finish
   ↓
Deadlocked Processes
```

If all processes can finish:

``` text
SAFE STATE
```

If some processes cannot finish:

``` text
DEADLOCK DETECTED
```

Example:

``` text
P1 → SAFE
P2 → DEADLOCKED
P3 → DEADLOCKED
P4 → SAFE
```

------------------------------------------------------------------------

# 7. Safe Sequence

The detector should generate a safe execution sequence whenever
possible.

Example:

``` text
Safe Sequence:

P1 → P4 → P2 → P3
```

If a safe sequence cannot be completed, the remaining processes are
reported as deadlocked.

------------------------------------------------------------------------

# 8. Resource Allocation Graph

The project includes a Resource Allocation Graph (RAG).

The graph contains:

-   Process nodes
-   Resource nodes
-   Request edges
-   Allocation edges

Example:

``` text
P1 → R2
R2 → P2
P2 → R3
R3 → P3
P3 → R1
R1 → P1
```

This forms a cycle:

``` text
P1 → R2 → P2 → R3 → P3 → R1 → P1
```

For appropriate resource configurations, a cycle indicates deadlock.

Python will visualize the graph using NetworkX and Matplotlib/Plotly.

------------------------------------------------------------------------

# 9. Deadlock Recovery

The recovery module starts when detection finds a deadlock.

At least two recovery methods are planned.

## Method 1: Process Termination

``` text
Deadlock detected
      ↓
Find deadlocked processes
      ↓
Select victim
      ↓
Terminate victim
      ↓
Release victim's resources
      ↓
Update Available
      ↓
Update system state
      ↓
Run detection again
```

Example:

``` text
Deadlocked:
P2, P3

Victim:
P3

P3 terminated.
Resources released.
Detection runs again.

DEADLOCK RESOLVED
```

## Method 2: Resource Preemption

``` text
Deadlock detected
      ↓
Select resource
      ↓
Select process
      ↓
Preempt resource
      ↓
Reallocate resource
      ↓
Update matrices
      ↓
Run detection again
```

Resource preemption is an advanced recovery feature.

------------------------------------------------------------------------

# 10. Victim Selection

The recovery module selects a process to terminate or preempt.

A simple scoring system can be used:

``` text
Victim Score =
    Resources Held
    + Priority Cost
    + Execution Cost
    + Recovery Cost
```

Example:

``` text
P1 → Score 8
P2 → Score 5
P3 → Score 3

Victim = P3
```

The exact formula can be simplified for the college implementation.

------------------------------------------------------------------------

# 11. Recovery Verification

After recovery, the system must run the detection algorithm again.

``` text
Recovery
   ↓
Update system
   ↓
Run detection again
   ↓
SAFE?
 /   \
YES   NO
 ↓     ↓
Done  Another Recovery Attempt
```

Possible final states:

``` text
DEADLOCK RESOLVED
```

or:

``` text
STILL DEADLOCKED
```

------------------------------------------------------------------------

# 12. Streamlit GUI

The GUI will use **Streamlit** instead of Tkinter.

## Main Application

``` text
DEADLOCK SIMULATOR

⚙️ System Setup
📊 Resource Allocation
🔍 Deadlock Detection
🕸️ Resource Allocation Graph
🔄 Recovery
📈 Statistics
```

## Recommended Pages / Sections

### 1. System Setup

-   Number of Processes
-   Number of Resources
-   Create System button

### 2. Resource Allocation

-   Allocation Matrix
-   Request Matrix
-   Available Resources
-   Input validation

### 3. Deadlock Detection

-   Detection button
-   Work/Finish steps
-   Process status
-   Safe sequence
-   Deadlocked processes

### 4. Resource Allocation Graph

-   Process nodes
-   Resource nodes
-   Allocation edges
-   Request edges
-   Before/after visualization

### 5. Recovery

-   Deadlocked process list
-   Process Termination
-   Resource Preemption
-   Victim selection
-   Recovery progress
-   Re-detection

### 6. Statistics

Display:

-   Number of processes
-   Number of resources
-   Number of deadlocked processes
-   Recovery method
-   Victim process
-   Number of resources released
-   Number of recovery attempts
-   Final system status
-   Safe sequence
-   Optional execution time

------------------------------------------------------------------------

# 13. Input Requirements

The user enters:

## Number of Processes

Example:

``` text
4
```

## Number of Resources

Example:

``` text
3
```

## Allocation Matrix

``` text
       R1 R2 R3
P1      1  0  0
P2      0  1  0
P3      0  0  1
P4      1  0  0
```

## Request Matrix

``` text
       R1 R2 R3
P1      0  1  0
P2      0  0  1
P3      1  0  0
P4      0  0  0
```

## Available Resources

``` text
R1 = 0
R2 = 0
R3 = 0
```

Input validation should prevent:

-   Negative values
-   Invalid numbers
-   Excessive process/resource counts
-   Invalid matrix dimensions
-   Invalid resource requests

------------------------------------------------------------------------

# 14. Detection Result

Example:

``` text
========================================
          DETECTION RESULT
========================================

P1     SAFE
P2     DEADLOCKED
P3     DEADLOCKED
P4     SAFE

STATUS: DEADLOCK DETECTED

Safe/Partial Sequence:
P1 → P4
```

The Streamlit interface should provide buttons or controls for:

``` text
[ Show Graph ]
[ Show Steps ]
[ Go To Recovery ]
```

------------------------------------------------------------------------

# 15. Step-by-Step Detection Visualization

The Streamlit GUI can show:

``` text
Step 1:
Work = Available

Step 2:
Check P1

Step 3:
P1 can finish

Step 4:
Work updated

Step 5:
Check P2

Step 6:
P2 cannot finish

...

Final:
P2 and P3 are deadlocked.
```

This is useful for project demonstration and viva.

------------------------------------------------------------------------

# 16. Recovery Screen

Example:

``` text
========================================
          DEADLOCK RECOVERY
========================================

Deadlocked Processes:
P2, P3

Recovery Method:

( ) Process Termination
( ) Resource Preemption

[ START RECOVERY ]
```

------------------------------------------------------------------------

# 17. Recovery Visualization

Example:

``` text
DEADLOCK DETECTED
       ↓
P2, P3 identified
       ↓
Calculate victim scores
       ↓
P3 selected
       ↓
Terminate P3
       ↓
Release resources
       ↓
Update system
       ↓
Run detection again
       ↓
SAFE STATE
```

------------------------------------------------------------------------

# 18. Final Result

Example:

``` text
========================================
             FINAL RESULT
========================================

Initial State:
DEADLOCK

Deadlocked Processes:
P2, P3

Recovery Method:
Process Termination

Victim:
P3

Resources Released:
2

Recovery Attempts:
1

Final State:
SAFE

Safe Sequence:
P3 → P2 → P1 → P4
```

------------------------------------------------------------------------

# 19. Four-Member Team Roles

## Member 1 --- C Detection Engine Developer

### Role

**Backend / Deadlock Detection Developer**

### Technology

-   C
-   C Data Structures

### Responsibilities

-   Process structure
-   Resource structure
-   Process management
-   Resource management
-   Allocation Matrix
-   Request Matrix
-   Available array
-   Work array
-   Finish array
-   Queue
-   Deadlock Detection Algorithm
-   Safe sequence
-   Deadlocked process identification
-   Resource allocation/release
-   Prepare C functions for Python integration

### Files

``` text
process.c
process.h
resource.c
resource.h
queue.c
queue.h
detection.c
detection.h
```

### Main Output

``` text
SAFE / DEADLOCK
Safe Sequence
Deadlocked Process IDs
```

------------------------------------------------------------------------

## Member 2 --- Streamlit Detection UI Developer

### Role

**Frontend / Detection Visualization Developer**

### Technology

-   Python
-   Streamlit
-   NetworkX
-   Matplotlib / Plotly

### Responsibilities

-   Main Streamlit interface
-   Process/resource input
-   Allocation Matrix UI
-   Request Matrix UI
-   Available Resource UI
-   Detection interface
-   Detection result screen
-   Safe sequence display
-   Deadlocked process display
-   Step-by-step detection visualization
-   Resource Allocation Graph
-   Connect Streamlit to C detection engine

### Files

``` text
gui.py
detection_gui.py
detection_visualizer.py
graph.py
matrix_view.py
```

### Main Output

``` text
Interactive Streamlit Dashboard
Detection Visualization
Resource Allocation Graph
Detection Explanation
```

------------------------------------------------------------------------

## Member 3 --- C Recovery Engine Developer

### Role

**Backend / Deadlock Recovery Developer**

### Technology

-   C
-   C Data Structures

### Responsibilities

-   Receive deadlocked process IDs
-   Process termination
-   Resource preemption
-   Resource release
-   Update Allocation Matrix
-   Update Available resources
-   Victim selection
-   Recovery cost
-   Re-run detection
-   Recovery result
-   Prepare C recovery functions for Python integration

### Files

``` text
recovery.c
recovery.h
victim.c
victim.h
```

### Main Output

``` text
Victim
Recovery Method
Released Resources
Recovery Status
```

------------------------------------------------------------------------

## Member 4 --- Streamlit Recovery, Analysis & Testing Developer

### Role

**Recovery UI / Analysis / Testing Developer**

### Technology

-   Python
-   Streamlit
-   NetworkX
-   Matplotlib / Plotly

### Responsibilities

-   Recovery Streamlit interface
-   Recovery method selection
-   Deadlocked process display
-   Victim display
-   Recovery progress
-   Before/after graph
-   Recovery visualization
-   Statistics
-   Test cases
-   Error handling
-   Integration testing
-   Final result screen

### Files

``` text
recovery_gui.py
recovery_visualizer.py
recovery_analysis.py
charts.py
test_cases.txt
```

### Main Output

``` text
Before Recovery
      ↓
Recovery Process
      ↓
After Recovery
      ↓
SAFE / STILL DEADLOCKED
```

------------------------------------------------------------------------

# 20. Complete Team Architecture

``` text
                         USER
                           ↓
                 ┌──────────────────┐
                 │  STREAMLIT GUI   │
                 │                  │
                 │ Member 2 + 4    │
                 └────────┬─────────┘
                          ↓
                   Python Controller
                          ↓
                        ctypes
                          ↓
                 ┌──────────────────┐
                 │    C ENGINE      │
                 │                  │
                 │ Member 1         │
                 │ Detection        │
                 │                  │
                 │ Member 3         │
                 │ Recovery         │
                 └────────┬─────────┘
                          ↓
                     DETECTION
                     /       \
                   SAFE      DEADLOCK
                    ↓           ↓
             Safe Sequence   Deadlocked PIDs
                                ↓
                             RECOVERY
                           /          \
                    Termination    Preemption
                           \          /
                              ↓
                       Release Resources
                              ↓
                         Detect Again
                              ↓
                    SAFE / STILL DEADLOCKED
                              ↓
                       Streamlit Result
```

------------------------------------------------------------------------

# 21. Project Folder Structure

``` text
Deadlock-Simulator/
│
├── README.md
├── requirements.txt
│
├── c_engine/
│   ├── include/
│   │   ├── process.h
│   │   ├── resource.h
│   │   ├── queue.h
│   │   ├── graph.h
│   │   ├── detection.h
│   │   ├── recovery.h
│   │   └── victim.h
│   │
│   ├── src/
│   │   ├── main.c
│   │   ├── process.c
│   │   ├── resource.c
│   │   ├── queue.c
│   │   ├── graph.c
│   │   ├── detection.c
│   │   ├── recovery.c
│   │   └── victim.c
│   │
│   ├── build/
│   │   └── deadlock_engine.dll
│   │
│   └── Makefile
│
├── python_gui/
│   ├── main.py
│   ├── gui.py
│   ├── simulator.py
│   ├── c_interface.py
│   │
│   ├── detection/
│   │   ├── detection_gui.py
│   │   └── detection_visualizer.py
│   │
│   ├── recovery/
│   │   ├── recovery_gui.py
│   │   ├── recovery_visualizer.py
│   │   └── recovery_analysis.py
│   │
│   └── visualization/
│       ├── graph.py
│       ├── matrix_view.py
│       └── charts.py
│
├── data/
│   ├── safe_cases/
│   ├── deadlock_cases/
│   └── recovery_cases/
│
├── tests/
│   ├── test_detection.c
│   ├── test_recovery.c
│   └── test_cases.txt
│
└── docs/
    ├── project_report.pdf
    ├── flowchart.png
    ├── architecture.png
    └── presentation.pptx
```

------------------------------------------------------------------------

# 22. Development Phases

## Phase 1 --- System + Detection

### Member 1

Build:

-   Process management
-   Resource management
-   Matrices
-   Detection engine

### Member 2

Build:

-   Streamlit detection UI
-   Input screens
-   Detection result display
-   Resource Allocation Graph

### Member 3

Prepare:

-   Recovery module design
-   Recovery data requirements
-   Detection-to-recovery interface

### Member 4

Prepare:

-   Test scenarios
-   Expected outputs
-   Streamlit recovery requirements
-   Recovery test data

### Phase 1 Output

``` text
Input
 ↓
Allocation + Request
 ↓
Detection
 ↓
SAFE / DEADLOCK
```

------------------------------------------------------------------------

# 23. Phase 2 --- Recovery

### Member 1

-   Expose detection functions needed after recovery
-   Support re-detection

### Member 2

-   Connect detection results to recovery UI
-   Display deadlocked processes

### Member 3

Implement:

-   Process termination
-   Resource preemption
-   Victim selection
-   Resource release
-   Re-detection

### Member 4

Build:

-   Recovery Streamlit UI
-   Recovery visualization
-   Recovery progress
-   Statistics

### Phase 2 Output

``` text
DEADLOCK
 ↓
RECOVERY
 ↓
RESOURCE RELEASE
 ↓
DETECTION AGAIN
 ↓
SAFE / STILL DEADLOCKED
```

------------------------------------------------------------------------

# 24. Phase 3 --- Real OS Integration + Testing

Phase 3 connects the complete simulator to the **actual operating
system**. The existing C detection and recovery engine remains the core
of the project, while Python obtains real OS information and Streamlit
provides the interface.

## Phase 3 Architecture

``` text
                ACTUAL OPERATING SYSTEM
                         ↓
              Real Processes / Resources
                         ↓
                 Python OS Monitor
                    (psutil)
                         ↓
                   Streamlit GUI
                         ↓
                      ctypes
                         ↓
                    C Engine
                 ↙             ↘
          Detection          Recovery
                 ↘             ↙
                  Re-detection
                         ↓
                  OS State Again
                         ↓
                 Streamlit Result
```

## Member 1 --- C OS/Detection Integration

-   Finalize the C detection engine.
-   Expose C functions through a DLL/shared library.
-   Accept process/resource data collected from the real OS.
-   Convert received data into allocation, request and available arrays.
-   Run deadlock detection on the mapped OS data.
-   Support re-detection after recovery.
-   Validate all C-Python data passed through `ctypes`.

## Member 2 --- Streamlit + OS Monitoring

-   Build the Real OS Monitoring page.
-   Display currently running processes.
-   Display PID, process name and process status.
-   Display selected system resource information.
-   Allow the user to choose processes/resources for analysis.
-   Send collected information to the C engine.
-   Display detection results and Resource Allocation Graph.

## Member 3 --- C Recovery + OS Recovery Integration

-   Connect the recovery engine with real OS process information.
-   Implement victim selection.
-   Release/recalculate simulated resource allocations.
-   Re-run detection after recovery.
-   For actual OS control, implement only a controlled and
    user-confirmed operation.
-   Prevent accidental termination of critical/system processes.
-   Log every recovery action and its result.

## Member 4 --- OS Recovery UI + Testing

-   Build the Real OS Recovery Streamlit interface.
-   Show detected/deadlocked processes.
-   Show selected recovery/victim process.
-   Display before/after OS information.
-   Create integration and edge-case tests.
-   Test Simulation Mode and Real OS Mode.
-   Prepare final demonstration and statistics.

## Real OS Mode

The project will contain two operating modes.

### Mode 1 --- Simulation Mode

``` text
User Input
    ↓
Allocation + Request + Available
    ↓
C Detection
    ↓
Deadlock
    ↓
C Recovery
    ↓
Re-detection
```

### Mode 2 --- Real OS Monitoring Mode

``` text
Actual OS
    ↓
Running Processes
    ↓
Resource Monitoring
    ↓
Resource Mapping Layer
    ↓
Allocation / Request / Available Model
    ↓
C Detection
    ↓
Result
```

The Resource Mapping Layer is important because normal OS monitoring
information does not automatically provide a complete deadlock
allocation/request matrix. The project must define how observed OS
process/resource information is mapped into the matrices required by the
C deadlock algorithm.

## Real OS Recovery

Real OS recovery is an advanced feature and must be controlled.

``` text
Detect Deadlock
      ↓
Show Affected Process
      ↓
User Confirmation
      ↓
Select Recovery Action
      ↓
Perform Controlled Action
      ↓
Read OS State Again
      ↓
Rebuild Resource Model
      ↓
Run C Detection Again
      ↓
SAFE / STILL DEADLOCKED
```

The application should not automatically terminate arbitrary system
processes. Critical/system processes must be protected, and destructive
operations should require explicit confirmation.

## Phase 3 Final Output

``` text
Actual Operating System
          ↓
   Python OS Monitor
          ↓
      Streamlit
          ↓
        ctypes
          ↓
       C Engine
          ↓
   ┌──────┴──────┐
Detection      Recovery
   └──────┬──────┘
          ↓
     Re-detection
          ↓
   Read OS State Again
          ↓
     Final Result
```

------------------------------------------------------------------------

# 25. Test Cases

At minimum:

## Test 1 --- No Deadlock

Expected:

``` text
SAFE
```

## Test 2 --- Simple Deadlock

Expected:

``` text
DEADLOCK DETECTED
```

## Test 3 --- Multiple Deadlocks

Expected:

``` text
P1, P2, P3 DEADLOCKED
```

## Test 4 --- Successful Recovery

``` text
Deadlock
 ↓
Terminate P3
 ↓
Resources Released
 ↓
SAFE
```

## Test 5 --- Recovery Failure

``` text
Recovery Attempt
 ↓
Still Deadlocked
 ↓
Second Recovery Attempt
 ↓
Resolved
```

## Test 6 --- Invalid Input

Examples:

``` text
Negative resources
Invalid matrix size
Non-numeric input
Invalid resource request
```

## Test 7 --- Real OS Process Monitoring

Expected:

``` text
Actual running processes displayed
PID and process information collected
```

## Test 8 --- Real OS Data to C Engine

Expected:

``` text
OS data
 ↓
Resource Mapping
 ↓
C Detection
 ↓
SAFE / DEADLOCK RESULT
```

## Test 9 --- OS Recovery Verification

Expected:

``` text
Recovery Action
 ↓
OS State Read Again
 ↓
Resource Model Updated
 ↓
C Detection Again
 ↓
SAFE / STILL DEADLOCKED
```

## Test 10 --- Protected System Process

Expected:

``` text
Critical/System Process
 ↓
Recovery blocked
 ↓
Safe warning shown
```

------------------------------------------------------------------------

# 26. Minimum Version

If the project deadline is short, implement:

## C

-   Structures
-   Arrays
-   2D matrices
-   Queue
-   Detection Algorithm
-   Process Termination Recovery

## Python

-   Streamlit
-   Basic dashboard
-   NetworkX
-   Basic Resource Allocation Graph
-   Result display
-   `psutil` for real OS process/resource monitoring
-   Simulation Mode + Real OS Monitoring Mode

For the first working OS-connected version, make real OS monitoring
read-only. Add actual OS control only after detection and data mapping
are verified.

Do not start with complicated resource preemption or advanced statistics
until the basic system is working.

------------------------------------------------------------------------

# 27. Advanced Version

After the minimum version works, add:

-   Resource preemption
-   Automatic victim selection
-   Recovery cost
-   Step-by-step animation
-   Resource Allocation Graph
-   Before/after visualization
-   Multiple test scenarios
-   Performance statistics
-   Recovery comparison
-   Random deadlock generation
-   Safe/unsafe state visualization

------------------------------------------------------------------------

# 28. Important Integration Rule

Do not make four independent projects.

The connection must be:

``` text
Member 1 Detection Output
        ↓
Deadlocked Process IDs
        ↓
Member 3 Recovery Input
        ↓
Recovery Result
        ↓
Member 1 Detection Again
        ↓
Final State
```

Members 2 and 4 visualize the same data in Streamlit rather than
creating separate logic.

The C engine remains the source of truth for the actual detection and
recovery algorithms.

------------------------------------------------------------------------

# 29. Final Demonstration

A good demonstration should follow:

``` text
1. Open Streamlit application

2. Enter:
   Processes = 4
   Resources = 3

3. Enter Allocation Matrix

4. Enter Request Matrix

5. Enter Available Resources

6. Click Detect Deadlock

7. Show:
   - Work/Finish steps
   - Deadlocked processes
   - Resource Allocation Graph

8. Open Recovery

9. Select:
   Process Termination

10. Show victim selection

11. Terminate selected process

12. Release resources

13. Run detection again

14. Show:
    DEADLOCK RESOLVED

15. Display:
    - Safe sequence
    - Recovery statistics
    - Before/after graph
```

------------------------------------------------------------------------

# 30. Viva Roles

## Member 1

> "I developed the C backend for process and resource management and
> implemented the deadlock detection algorithm using arrays, matrices,
> structures and queues."

## Member 2

> "I developed the Streamlit interface and Resource Allocation Graph
> visualization for entering system data and displaying detection
> results."

## Member 3

> "I implemented the C recovery module, including process termination,
> resource preemption, victim selection, resource release and
> re-detection."

## Member 4

> "I developed the Streamlit recovery interface, recovery visualization,
> statistics and complete system testing."

------------------------------------------------------------------------

# 31. Final Project Summary

``` text
C ENGINE
├── Data Structures
├── Process Management
├── Resource Management
├── Deadlock Detection
├── Safe Sequence
├── Graph Logic
└── Deadlock Recovery

PYTHON
├── Streamlit GUI
├── NetworkX
├── Matplotlib / Plotly
├── Visualization
├── Simulation
└── Analysis
```

## Final Application Flow

``` text
USER
 ↓
STREAMLIT GUI
 ↓
PYTHON CONTROLLER
 ↓
CTYPES
 ↓
C ENGINE
 ↓
DEADLOCK DETECTION
 ↓
DEADLOCK?
 ├── NO → SAFE SEQUENCE
 │
 └── YES
       ↓
   DEADLOCKED PROCESSES
       ↓
     RECOVERY
       ↓
 TERMINATE / PREEMPT
       ↓
 RELEASE RESOURCES
       ↓
   DETECT AGAIN
       ↓
 SAFE / STILL DEADLOCKED
       ↓
 STREAMLIT VISUALIZATION
```

------------------------------------------------------------------------

# 32. Project Rule

The final system should be one integrated application:

**Streamlit Frontend + Python Controller + C Detection/Recovery Engine**

The UI should not duplicate the core OS algorithms. C performs the
important detection and recovery operations, while Python/Streamlit
handles user interaction, visualization, simulation control and
analysis.
