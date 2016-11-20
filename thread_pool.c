#include "thread_pool.h"
#include <stdlib.h>
#include <string.h>
static volatile int cont = 1;

static struct node* pop(struct queue* queue)  {
    if (queue->size == 0) return NULL;
    struct node* N = queue->head.prev;
    N->prev->next = N->next;
    N->next->prev = N->prev;
    queue->size--;
    return N;
}
static void push(struct wsqueue* queue, struct node* node) {
    pthread_mutex_lock(&queue->mutex);
    node->prev = &queue->queue.head;
    node->next = queue->queue.head.next;
    node->prev->next = node;
    node->next->prev = node;
    queue->queue.size++;
    pthread_cond_signal(&queue->cond);
    pthread_mutex_unlock(&queue->mutex);
}
static void* go(void* data) {
    struct wsqueue* queue = (struct wsqueue*)(data);
    while (cont == 1 || queue->queue.size > 0) {
	pthread_mutex_lock(&queue->mutex);
	while (cont == 1 && queue->queue.size == 0)
	    pthread_cond_wait(&queue->cond, &queue->mutex);
	//-------
	struct node* node = pop(&queue->queue);
	//------
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
void thpool_init(thread_pool_t* pool, int t) {
    pool->queue.queue.head.next = &pool->queue.queue.head;
    pool->queue.queue.head.prev = &pool->queue.queue.head;
    pool->queue.queue.size = 0;
    pthread_mutex_init(&pool->queue.mutex, NULL);
    pthread_cond_init(&pool->queue.cond, NULL);
    int i = 0;
    pool->threads = malloc(t * sizeof(pthread_t));
    pool->t = t;
    for (; i < t; i++)
        pthread_create(&pool->threads[i], NULL, go, &pool->queue);
}
void thpool_submit(thread_pool_t* pool, task_t* task) {
    push(&pool->queue, (struct node*)(task));
}
void thpool_wait(task_t* task) {
    if (task == NULL) return;
    pthread_mutex_lock(&task->mutex);
    while (!task->done)
	pthread_cond_wait(&task->cond, &task->mutex);
    pthread_mutex_unlock(&task->mutex);
}
void thpool_finit(thread_pool_t* pool) {
    int i = 0;
    pthread_mutex_lock(&pool->queue.mutex);
    cont = 0;
    pthread_cond_broadcast(&pool->queue.cond);
    pthread_mutex_unlock(&pool->queue.mutex);
    for (; i < pool->t; i++)
    	pthread_join(pool->threads[i], NULL);
    pthread_mutex_destroy(&pool->queue.mutex);
    pthread_cond_destroy(&pool->queue.cond);
    free(pool->threads);
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
