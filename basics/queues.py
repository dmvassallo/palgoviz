"""
Queues, in the general sense.

TODO: To focus on fundamental operations of generalized queues, the initial
implementations of these queue types might not override __repr__. Eventually,
that should be fixed (and this note removed). Design decisions to accompany
implementing __repr__ might include: Should (all or some of) the queue types
support construction from an iterable? Be iterable themselves? Reversible?
Should distinct queue objects ever be equal? To objects of a different type?
"""

from abc import ABC, abstractmethod


class Queue(ABC):
    """Abstract class representing a generalized queue."""


class FifoQueue(Queue):
    """Abstract class representing a first-in first-out queue (a "queue")."""


class LifoQueue(Queue):
    """Abstract class representing a last-in first-out queue (a stack)."""


class PriorityQueue(Queue):
    """Abstract class representing a priority queue."""


class DequeFifoQueue(FifoQueue):
    """A FIFO queue (i.e., a "queue") based on a collections.deque."""


class AltDequeFifoQueue(FifoQueue):
    """
    A FIFO queue (i.e., a "queue") based on a collections.deque.

    Like DequeFifoQueue but elements move through in the other direction.
    """


class SlowFifoQueue(FifoQueue):
    """A FIFO queue (i.e., a "queue") based on a list. Linear-time dequeue."""


class BiStackFifoQueue(FifoQueue):
    """A FIFO queue (i.e., a "queue") based on two lists used as stacks."""


class SinglyLinkedListFifoQueue(FifoQueue):
    """A FIFO queue (i.e., a "queue") based on a singly linked list."""


class ListLifoQueue(LifoQueue):
    """A LIFO queue (i.e., a stack) based on a list."""


class DequeLifoQueue(LifoQueue):
    """A LIFO queue (i.e., a stack) based on a collections.deque."""


class AltDequeLifoQueue(LifoQueue):
    """
    A LIFO queue (i.e., a stack) based on a collections.deque.

    Like DequeLifoQueue but elements are pushed and popped at the other end.
    """


class SinglyLinkedListLifoQueue(LifoQueue):
    """A LIFO queue (i.e., a stack) based on a singly linked list."""


class FastEnqueueMaxPriorityQueue(PriorityQueue):
    """A max priority queue with O(1) enqueue, O(n) dequeue, and O(n) peek."""


class FastDequeueMaxPriorityQueue(PriorityQueue):
    """A max priority queue with O(n) enqueue, O(1) dequeue, and O(1) peek."""
