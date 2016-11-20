#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include "thread_pool.h"
int rec_lim = 0;
static int comp(const void* a, const void* b) {
    return *((int*)a) - *((int*)b);
}
static void swap(int* a, int *b){
    int tmp = *a;
    *a = *b;
    *b = tmp;
}
void sort(void* data) {
    task_t* task = (task_t*)(data);
    task_args_t* args = (task_args_t*)(task->args);
    if (args->depth == rec_lim) {
	qsort(args->mas, args->len, sizeof(int), comp);
	return;
    }	
    if (args->len <= 1) return;
    int x = args->mas[rand() % args->len];
    int l = 0, r = args->len;
    while(l < r) {
	while(args->mas[l] <= x) l++;
	while(args->mas[r] > x) r--;
	if(l < r) swap(&(args->mas[l]), &(args->mas[r])), l++, r--;
    }
    //--------------------------------------------------------
    struct task_args* a1 = (struct task_args*)malloc(sizeof(struct task_args));
    a1->len = l;
    a1->depth = args->depth + 1;
    a1->mas = args->mas;
    //------------------------
    struct task_args* a2 = (struct task_args*)malloc(sizeof(struct task_args));
    a2->len = args->len - l;
    a2->depth = args->depth + 1;
    a2->mas = args->mas + l;
    //------------------------------------------
    task_t* t1 = task_init(task->pool, sort, (void*)a1);
    task_t* t2 = task_init(task->pool, sort, (void*)a2);
    task->c[0] = t1;
    task->c[1] = t2;
    thpool_submit(task->pool, t1);
    thpool_submit(task->pool, t2);
}
static void f(task_t* task) {
    int i = 0;
    if (task == NULL) return;
    thpool_wait(task);
    for(; i < 2; i++) f(task->c[i]);
    free(task->args);
    free(task);
}
int main(int argc, char* argv[]) {
    //double tt = clock();
    int t = atoi(argv[1]);
    int n = atoi(argv[2]);
    rec_lim = atoi(argv[3]);
    int i = 0;
    srand(30);
    int* mas = malloc(n * sizeof(int));
    for (; i < n; i++)
	mas[i] = rand() % 15 + 10;
    //for (i = 0; i < n; i++)
    //	printf("%d ", mas[i]);
    //printf("\n");
    thread_pool_t pool;
    thpool_init(&pool, t);
    struct task_args* a = (struct task_args*)malloc(sizeof(struct task_args));
    a->len = n;
    a->depth = 0;
    a->mas = mas;
    task_t* task = task_init(&pool, sort, (void*)a);
    thpool_submit(&pool, task);
    f(task);
    thpool_finit(&pool);
    //for (i = 0; i < n; i++)
    //	printf("%d ", mas[i]);
    //printf("\n");
    free(mas);
    //fprintf(stderr, "%.6lf\n", (clock() - t) / CLOCKS_PER_SEC);
    pthread_exit(NULL);
    //fprintf(stderr, "%.6lf\n", (clock() - t) / CLOCKS_PER_SEC);
    return 0;
}
