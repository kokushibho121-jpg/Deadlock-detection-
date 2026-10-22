"""Build and call the Recovery module's independent C action engine."""
from __future__ import annotations

import ctypes
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from recovery_state import SystemState

ROOT = Path(__file__).resolve().parent
HEADER = ROOT / "c_engine" / "include"
SOURCE = ROOT / "c_engine" / "src" / "recovery_engine.c"


def _library_path():
    # Keep the DLL outside OneDrive and build it separately for each user.
    cache_root = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return cache_root / "pbl_deadlock" / "recovery" / "recovery_engine.dll"


def _compile(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    compiler = shutil.which("cl")
    if not compiler:
        return "MSVC was not found. Start the app from x64 Native Tools Command Prompt for Visual Studio."

    obj = path.parent / "recovery_engine.obj"
    cmd = [compiler, "/nologo", "/LD", "/O2", f"/I{HEADER}", str(SOURCE),
           f"/Fe:{path}", f"/Fo:{obj}"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=45)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return str(exc)
    if result.returncode == 0:
        return None
    return result.stderr.strip() or result.stdout.strip() or "MSVC compilation failed."


def _load_library(path: Path):
    library = ctypes.CDLL(str(path))
    int_pointer = ctypes.POINTER(ctypes.c_int)
    library.recovery_apply.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
        ctypes.c_int, int_pointer, int_pointer, int_pointer, int_pointer, int_pointer]
    library.recovery_apply.restype = ctypes.c_int
    library.recovery_choose_victim.argtypes = [ctypes.c_int, ctypes.c_int, int_pointer, int_pointer, ctypes.c_int]
    library.recovery_choose_victim.restype = ctypes.c_int
    return library


class Engine:
    def __init__(self):
        self.library: ctypes.CDLL | None = None
        self.notice: str | None = None
        path = _library_path()
        sources = (HEADER / "recovery_engine.h", SOURCE)
        try:
            stale = not path.exists() or any(item.stat().st_mtime_ns > path.stat().st_mtime_ns for item in sources)
            if stale:
                path.unlink(missing_ok=True)
                error = _compile(path)
                if error:
                    raise RuntimeError(error)
            try:
                self.library = _load_library(path)
            except OSError:
                path.unlink(missing_ok=True)
                error = _compile(path)
                if error:
                    raise RuntimeError(error)
                self.library = _load_library(path)
        except (OSError, RuntimeError) as exc:
            self.notice = str(exc)

    @property
    def using_c(self):
        return self.library is not None

    def recover(self, state: SystemState, method: str, victim: int,
                resource: int | None = None):
        if not self.library:
            raise RuntimeError(self.notice or "The C recovery engine is unavailable.")
        updated = state.clone()
        p, r = updated.process_count, updated.resource_count
        # ctypes sends flat integer arrays to C, then copies the result back.
        allocations = (ctypes.c_int * (p * r))(*(v for row in updated.allocation for v in row))
        requests = (ctypes.c_int * (p * r))(*(v for row in updated.request for v in row))
        available = (ctypes.c_int * r)(*updated.available)
        active = (ctypes.c_int * p)(*updated.active)
        released = ctypes.c_int()
        method_id = 0 if method == "Process termination" else 1
        resource_id = -1 if resource is None else resource
        code = self.library.recovery_apply(p, r, method_id, victim, resource_id,
            allocations, requests, available, active, ctypes.byref(released))
        if code:
            raise ValueError("The selected process/resource cannot be recovered this way.")
        updated.allocation = [list(allocations[i*r:(i+1)*r]) for i in range(p)]
        updated.request = [list(requests[i*r:(i+1)*r]) for i in range(p)]
        updated.available = list(available)
        updated.active = list(active)
        return updated, released.value

    def select_victim(self, state: SystemState, candidates: list[int]):
        if not self.library:
            raise RuntimeError(self.notice or "The C recovery engine is unavailable.")
        allocation = (ctypes.c_int * (state.process_count * state.resource_count))(
            *(value for row in state.allocation for value in row))
        candidate_array = (ctypes.c_int * len(candidates))(*candidates)
        victim = self.library.recovery_choose_victim(state.process_count, state.resource_count,
            allocation, candidate_array, len(candidates))
        if victim < 0:
            raise ValueError("C victim selection could not choose from the selected processes.")
        return victim


_engine: Engine | None = None


def get_engine():
    global _engine
    if _engine is None:
        _engine = Engine()
    return _engine
