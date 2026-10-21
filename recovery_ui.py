"""Streamlit screens for the Recovery module."""
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from recovery_state import MAX_PROCESSES, MAX_RESOURCES, SystemState, validate_state


def state_editor():
    left, right = st.columns(2)
    p = left.number_input("Processes", 1, MAX_PROCESSES, 4, key="process_count")
    r = right.number_input("Resource types", 1, MAX_RESOURCES, 3, key="resource_count")
    processes = [f"P{i + 1}" for i in range(p)]
    resources = [f"R{i + 1}" for i in range(r)]
    zeros = [[0] * r for _ in range(p)]

    with st.form("recovery_state_form"):
        st.caption("Enter allocated resources, requests, and available instances.")
        left, right = st.columns(2)
        with left:
            st.write("Allocation")
            allocation = st.data_editor(pd.DataFrame(zeros, index=processes, columns=resources),
                                        key=f"allocation_{p}_{r}", num_rows="fixed", width="stretch")
        with right:
            st.write("Requests")
            request = st.data_editor(pd.DataFrame(zeros, index=processes, columns=resources),
                                     key=f"request_{p}_{r}", num_rows="fixed", width="stretch")
        available = st.data_editor(pd.DataFrame([[0] * r], index=["Available"], columns=resources),
                                   key=f"available_{p}_{r}", num_rows="fixed", width="stretch")
        submitted = st.form_submit_button("Use this system", type="primary")

    if not submitted:
        return None

    def numbers(table):
        result = []
        for row in table.to_numpy().tolist():
            values = [float(value) for value in row]
            if any(value < 0 or not value.is_integer() for value in values):
                raise ValueError("Enter non-negative whole numbers.")
            result.append([int(value) for value in values])
        return result

    try:
        state = SystemState(numbers(allocation), numbers(request), numbers(available)[0], [1] * p)
        validate_state(state)
        return state
    except (ValueError, TypeError, OverflowError) as error:
        st.error(str(error))
        return None


def render_graph(state: SystemState):
    processes = [i for i, active in enumerate(state.active) if active]
    resources = list(range(state.resource_count))
    positions = {}

    for names, x in (([f"P{i + 1}" for i in processes], 0),
                     ([f"R{i + 1}\nfree: {state.available[i]}" for i in resources], 1)):
        for index, name in enumerate(names):
            y = 0 if len(names) == 1 else 1 - 2 * index / (len(names) - 1)
            positions[name] = (x, y)

    fig, ax = plt.subplots(figsize=(7, max(3.5, max(len(processes), len(resources)) * .8)))
    for i in processes:
        x, y = positions[f"P{i + 1}"]
        ax.scatter(x, y, s=1400, color="#dceafe", edgecolor="#3573bd", zorder=2)
        ax.text(x, y, f"P{i + 1}", ha="center", va="center", zorder=3)
    for i in resources:
        name = f"R{i + 1}\nfree: {state.available[i]}"
        x, y = positions[name]
        ax.scatter(x, y, s=1800, marker="s", color="#dcfce7", edgecolor="#35a269", zorder=2)
        ax.text(x, y, name, ha="center", va="center", zorder=3)

    for i in processes:
        for j in resources:
            process, resource = f"P{i + 1}", f"R{j + 1}\nfree: {state.available[j]}"
            for amount, start, end, color, style, offset in (
                (state.allocation[i][j], resource, process, "#288553", "solid", .07),
                (state.request[i][j], process, resource, "#d28723", "dashed", -.07),
            ):
                if amount:
                    x1, y1 = positions[start]
                    x2, y2 = positions[end]
                    ax.annotate("", (x2, y2), (x1, y1), zorder=1,
                                arrowprops={"arrowstyle": "->", "color": color,
                                            "linestyle": style, "lw": 2, "shrinkA": 24, "shrinkB": 24})
                    ax.text((x1 + x2) / 2, (y1 + y2) / 2 + offset, str(amount), color=color, ha="center")

    ax.text(0, 1.15, "Processes", ha="center", weight="bold")
    ax.text(1, 1.15, "Resources", ha="center", weight="bold")
    ax.set(xlim=(-.3, 1.3), ylim=(-1.2, 1.35))
    ax.axis("off")
    st.pyplot(fig, width="stretch")
    plt.close(fig)
    st.caption("Solid green arrows: allocation. Dashed orange arrows: requests.")


def show_engine(engine):
    if engine.using_c:
        st.caption("Backend: C engine via ctypes")
    else:
        st.error("C engine unavailable: " + (engine.notice or "Start the x64 Visual Studio tools prompt."))
        st.stop()


