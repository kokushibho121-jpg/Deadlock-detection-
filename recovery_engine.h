#ifndef RECOVERY_ENGINE_H
#define RECOVERY_ENGINE_H

#ifdef _WIN32
#  ifdef RECOVERY_ENGINE_BUILD
#    define RECOVERY_API __declspec(dllexport)
#  else
#    define RECOVERY_API __declspec(dllimport)
#  endif
#else
#  define RECOVERY_API __attribute__((visibility("default")))
#endif

#ifdef __cplusplus
extern "C" {
#endif

#define RECOVERY_MAX_PROCESSES 32
#define RECOVERY_MAX_RESOURCES 16

/* Apply method 0 (terminate) or 1 (preempt one instance) to the simulated state. */
RECOVERY_API int recovery_apply(int process_count, int resource_count, int method,
    int process, int resource, int *allocation, int *request,
    int *available, int *active, int *released);

/* Return the selected process holding the fewest instances, or -1 on error. */
RECOVERY_API int recovery_choose_victim(int process_count, int resource_count,
    const int *allocation, const int *candidates, int candidate_count);

#ifdef __cplusplus
}
#endif
#endif
