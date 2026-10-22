# Recovery Module (Phase 2)

This standalone Streamlit app demonstrates deadlock recovery actions. The recovery operations run in C; Python provides the interface and calls the C functions. Detection is handled by the separate Detection module.

## Requirements

- Windows 10 or 11
- Python 3.11 or newer
- Visual Studio Build Tools with **Desktop development with C++** and the x64 tools

## First-time setup and run (CMD)

1. Extract this folder from the ZIP.
2. Open **x64 Native Tools Command Prompt for Visual Studio** from the Start menu.
3. Change to the extracted `recovery` folder. Replace the example path with your actual folder:

   ```cmd
   cd /d "C:\path\to\recovery"
   ```

4. Run these commands once to set up the Python packages:

   ```cmd
   py -m venv .venv
   .venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

5. Start the app:

   ```cmd
   .venv\Scripts\python.exe -m streamlit run app.py
   ```

Open the local URL printed in the command window (usually `http://localhost:8501`). Keep the window open while using the app. Press **Ctrl+C** in that window to stop it.

The C DLL is compiled automatically on first launch and stored in the current Windows user's local AppData folder. Each teammate should create their own `.venv` and DLL by following these steps; do not share those generated folders.

Use **Undo last action** to reverse a simulated recovery and **Redo last action** to reapply it. A new recovery action clears the redo history.

## Main files

- `app.py` — main Streamlit workflow.
- `recovery_state.py` — resource data and input validation.
- `recovery_ui.py` — state form, resource graph, and compiler status.
- `c_interface.py` — compiles the C file and calls its functions.
- `c_engine/include/recovery_engine.h` and `c_engine/src/recovery_engine.c` — C recovery functions.
- `requirements.txt` — Python package list.
