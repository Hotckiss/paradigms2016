#pragma once
#include <pthread.h>

typedef struct node {
    struct node* next;
    struct node* prev;
} node_t;

typedef struct queue {
    node_t head;
    int size;
} queue_t;

typedef struct wsqueue {
    queue_t queue;
    pthread_mutex_t mutex;
    pthread_cond_t cond;
} wsqueue_t;

node_t* queue_pop(queue_t* queue);
void wsqueue_init(wsqueue_t* queue);
void wsqueue_push(wsqueue_t* queue, node_t* node);
inline int wsqueue_size(wsqueue_t* queue);
void wsqueue_finit(wsqueue_t* queue);
void wsqueue_notify_all(wsqueue_t* queue);

