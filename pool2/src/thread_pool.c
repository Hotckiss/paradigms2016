#include <stdlib.h>
#include <string.h>
#include "thread_pool.h"

static volatile int cont = 1;

static void* go(void* data) {
    wsqueue_t* queue = (wsqueue_t*)(data);
    while (cont == 1 || wsqueue_size(queue) > 0) {
        pthread_mutex_lock(&queue->mutex);
        while (cont == 1 && wsqueue_size(queue) == 0)
            pthread_cond_wait(&queue->cond, &queue->mutex);
        node_t* node = queue_pop(&queue->queue);
        pthread_mutex_unlock(&queue->mutex);
        if (node != NULL) {
            task_t* task = (task_t*)(node);
            pthread_mutex_lock(&task->mutex);
            task->f((void*)(task));
            task->done = 1;
            pthread_cond_signal(&task->cond);
            pthread_mutex_unlock(&task->mutex);
        }
    }
    return NULL;
}
void thpool_init(thread_pool_t* pool, int num_t) {
    wsqueue_init(&pool->queue);
    int i;
    pool->threads = malloc(sizeof(pthread_t) * num_t);
    pool->t = num_t;
    for (i = 0; i < num_t; i++) pthread_create(&pool->threads[i], NULL, go, &pool->queue);
}
void thpool_submit(thread_pool_t* pool, task_t* task) {
    wsqueue_push(&pool->queue, (node_t*)(task));
}
void thpool_wait(task_t* task) {
    if (task == NULL) return;
    pthread_mutex_lock(&task->mutex);
    while (task->done == 0)
        pthread_cond_wait(&task->cond, &task->mutex);
    pthread_mutex_unlock(&task->mutex);
}
void thpool_finit(thread_pool_t* pool) {
    int i = 0;
    pthread_mutex_lock(&pool->queue.mutex);
    cont = 0;
    pthread_mutex_unlock(&pool->queue.mutex);
    wsqueue_notify_all(&pool->queue);
    for (; i < pool->t; i++)
        pthread_join(pool->threads[i], NULL);
    free(pool->threads);
    wsqueue_finit(&pool->queue);
}

task_t* task_init(thread_pool_t* pool, void (*f)(void*), void* args) {
    task_t* task = malloc(sizeof(task_t));
    task->pool = pool;
    task->f = f;
    task->args = args;
    task->done = 0;
    task->c[0] = NULL;
    task->c[1] = NULL;
    pthread_mutex_init(&task->mutex, NULL);
    pthread_cond_init(&task->cond, NULL);
    return task;
}

