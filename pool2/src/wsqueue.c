#include "wsqueue.h"

void queue_init(queue_t* queue) {
    queue->head.next = &queue->head;
    queue->head.prev = &queue->head;
    queue->size = 0;
}
void queue_push(queue_t* queue, node_t* node) {
    node->prev = &queue->head;
    node->next = queue->head.next;
    node->prev->next = node;
    node->next->prev = node;
    queue->size++;
}
int queue_size(queue_t* queue) { return queue->size; }
node_t* queue_pop(queue_t* queue) {
    if (!queue_size(queue)) return NULL;
    node_t* node = queue->head.prev;
    node->prev->next = node->next;
    node->next->prev = node->prev;
    queue->size--;
    return node;
}
void wsqueue_init(wsqueue_t* queue) {
    queue_init(&queue->queue);
    pthread_mutex_init(&queue->mutex, NULL);
    pthread_cond_init(&queue->cond, NULL);
}
void wsqueue_push(wsqueue_t* queue, node_t* node) {
    pthread_mutex_lock(&queue->mutex);
    queue_push(&queue->queue, node);
    pthread_cond_signal(&queue->cond);
    pthread_mutex_unlock(&queue->mutex);
}
int wsqueue_size(wsqueue_t* queue) { return queue_size(&queue->queue); }
void wsqueue_finit(wsqueue_t* queue) {
    pthread_mutex_destroy(&queue->mutex);
    pthread_cond_destroy(&queue->cond);
}
void wsqueue_notify_all(wsqueue_t* queue) {
    pthread_mutex_lock(&queue->mutex);
    pthread_cond_broadcast(&queue->cond);
    pthread_mutex_unlock(&queue->mutex);
}
