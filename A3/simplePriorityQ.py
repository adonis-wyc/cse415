'''simplePriorityQ.py

This is a simple implementation of a priority queue that supports
the remove operation as well as insert and deletemin.  Rather than
using heapdict.py, it just uses a list of tuples and does linear
searches when needed.

Version 0.1, S. Tanimoto, Jan. 27, 2018.
 Supports access by key to previously enqueued elements.

This data structure is provided to support implementations
of A* in Python.

'''

class PriorityQ:
  def __init__(self):
    self.h = []

  def insert(self, elt, priority):
    for (p, old_elt) in self.h:
      if elt==old_elt:
        raise Exception("Key is already in the priority queue: "+str(elt))
    self.h = self.insert_sorted(elt, priority, self.h)

  def insert_sorted(self, elt, priority, lst):
    if lst==[]: return [(priority, elt)]
    this_p, this_elt = lst[0]
    if priority <= this_p: return [(priority, elt)]+lst
    else: return [lst[0]] + self.insert_sorted(elt, priority, lst[1:])

  def deletemin(self):
    # Returns the element having smallest priority value.
    if self.h==[]:
      raise Exception("deletemin called on an empty priority queue.")
    item = self.h[0]
    self.h = self.h[1:]
    return (item[1],item[0])

  def remove(self, elt):
    # Removes an arbitrary element from the priority queue.
    # This allows updating a priority value for a key by
    # first removing it and then inserting it again with its
    # new priority value.
    for (idx, item) in enumerate(self.h):
      if item[1]==elt: del self.h[idx]

  def getpriority(self, elt):
    for (p, e) in self.h:
      if e==elt: return p
    raise Exception("In getpriority, element not found in the priority queue.")

  def getEnqueuedElement(self, key):
    for item in self.h:
      p, e = item
      if e==key: return e
    raise Exception("In getEnqueuedElement, element not found in the priority queue.")

  def __len__(self):
    return len(self.h)

  def __contains__(self, elt):
    for (p, e) in self.h:
      if e==elt: return True
    return False

  def __str__(self):
    return 'PriorityQ'+str(self.h)

  def print_pq(self, name, priority_val_name):
    size = len(self)
    lst = self.h
    # The following sorting is by priority value.
    # This is problem-independent.
    # It's needed because humans want to see the
    # priority queue as a sorted list, not as a 
    # semi-sorted binary heap.
    # The sorting might seem to undo the efficiency
    # gains of using the binary heap.  True, and if
    # that is an issue in some application, we just comment
    # out the call to this optional function that is for
    # the benefit of humans inspecting the alg's behavior.
    
    print(name+" is now: ",end='')
    for idx,pq_item in enumerate(lst):
      if idx < size-1: 
        print(self.pq_item_str(pq_item, priority_val_name),end=', ')
      else:
        print(self.pq_item_str(pq_item, priority_val_name))

  def pq_item_str(self, pq_item, priority_val_name):
    '''Format one item from the priority queue.'''
    (p, s) = pq_item
    return str(s)+'('+priority_val_name+' = '+str(p)+')'
  
