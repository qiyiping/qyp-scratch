#include "two_bottle_puzzle.h"

/**
 * Simple queue implementation
 */
typedef struct _queue {
  int *q;
  int front;
  int end;
  int size;
} queue;

queue *create_queue(int n) {
  queue* q = (queue *) malloc(sizeof(queue));
  q->front = 0;
  q->end = 0;
  q->size = n+1;
  q->q = (int *)malloc(q->size * sizeof(int));
  return q;
}

void destroy_queue(queue *q) {
  free(q->q);
  free(q);
}

bool push(queue *q, int i) {
  int next = (q->front + 1) % q->size;
  if (next == q->end) return false;
  q->q[next] = i;
  q->front = next;
  return true;
}

bool pop(queue *q, int *i) {
  if (q->front == q->end) return false;
  int idx = (q->end + 1) % q->size;
  *i = q->q[idx];
  q->end = idx;
  return true;
}

/**
 * state definition
 */
typedef struct _state {
  int action;
  int prev_state_index;
  bool visited;
} state;

static char action_table[6][30] = {
  "fill x",
  "fill y",
  "empty x",
  "empty y",
  "move x to y",
  "move y to x"
};

void print_actions(state *t, int a, int i) {
  if (t[i].prev_state_index < 0) {
    printf("initial state => x: %d, y: %d\n", i%(a+1), i/(a+1));
  } else {
    print_actions(t, a, t[i].prev_state_index);
    printf("%s => x: %d, y: %d\n", action_table[t[i].action], i%(a+1), i/(a+1));
  }
}


/**
 * breadth-first search
 */
bool solve(int a, int b, int c, bool print) {
  state *t = (state *)malloc((a+1) * (b+1) * sizeof(state));
  for (int i = 0; i < (a+1) * (b+1); ++i) {
    t[i].visited = false;
  }
  queue *q = create_queue((a+1) * (b+1));
  push(q, 0);
  t[0].visited = true;
  t[0].action = -1;
  t[0].prev_state_index = -1;

  bool found = false;
  int i;
  int *next_state = (int *)malloc(6 * sizeof(int));
  while(pop(q, &i)) {
    int x = i%(a+1);
    int y = i/(a+1);
    if (y == c || x == c) {
      if (print) {
        print_actions(t, a, i);
      }
      found = true;
      break;
    }

    // fill x ==> (a, y)
    next_state[0] = y*(a+1) + a;;
    // fill y ==> (x, b)
    next_state[1] = b*(a+1) + x;
    // empty x ==> (0, y)
    next_state[2] = y*(a+1);
    // empty y ==> (x, 0)
    next_state[3] = x;
    // move x to y ==> d = min((b-y), x) (x-d, y+d)
    int d = (b-y <= x)? b-y:x;
    next_state[4] = (y+d)*(a+1) + x-d;
    // move y to x ==> d = min(a-x, y) (x+d, y-d)
    d = (a-x <= y)? a-x:y;
    next_state[5] = (y-d)*(a+1) + x+d;

    for(int j = 0; j < 6; ++j) {
      if (!t[next_state[j]].visited) {
        t[next_state[j]].visited = true;
        t[next_state[j]].prev_state_index = i;
        t[next_state[j]].action = j;
        push(q, next_state[j]);
      }
    }
  }

  free(t);
  free(next_state);
  destroy_queue(q);

  return found;
}
