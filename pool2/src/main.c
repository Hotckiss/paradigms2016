#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include "thread_pool.h"

static int rec_lim = 0;

typedef struct args {
    int* mas;
    int len;
    int depth;
} task_args_t;

static task_args_t* make(int* mas, int len, int depth) {
    task_args_t* task = malloc(sizeof(task_args_t));
    task->mas = mas;
    task->len = len;
    task->depth = depth;
    return task;
}
static int comp(const void* a, const void* b) {
    int* pa = (int*)(a);
    int* pb = (int*)(b);
    return (*pa) - (*pb);
}
void sort(void* data) {
    task_t* task = (task_t*)(data);
    task_args_t* args = (task_args_t*)(task->args);
    if (args->len <= 1) return;
    if (args->depth == rec_lim) {
        qsort(args->mas, args->len, sizeof(int), comp);
        return;
    }
    int x = args->mas[args->len >> 1];
    int l = 0, r = args->len - 1, i=0;
    while (l <= r) {
        while (args->mas[l] < x) l++;
        while (args->mas[r] > x) r--;
        if(l <= r) {
            if (args->mas[l] > args->mas[r]) {
                int tmp = args->mas[l];
                args->mas[l] = args->mas[r];
                args->mas[r] = tmp;
            }
            l++;
            r--;
        }
    }
    task_args_t* a1 = make(args->mas, l, args->depth + 1);
    task_args_t* a2 = make(args->mas + l, args->len - l, args->depth + 1);
    task->c[0] = (task_t*)task_init(task->pool, sort, (void*)(a1));
    task->c[1] = (task_t*)task_init(task->pool, sort, (void*)(a2));
    thpool_submit(task->pool, task->c[0]);
    thpool_submit(task->pool, task->c[1]);
}
static void tree_go(task_t* task) {
    if (task == NULL) return;
    int i;
    thpool_wait(task);
    for(i = 0; i < 2; i++) tree_go(task->c[i]);
    free(task->args);
    free(task);
}
int main(int argc, char* argv[]) {
    int t = atoi(argv[1]);
    int n = atoi(argv[2]);
    rec_lim = atoi(argv[3]);
    int i = 0;
    srand(30);
    int* mas = malloc(sizeof(int) * n);
    for (; i < n; i++)
        mas[i] = rand() % 15  + 10;
    thread_pool_t pool;
    thpool_init(&pool, t);
    task_t* task = task_init(&pool, sort, (void*)(make(mas, n, 0)));
    thpool_submit(&pool, task);
    tree_go(task);
    // check
    for (i = 0; i < n - 1; i++) if (mas[i] > mas[i + 1]) return 1;

    thpool_finit(&pool);
    free(mas);
    pthread_exit(NULL);
    return 0;
}