def action_tab(state: SystemState, engine, history: list[dict]):
    st.subheader("Choose candidate processes")
    active = [i for i, yes in enumerate(state.active) if yes]
    names = [f"P{i + 1}" for i in active]
    selected = st.multiselect("Processes supplied for recovery", names, key="recovery_candidates")
    candidates = [int(name[1:]) - 1 for name in selected]
    if not candidates:
        st.info("Select candidate processes to enable recovery.")
        return

    method = st.segmented_control("Recovery method", ["Process termination", "Resource preemption"],
                                  default="Process termination", key="recovery_method")
    settings, comparison = st.columns(2, gap="large")
    with settings, st.container(border=True):
        st.subheader("Action settings")
        suggested = engine.select_victim(state, candidates)
        signature = (tuple(candidates), tuple(tuple(state.allocation[i]) for i in candidates))
        if st.session_state.get("recovery_suggestion_signature") != signature:
            st.session_state.pop("recovery_victim", None)
            st.session_state.recovery_suggestion_signature = signature
        st.success(f"C selected P{suggested + 1}: it holds the fewest resource instances.")
        victim_name = st.selectbox("Process to recover (change to override C)",
                                   [f"P{i + 1}" for i in candidates],
                                   index=candidates.index(suggested), key="recovery_victim")
        victim = int(victim_name[1:]) - 1
        st.metric("Instances held", sum(state.allocation[victim]))

        resource = None
        if method == "Resource preemption":
            choices = [i for i, count in enumerate(state.allocation[victim]) if count]
            if choices:
                resource = st.selectbox("Resource to preempt", choices,
                    format_func=lambda i: f"R{i + 1} · {state.allocation[victim][i]} held",
                    key="recovery_resource")
            else:
                st.warning("This process has no resource to preempt.")

        st.caption("Termination releases all held instances; preemption returns one selected instance.")
        if st.button("Apply simulated action", type="primary", disabled=(method == "Resource preemption" and resource is None)):
            before = state_data(state)
            updated, released = engine.recover(state, method, victim, resource)
            entry = {"method": method, "victim": victim, "released": released,
                     "before": before, "after": state_data(updated)}
            st.session_state.recovery_history = history + [entry]
            st.session_state.recovery_redo = []
            st.session_state.recovery_state = entry["after"]
            st.rerun()

    with comparison, st.container(border=True):
        st.subheader("Recovery comparison")
        st.dataframe(pd.DataFrame([{
            "Process": f"P{i + 1}",
            "Instances released if terminated": sum(state.allocation[i]),
            "Resource types eligible for preemption": sum(x > 0 for x in state.allocation[i]),
        } for i in candidates]), hide_index=True, width="stretch")
        st.caption("Counts only. C preselects the candidate holding the fewest instances.")


def state_data(state: SystemState):
    return {"allocation": state.allocation, "request": state.request,
            "available": state.available, "active": state.active}


def matrix_table(matrix, state):
    return pd.DataFrame(matrix, index=[f"P{i + 1}" for i in range(state.process_count)],
                        columns=[f"R{i + 1}" for i in range(state.resource_count)])


def state_tab(state: SystemState, history: list[dict]):
    graph, table = st.columns([1.1, 1], gap="large")
    with graph:
        st.subheader("Allocation graph")
        render_graph(state)
    with table:
        st.subheader("Allocation matrix")
        st.dataframe(matrix_table(state.allocation, state))
    if history:
        item = history[-1]
        st.success(f"Latest action: {item['method']} on P{item['victim'] + 1}; {item['released']} instance(s) released.")
        before, after = st.columns(2)
        for column, label, key in ((before, "Before", "before"), (after, "After", "after")):
            with column:
                st.write(label)
                st.dataframe(matrix_table(item[key]["allocation"], state))


def history_tab(history: list[dict]):
    if not history:
        st.info("Simulated actions will appear here.")
        return
    rows = [{"Attempt": i + 1, "Method": item["method"],
             "Process": f"P{item['victim'] + 1}", "Instances released": item["released"]}
            for i, item in enumerate(history)]
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")


def history_controls(history: list[dict]):
    undo, redo, reset = st.columns(3)
    if undo.button("Undo last action", disabled=not history):
        item = history[-1]
        st.session_state.recovery_state = item["before"]
        st.session_state.recovery_history = history[:-1]
        st.session_state.recovery_redo.append(item)
        st.rerun()
    if redo.button("Redo last action", disabled=not st.session_state.recovery_redo):
        item = st.session_state.recovery_redo.pop()
        st.session_state.recovery_state = item["after"]
        st.session_state.recovery_history = history + [item]
        st.rerun()
    if reset.button("Reset scenario", disabled=not history):
        st.session_state.recovery_history = []
        st.session_state.recovery_redo = []
        st.session_state.recovery_state = st.session_state.recovery_base
        st.rerun()
