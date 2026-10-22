#include<stdio.h>
#define MAX_PROCESSES 10
#define MAX_RESOURCES 5

typedef struct {
    int p_id;
    int allocation[MAX_RESOURCES];
    int request[MAX_RESOURCES];

}process;

int canfinish(process p,int work[],int resources){
    for(int j=0;j<resources;j++){
        if(p.request[j]>work[j]){
            return 0;
        }
    }
    return 1;
}

int main(){
    int n,m;

    process processes[MAX_PROCESSES];

    int available[MAX_RESOURCES];
    int work[MAX_RESOURCES];
    int finish[MAX_PROCESSES];

    int safe_sequence[MAX_PROCESSES];
    int safe_count=0;

    printf("Enter number of processes:");
    scanf("%d",&n);

    printf("Enter number of resources :");
    scanf("%d",&m);

    for(int i=0;i<n;i++){
        processes[i].p_id = i+1;
    }

    printf("\nEnter Allocation Matrix:\n");
    for(int i=0;i<n;i++){
        printf("P%d:",processes[i].p_id);
        for(int j=0;j<m;j++){
            scanf("%d",&processes[i].allocation[j]);
        }
    }
    

    printf("\nEnter Request Matrix: \n");
    for(int i=0;i<n;i++){
        printf("P%d:",processes[i].p_id);

        for(int j=0;j<m;j++){
            scanf("%d",&processes[i].request[j]);
        }
    }

    printf("\nEnter Available Resources:\n");
    for(int j=0;j<m;j++){
        scanf("%d",&available[j]);
    }

    for(int j=0;j<m;j++){
        work[j]=available[j];
    }
    for(int i=0;i<n;i++){
        finish[i]=0;
    }

    int found;
    do{
        found=0;
        for(int i=0;i<n;i++){

            if(finish[i]==0){
                if(canfinish(processes[i],work,m)){
                    safe_sequence[safe_count]=i;
                               safe_count++;
                               for(int j=0;j<m;j++){
                                work[j]= work[j]+ processes[i].allocation[j];
                               }
                               finish[i]=1;
                               found =1;

                }
            }
        }


    }while(found==1);
    
    if(safe_count==n){
        printf("--\n--");
        printf("SYSTEM IS SAFE\n");
        printf("--\n--");

        printf("Safe Sequence:");
        for(int i=0;i<n;i++){
            printf("P%d",safe_sequence[i]+1);
            if(i != n -1){
                printf(" -> ");
            }
        }
        printf("\n");
    }
    else{
        printf("--\n--");
        printf("DEADLOCK DETECTED\n");
        printf("--\n--");

        printf("Deadlock Processes:");
        for(int i =0;i<n;i++){
            if(finish[i]==0){
                printf("P%d",processes[i].p_id);
            }
        }
        printf("\n");
    }
    return 0;
}


