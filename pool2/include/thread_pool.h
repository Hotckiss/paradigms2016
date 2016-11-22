#pragma once
#include <pthread.h>

#include "wsqueue.h"

typedef struct thread_pool {
    pthread_t* threads;
    int t;
    wsqueue_t queue;
} thread_pool_t;

typedef struct task {
    node_t node;
    void (*f)(void*);
    void* args;
    int done;
    struct task* c[2];
    thread_pool_t* pool;
    pthread_mutex_t mutex;
    pthread_cond_t cond;
} task_t;

task_t* task_init(thread_pool_t* pool, void (*f)(void*), void* args);
void thpool_init(thread_pool_t* pool, int t);
void thpool_submit(thread_pool_t* pool, task_t* task);
void thpool_wait(task_t* task);
void thpool_finit(thread_pool_t* pool);


