import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import subprocess
import re
import os

# ============================================================
# Deadlock Detection Simulator - GUI V2
# Member 2: Frontend + Detection Visualization
#
# Integration:
# Tkinter GUI -> detection.exe -> captured C output -> GUI result
#
# Keep gui.py and detection.exe in the same folder.
# ============================================================

APP_TITLE = "Deadlock Detection Simulator"

# ---------- Visual design ----------
BG = "#F5F6F8"
CARD = "#FFFFFF"
TEXT = "#20242A"
MUTED = "#68727E"
BORDER = "#E0E4E8"
ACCENT = "#315EFB"
ACCENT_HOVER = "#244BD0"
SAFE = "#218739"
SAFE_BG = "#EAF6ED"
DANGER = "#C73737"
DANGER_BG = "#FCECEC"
WARN = "#A56A00"
WARN_BG = "#FFF5DC"

FONT = "Segoe UI"

BASE_DIR = Path(__file__).resolve().parent
C_EXE = BASE_DIR / ("detection.exe" if os.name == "nt" else "detection")


class DeadlockGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(APP_TITLE)
        self.geometry("1120x760")
        self.minsize(980, 650)
        self.configure(bg=BG)

        self.n = 0
        self.m = 0
        self.allocation_entries = []
        self.request_entries = []
        self.available_entries = []
        self.last_output = ""

        self.configure_styles()
        self.build_ui()

    # ========================================================
    # STYLING
    # ========================================================

    def configure_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(
            "TEntry",
            font=(FONT, 10),
            padding=(7, 6),
            fieldbackground="white",
            background="white",
            foreground=TEXT,
            bordercolor=BORDER,
            lightcolor=BORDER,
            darkcolor=BORDER,
        )

        style.configure(
            "Primary.TButton",
            font=(FONT, 10, "bold"),
            padding=(17, 9),
            background=ACCENT,
            foreground="white",
            borderwidth=0,
        )
        style.map(
            "Primary.TButton",
            background=[("active", ACCENT_HOVER), ("disabled", "#AEB9D8")],
        )

        style.configure(
            "Secondary.TButton",
            font=(FONT, 10),
            padding=(14, 8),
            background=CARD,
            foreground=TEXT,
            borderwidth=1,
        )
        style.map(
            "Secondary.TButton",
            background=[("active", "#F0F2F5")],
        )

    def card(self, parent):
        return tk.Frame(
            parent,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1,
            bd=0,
        )

    # ========================================================
    # MAIN UI
    # ========================================================

    def build_ui(self):
        self.build_header()
        self.build_setup()
        self.build_scroll_area()
        self.build_result_area()
        self.build_fixed_action_bar()

    def build_header(self):
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=32, pady=(24, 8))

        left = tk.Frame(header, bg=BG)
        left.pack(side="left")

        tk.Label(
            left,
            text="Deadlock Detection",
            bg=BG,
            fg=TEXT,
            font=(FONT, 24, "bold"),
        ).pack(anchor="w")

        tk.Label(
            left,
            text="Analyse processes and resource dependencies",
            bg=BG,
            fg=MUTED,
            font=(FONT, 10),
        ).pack(anchor="w", pady=(3, 0))

        status = "Backend ready" if C_EXE.exists() else "Backend not found"
        status_color = SAFE if C_EXE.exists() else WARN

        self.backend_status = tk.Label(
            header,
            text=f"● {status}",
            bg=BG,
            fg=status_color,
            font=(FONT, 9, "bold"),
        )
        self.backend_status.pack(side="right", anchor="n", pady=8)

    def build_setup(self):
        card = self.card(self)
        card.pack(fill="x", padx=32, pady=(8, 10))

        inner = tk.Frame(card, bg=CARD)
        inner.pack(fill="x", padx=20, pady=16)

        tk.Label(
            inner,
            text="SYSTEM SETUP",
            bg=CARD,
            fg=MUTED,
            font=(FONT, 9, "bold"),
        ).grid(row=0, column=0, columnspan=5, sticky="w", pady=(0, 9))

        tk.Label(
            inner, text="Processes", bg=CARD, fg=TEXT, font=(FONT, 10)
        ).grid(row=1, column=0, sticky="w")

        tk.Label(
            inner, text="Resources", bg=CARD, fg=TEXT, font=(FONT, 10)
        ).grid(row=1, column=1, sticky="w", padx=(20, 0))

        self.process_var = tk.StringVar(value="4")
        self.resource_var = tk.StringVar(value="3")

        ttk.Entry(
            inner, textvariable=self.process_var, width=8
        ).grid(row=2, column=0, sticky="w", pady=(4, 0))

        ttk.Entry(
            inner, textvariable=self.resource_var, width=8
        ).grid(row=2, column=1, sticky="w", padx=(20, 0), pady=(4, 0))

        ttk.Button(
            inner,
            text="Create System",
            style="Primary.TButton",
            command=self.create_system,
        ).grid(row=2, column=4, sticky="e")

        inner.grid_columnconfigure(3, weight=1)

    def build_scroll_area(self):
        outer = tk.Frame(self, bg=BG)
        outer.pack(fill="both", expand=True, padx=32)

        self.canvas = tk.Canvas(
            outer,
            bg=BG,
            highlightthickness=0,
            bd=0,
        )
        self.scrollbar = ttk.Scrollbar(
            outer, orient="vertical", command=self.canvas.yview
        )

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.content = tk.Frame(self.canvas, bg=BG)
        self.window_id = self.canvas.create_window(
            (0, 0), window=self.content, anchor="nw"
        )

        self.content.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            ),
        )
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfigure(
                self.window_id, width=e.width
            ),
        )

        # Mouse wheel makes the matrices easier to use.
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        self.matrix_area = tk.Frame(self.content, bg=BG)
        self.matrix_area.pack(fill="x", pady=(0, 12))

        self.show_placeholder()

    def on_mousewheel(self, event):
        if self.canvas.winfo_exists():
            self.canvas.yview_scroll(int(-event.delta / 120), "units")

    def show_placeholder(self):
        for w in self.matrix_area.winfo_children():
            w.destroy()

        card = self.card(self.matrix_area)
        card.pack(fill="x")

        tk.Label(
            card,
            text="Enter the number of processes and resources, then click "
                 "\"Create System\".",
            bg=CARD,
            fg=MUTED,
            font=(FONT, 10),
            pady=25,
        ).pack()

    # ========================================================
    # FIXED ACTION BAR
    # ========================================================

    def build_fixed_action_bar(self):
        # This bar intentionally lives OUTSIDE the scrolling canvas.
        # Therefore the main action is always visible regardless of
        # how tall the matrices are.
        self.action_bar = tk.Frame(
            self,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1,
            bd=0,
        )
        self.action_bar.pack(
            fill="x",
            padx=32,
            pady=(0, 18),
        )

        inner = tk.Frame(self.action_bar, bg=CARD)
        inner.pack(fill="x", padx=16, pady=11)

        tk.Label(
            inner,
            text="READY TO ANALYSE",
            bg=CARD,
            fg=MUTED,
            font=(FONT, 9, "bold"),
        ).pack(side="left")

        self.clear_button = ttk.Button(
            inner,
            text="Clear",
            style="Secondary.TButton",
            command=self.clear_inputs,
        )
        self.clear_button.pack(side="right", padx=(8, 0))

        self.detect_button = ttk.Button(
            inner,
            text="Detect Deadlock",
            style="Primary.TButton",
            command=self.detect,
        )
        self.detect_button.pack(side="right")

    # ========================================================
    # MATRIX UI
    # ========================================================

    def section_card(self, parent, title, subtitle):
        card = self.card(parent)

        header = tk.Frame(card, bg=CARD)
        header.pack(fill="x", padx=18, pady=(14, 8))

        tk.Label(
            header,
            text=title,
            bg=CARD,
            fg=TEXT,
            font=(FONT, 11, "bold"),
        ).pack(anchor="w")

        tk.Label(
            header,
            text=subtitle,
            bg=CARD,
            fg=MUTED,
            font=(FONT, 9),
        ).pack(anchor="w", pady=(2, 0))

        body = tk.Frame(card, bg=CARD)
        body.pack(fill="x", padx=18, pady=(0, 15))

        return card, body

    def create_matrix(self, parent, n, m):
        entries = []

        grid = tk.Frame(parent, bg=CARD)
        grid.pack(anchor="w")

        tk.Label(
            grid, text="", bg=CARD, width=6
        ).grid(row=0, column=0)

        for j in range(m):
            tk.Label(
                grid,
                text=f"R{j+1}",
                bg=CARD,
                fg=MUTED,
                font=(FONT, 9, "bold"),
                width=7,
            ).grid(row=0, column=j + 1, padx=2, pady=(0, 3))

        for i in range(n):
            tk.Label(
                grid,
                text=f"P{i+1}",
                bg=CARD,
                fg=TEXT,
                font=(FONT, 9, "bold"),
                width=6,
                anchor="w",
            ).grid(row=i + 1, column=0, sticky="w", pady=2)

            row = []

            for j in range(m):
                entry = ttk.Entry(
                    grid,
                    width=7,
                    justify="center",
                )
                entry.insert(0, "0")
                entry.grid(
                    row=i + 1,
                    column=j + 1,
                    padx=2,
                    pady=2,
                )
                row.append(entry)

            entries.append(row)

        return entries

    def create_available(self, parent, m):
        frame = tk.Frame(parent, bg=CARD)
        frame.pack(anchor="w")

        entries = []

        for j in range(m):
            box = tk.Frame(frame, bg=CARD)
            box.grid(row=0, column=j, padx=(0, 10))

            tk.Label(
                box,
                text=f"R{j+1}",
                bg=CARD,
                fg=MUTED,
                font=(FONT, 9, "bold"),
            ).pack(anchor="w")

            entry = ttk.Entry(box, width=7, justify="center")
            entry.insert(0, "0")
            entry.pack(pady=(3, 0))

            entries.append(entry)

        return entries

    def create_system(self):
        try:
            n = int(self.process_var.get().strip())
            m = int(self.resource_var.get().strip())
        except ValueError:
            messagebox.showerror(
                "Invalid system size",
                "Processes and resources must be whole numbers.",
            )
            return

        if n < 1 or n > 1000:
            messagebox.showerror(
                "Invalid processes",
                "Processes must be between 1 and 1000.",
            )
            return

        if m < 1 or m > 10:
            messagebox.showerror(
                "Invalid resources",
                "Resources must be between 1 and 10.",
            )
            return

        self.n = n
        self.m = m

        for w in self.matrix_area.winfo_children():
            w.destroy()

        # Two-column layout keeps the common 4x3 case compact.
        columns = tk.Frame(self.matrix_area, bg=BG)
        columns.pack(fill="x")

        columns.grid_columnconfigure(0, weight=1, uniform="matrix")
        columns.grid_columnconfigure(1, weight=1, uniform="matrix")

        allocation_card, allocation_body = self.section_card(
            columns,
            "RESOURCE ALLOCATION",
            "Resources currently held by each process.",
        )
        allocation_card.grid(
            row=0, column=0, sticky="nsew", padx=(0, 6), pady=(0, 10)
        )

        request_card, request_body = self.section_card(
            columns,
            "RESOURCE REQUESTS",
            "Additional resources each process is requesting.",
        )
        request_card.grid(
            row=0, column=1, sticky="nsew", padx=(6, 0), pady=(0, 10)
        )

        self.allocation_entries = self.create_matrix(
            allocation_body, n, m
        )
        self.request_entries = self.create_matrix(
            request_body, n, m
        )

        # Available Resources card
        available_card = self.card(columns)
        available_card.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(0, 10),
        )

        available_inner = tk.Frame(available_card, bg=CARD)
        available_inner.pack(fill="x", padx=18, pady=14)

        tk.Label(
            available_inner,
            text="AVAILABLE RESOURCES",
            bg=CARD,
            fg=TEXT,
            font=(FONT, 11, "bold"),
        ).pack(anchor="w")

        tk.Label(
            available_inner,
            text="Resources that are currently free.",
            bg=CARD,
            fg=MUTED,
            font=(FONT, 9),
        ).pack(anchor="w", pady=(2, 10))

        self.available_entries = self.create_available(
            available_inner, m
        )

        self.clear_result()

        self.canvas.yview_moveto(0)

    def clear_inputs(self):
        """Reset all matrix/resource fields to zero and clear the result."""
        for rows in (self.allocation_entries, self.request_entries):
            for row in rows:
                for entry in row:
                    entry.delete(0, "end")
                    entry.insert(0, "0")

        for entry in self.available_entries:
            entry.delete(0, "end")
            entry.insert(0, "0")

        self.last_output = ""
        self.clear_result()

        if hasattr(self, "backend_status"):
            self.backend_status.config(
                text="● Backend ready",
                fg=SAFE,
            )

    # ========================================================
    # INPUT + C INTEGRATION
    # ========================================================

    def read_matrix(self, matrix_entries, name):
        matrix = []

        for i, row in enumerate(matrix_entries):
            values = []

            for j, entry in enumerate(row):
                raw = entry.get().strip()

                if not raw:
                    raise ValueError(
                        f"{name}: P{i+1}, R{j+1} is empty."
                    )

                try:
                    value = int(raw)
                except ValueError:
                    raise ValueError(
                        f"{name}: P{i+1}, R{j+1} must be an integer."
                    )

                if value < 0:
                    raise ValueError(
                        f"{name}: P{i+1}, R{j+1} cannot be negative."
                    )

                values.append(value)

            matrix.append(values)

        return matrix

    def read_available(self):
        values = []

        for j, entry in enumerate(self.available_entries):
            raw = entry.get().strip()

            if not raw:
                raise ValueError(f"Available R{j+1} is empty.")

            try:
                value = int(raw)
            except ValueError:
                raise ValueError(
                    f"Available R{j+1} must be an integer."
                )

            if value < 0:
                raise ValueError(
                    f"Available R{j+1} cannot be negative."
                )

            values.append(value)

        return values

    def make_c_input(self, allocation, request, available):
        # This order exactly matches detection.c:
        # n, m, allocation matrix, request matrix, available resources.
        lines = [
            str(self.n),
            str(self.m),
        ]

        for row in allocation:
            lines.append(" ".join(str(x) for x in row))

        for row in request:
            lines.append(" ".join(str(x) for x in row))

        lines.append(" ".join(str(x) for x in available))

        return "\n".join(lines) + "\n"

    def detect(self):
        if not self.n or not self.m:
            messagebox.showwarning(
                "Create a system first",
                "Enter the number of processes and resources, "
                "then click Create System.",
            )
            return

        if not C_EXE.exists():
            messagebox.showerror(
                "C backend not found",
                f"Could not find:\n\n{C_EXE}\n\n"
                "Compile detection.c as detection.exe and put it "
                "in the same folder as gui.py.",
            )
            return

        try:
            allocation = self.read_matrix(
                self.allocation_entries,
                "Allocation",
            )

            request = self.read_matrix(
                self.request_entries,
                "Request",
            )

            available = self.read_available()

            c_input = self.make_c_input(
                allocation,
                request,
                available,
            )

            self.backend_status.config(
                text="● Running detection...",
                fg=ACCENT,
            )
            self.update_idletasks()

            output = self.run_detection(c_input)
            self.last_output = output

            self.backend_status.config(
                text="● Backend ready",
                fg=SAFE,
            )

            self.show_result(output)

        except ValueError as exc:
            messagebox.showerror(
                "Check your input",
                str(exc),
            )

        except RuntimeError as exc:
            self.backend_status.config(
                text="● Backend ready",
                fg=SAFE,
            )
            messagebox.showerror(
                "Detection failed",
                str(exc),
            )

    def run_detection(self, input_text):
        kwargs = dict(
            input=input_text,
            text=True,
            capture_output=True,
            timeout=10,
            cwd=str(BASE_DIR),
        )

        # Prevent a console window from appearing on Windows.
        if os.name == "nt":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            kwargs["startupinfo"] = startupinfo
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW

        try:
            result = subprocess.run(
                [str(C_EXE)],
                **kwargs,
            )
        except FileNotFoundError:
            raise RuntimeError(
                f"Detection backend not found:\n{C_EXE}"
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError(
                "The detection engine timed out."
            )

        if result.returncode != 0:
            details = result.stderr.strip()

            if not details:
                details = result.stdout.strip()

            raise RuntimeError(
                "The C detection program returned an error.\n\n"
                + (details or "Unknown error.")
            )

        return result.stdout

    # ========================================================
    # RESULT UI
    # ========================================================

    def build_result_area(self):
        self.result_area = tk.Frame(self.content, bg=BG)
        self.result_area.pack(fill="x", pady=(0, 20))

        self.clear_result()

    def clear_result(self):
        for w in self.result_area.winfo_children():
            w.destroy()

    def parse_output(self, output):
        is_safe = "SYSTEM IS SAFE" in output
        is_deadlock = "DEADLOCK DETECTED" in output

        sequence = []
        deadlocked = []

        if is_safe:
            match = re.search(
                r"Safe Sequence:\s*(?:\n\s*)?(.+)",
                output,
            )

            if match:
                sequence = re.findall(
                    r"P\d+",
                    match.group(1),
                )

        if is_deadlock:
            match = re.search(
                r"Deadlocked Processes:\s*(?:\n\s*)?(.+)",
                output,
            )

            if match:
                deadlocked = re.findall(
                    r"P\d+",
                    match.group(1),
                )

        return is_safe, is_deadlock, sequence, deadlocked

    def show_result(self, output):
        self.clear_result()

        safe, deadlock, sequence, deadlocked = self.parse_output(
            output
        )

        card = self.card(self.result_area)
        card.pack(fill="x")

        inner = tk.Frame(card, bg=CARD)
        inner.pack(fill="x", padx=20, pady=17)

        tk.Label(
            inner,
            text="DETECTION RESULT",
            bg=CARD,
            fg=MUTED,
            font=(FONT, 9, "bold"),
        ).pack(anchor="w")

        if safe:
            self.show_safe_result(
                inner,
                sequence,
            )

        elif deadlock:
            self.show_deadlock_result(
                inner,
                deadlocked,
            )

        else:
            tk.Label(
                inner,
                text="The backend returned a result that could not "
                     "be interpreted.",
                bg=CARD,
                fg=WARN,
                font=(FONT, 10, "bold"),
            ).pack(anchor="w", pady=(12, 8))

        actions = tk.Frame(inner, bg=CARD)
        actions.pack(fill="x", pady=(15, 0))

        ttk.Button(
            actions,
            text="View Detection Steps",
            style="Secondary.TButton",
            command=self.show_steps,
        ).pack(side="left")

        ttk.Button(
            actions,
            text="Run Detection Again",
            style="Primary.TButton",
            command=self.detect,
        ).pack(side="right")

        # Bring the result into view automatically.
        self.after(
            100,
            lambda: self.canvas.yview_moveto(1.0),
        )

    def show_safe_result(self, parent, sequence):
        box = tk.Frame(parent, bg=SAFE_BG)
        box.pack(fill="x", pady=(11, 14))

        tk.Label(
            box,
            text="✓",
            bg=SAFE_BG,
            fg=SAFE,
            font=(FONT, 20, "bold"),
        ).pack(side="left", padx=(17, 10), pady=11)

        tk.Label(
            box,
            text="SYSTEM IS SAFE",
            bg=SAFE_BG,
            fg=SAFE,
            font=(FONT, 13, "bold"),
        ).pack(side="left", pady=11)

        tk.Label(
            parent,
            text="Safe sequence",
            bg=CARD,
            fg=MUTED,
            font=(FONT, 9, "bold"),
        ).pack(anchor="w")

        sequence_text = "  →  ".join(sequence) if sequence else "Unavailable"

        tk.Label(
            parent,
            text=sequence_text,
            bg="#F7F8FA",
            fg=TEXT,
            font=(FONT, 12, "bold"),
            anchor="w",
            padx=14,
            pady=12,
        ).pack(fill="x", pady=(5, 0))

    def show_deadlock_result(self, parent, deadlocked):
        box = tk.Frame(parent, bg=DANGER_BG)
        box.pack(fill="x", pady=(11, 14))

        tk.Label(
            box,
            text="!",
            bg=DANGER_BG,
            fg=DANGER,
            font=(FONT, 20, "bold"),
        ).pack(side="left", padx=(19, 13), pady=11)

        tk.Label(
            box,
            text="DEADLOCK DETECTED",
            bg=DANGER_BG,
            fg=DANGER,
            font=(FONT, 13, "bold"),
        ).pack(side="left", pady=11)

        tk.Label(
            parent,
            text="Deadlocked processes",
            bg=CARD,
            fg=MUTED,
            font=(FONT, 9, "bold"),
        ).pack(anchor="w")

        text = ", ".join(deadlocked) if deadlocked else "Unavailable"

        tk.Label(
            parent,
            text=text,
            bg=CARD,
            fg=TEXT,
            font=(FONT, 12, "bold"),
        ).pack(anchor="w", pady=(5, 0))

    # ========================================================
    # STEP-BY-STEP VIEW
    # ========================================================

    def show_steps(self):
        if not self.last_output:
            return

        win = tk.Toplevel(self)
        win.title("Detection Steps")
        win.geometry("820x650")
        win.minsize(700, 500)
        win.configure(bg=BG)
        win.transient(self)

        header = tk.Frame(win, bg=BG)
        header.pack(fill="x", padx=25, pady=(22, 8))

        tk.Label(
            header,
            text="Detection Steps",
            bg=BG,
            fg=TEXT,
            font=(FONT, 18, "bold"),
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Step-by-step output from the C detection engine",
            bg=BG,
            fg=MUTED,
            font=(FONT, 9),
        ).pack(anchor="w", pady=(3, 0))

        card = self.card(win)
        card.pack(fill="both", expand=True, padx=25, pady=(8, 22))

        frame = tk.Frame(card, bg=CARD)
        frame.pack(fill="both", expand=True, padx=14, pady=14)

        scroll = ttk.Scrollbar(frame)
        scroll.pack(side="right", fill="y")

        text = tk.Text(
            frame,
            bg="#FBFCFD",
            fg=TEXT,
            font=("Consolas", 10),
            relief="flat",
            bd=0,
            wrap="none",
            padx=13,
            pady=12,
            yscrollcommand=scroll.set,
        )
        text.pack(fill="both", expand=True)

        scroll.configure(command=text.yview)

        text.insert("1.0", self.last_output)
        text.configure(state="disabled")


if __name__ == "__main__":
    app = DeadlockGUI()
    app.mainloop()
