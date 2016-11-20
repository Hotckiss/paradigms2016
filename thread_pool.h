#pragma once
#include <pthread.h>
struct node {
    struct node* next;
    struct node* prev;
};
struct queue {
    struct node head;
    int size;
};
struct wsqueue {
    struct queue queue;
    pthread_mutex_t mutex;
    pthread_cond_t cond;
};
typedef struct thread_pool {
    pthread_t* threads;
    int t;
    struct wsqueue queue;
} thread_pool_t;

typedef struct task {
    struct node node;
    void (*f)(void*);
    void* args;
    int done;
    struct task* c[2]; 
    thread_pool_t* pool;
    pthread_mutex_t mutex;
    pthread_cond_t cond;
} task_t;

typedef struct task_args {
    int len;
    int depth;
    int* mas;
} task_args_t;

task_t* task_init(thread_pool_t* pool, void (*f)(void*), void* args);
void thpool_init(thread_pool_t* pool, int t);
void thpool_submit(thread_pool_t* pool, task_t* task);
void thpool_wait(task_t* task);
void thpool_finit(thread_pool_t* pool);

