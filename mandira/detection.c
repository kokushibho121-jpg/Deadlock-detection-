#include <stdio.h>
#define MAX_PROCESSES 10
#define MAX_RESOURCES 5

typedef struct{
    int p_id;
    int allocation[MAX_RESOURCES];
    int request[MAX_RESOURCES];
} process;

int canfinish(process p, int work[], int resources){
    for(int j = 0; j < resources; j++)
    {
        if(p.request[j] > work[j])
        {
            return 0;
        }
    }
    return 1;
}
void printArray(int arr[], int size){
    for(int i = 0; i < size; i++)
    {
        printf("%d ", arr[i]);
    }
    printf("\n");
}


int main()
{
    int n, m;
    process processes[MAX_PROCESSES];
    int available[MAX_RESOURCES];
    int work[MAX_RESOURCES];
    int finish[MAX_PROCESSES];

    int safe_sequence[MAX_PROCESSES];
    int safe_count = 0;

    int found;
    printf("Enter number of processes:");
    scanf("%d", &n);

    printf("Enter number of resources:");
    scanf("%d", &m);

    if(n <= 0 || n > MAX_PROCESSES){
        printf("Invalid number of processes\n");
        return 1;
    }

    if(m <= 0 || m > MAX_RESOURCES){
        printf("Invalid number of resources\n");
        return 1;
    }

    for(int i = 0; i < n; i++){
        processes[i].p_id = i + 1;
    }

    printf("\nEnter Allocation Matrix:\n");

    for(int i = 0; i < n; i++){
        printf("P%d: ", processes[i].p_id);

        for(int j = 0; j < m; j++){
            scanf("%d", &processes[i].allocation[j]);

            if(processes[i].allocation[j] < 0){
                printf("Invalid allocation value.\n");
                return 1;
            }
        }
    }

    printf("\nEnter Request Matrix:\n");

    for(int i = 0; i < n; i++){
        printf("P%d: ", processes[i].p_id);

        for(int j = 0; j < m; j++){
            scanf("%d", &processes[i].request[j]);

            if(processes[i].request[j] < 0){
                printf("Invalid request value.\n");
                return 1;
            }
        }
    }

    printf("\nEnter Available Resources:\n");

    for(int j = 0; j < m; j++)
    {
        scanf("%d", &available[j]);

        if(available[j] < 0)
        {
            printf("Invalid available resource.\n");
            return 1;
        }
    }
    for(int j = 0; j < m; j++)
    {
        work[j] = available[j];
    }

    for(int i = 0; i < n; i++)
    {
        finish[i] = 0;
    }


    printf("\n");
    printf("DEADLOCK DETECTION\n");
    printf("\n");

    printf("\nInitial Work: ");
    printArray(work, m);


    do{
        found = 0;
        for(int i = 0; i < n; i++){
            if(finish[i] == 0){
                printf("\nChecking P%d...\n", processes[i].p_id);

                printf("Request: ");
                printArray(processes[i].request, m);

                printf("Work:    ");
                printArray(work, m);


                if(canfinish(processes[i], work, m)){
                    printf("P%d CAN FINISH\n", processes[i].p_id);

                    safe_sequence[safe_count] = i;
                    safe_count++;

                    for(int j = 0; j < m; j++){
                        work[j] =
                            work[j] + processes[i].allocation[j];
                    }
                    finish[i] = 1;
                    found = 1;
                    printf("Updated Work: ");
                    printArray(work, m);
                }
                else{
                    printf("P%d CANNOT FINISH\n", processes[i].p_id);
                }
            }
        }

    } while(found == 1);
    printf("\n");
    printf("FINAL RESULT\n");
    printf("\n");


    if(safe_count == n){
        printf("\nSYSTEM IS SAFE\n");
        printf("\nSafe Sequence:\n");

        for(int i = 0; i < n; i++){
            printf("P%d", processes[safe_sequence[i]].p_id);

            if(i != n - 1){
                printf(" -> ");
            }
        }

        printf("\n");
    }
    else{
        printf("\nDEADLOCK DETECTED\n");
        printf("\nDeadlocked Processes:\n");

        for(int i = 0; i < n; i++){
            if(finish[i] == 0){
                printf("P%d ", processes[i].p_id);
            }
        }

        printf("\n");
    }


    return 0;
}
