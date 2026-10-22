#define RECOVERY_ENGINE_BUILD
#include "recovery_engine.h"

int recovery_apply(int process_count, int resource_count, int method, int process, int resource,
                   int *allocation, int *request, int *available,
                   int *active, int *released) {
    int resource_type, released_count = 0;
    if (process_count < 1 || process_count > RECOVERY_MAX_PROCESSES ||
        resource_count < 1 || resource_count > RECOVERY_MAX_RESOURCES ||
        !allocation || !request || !available || !active || !released ||
        process < 0 || process >= process_count || !active[process]) return -1;

    /* Termination releases every resource held by the process. */
    if (method == 0) {
        for (resource_type = 0; resource_type < resource_count; ++resource_type) {
            int cell = process * resource_count + resource_type;
            available[resource_type] += allocation[cell];
            released_count += allocation[cell];
            allocation[cell] = 0;
            request[cell] = 0;
        }
        active[process] = 0;
    /* Preemption returns one instance of the selected resource type. */
    } else if (method == 1) {
        int cell;
        if (resource < 0 || resource >= resource_count) return -1;
        cell = process * resource_count + resource;
        if (allocation[cell] < 1) return -1;
        --allocation[cell];
        ++available[resource];
        if (request[cell] > 0) --request[cell];
        released_count = 1;
    } else {
        return -1;
    }

    *released = released_count;
    return 0;
}

int recovery_choose_victim(int process_count, int resource_count, const int *allocation,
                           const int *candidates, int candidate_count) {
    int best_process = -1, fewest_held = 0, candidate, resource_type;
    if (process_count < 1 || process_count > RECOVERY_MAX_PROCESSES ||
        resource_count < 1 || resource_count > RECOVERY_MAX_RESOURCES ||
        !allocation || !candidates || candidate_count < 1 || candidate_count > process_count)
        return -1;

    for (candidate = 0; candidate < candidate_count; ++candidate) {
        int process = candidates[candidate], held_instances = 0;
        if (process < 0 || process >= process_count) return -1;
        for (resource_type = 0; resource_type < resource_count; ++resource_type) {
            int held = allocation[process * resource_count + resource_type];
            if (held < 0) return -1;
            held_instances += held;
        }
        if (best_process < 0 || held_instances < fewest_held ||
            (held_instances == fewest_held && process > best_process)) {
            best_process = process;
            fewest_held = held_instances;
        }
    }
    return best_process;
}
