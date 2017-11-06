---
title: Concurrency Control
---

There are several interactions between transactions - say parallely two
requests come to read/write on the same record. 

### Problems

* **Dirty read**: Read from row modified by a running transaction, not
  committed yet.
* **Non repeatable read**: Row retrieved twice, although values differ
  between the reads.
* **Phantom**: Two similar queries - give different results.

### Handling

#### Scheduler

A scheduler can **delay** or **abort** a transaction, in favour of
optimizing read-write to disk or or consistency.

* Criteria:
    * Read uncommitted.
    * Read rommitted.
    * Repeatable read.
    * Serializabality.

* Protocol:
    * No Locking
    * Locking
    * Optimistic
    * Timestamp


##### Serial and Serializable Schedules

If transaction executed alone, starts and leaves database in a
consistent state.

* **Schedule**: Time ordered sequence of important actions taken by one or
more transactions.

###### **Serial schedule**

<table class="table table-inverted">
<thead>
<tr class="header">
<th>
T1
</th>
<th>
T2
</th>
</tr>
</thead>
<tbody>
<tr>
<td>

```py
Read(A)         # 1
A = A + 100     # 1
Write(A)        # 1
Read(B)         # 1
B = B + 100     # 1
Write(B)        # 1
```
            
</td>
<td>

```py
Read(A)         # 2
A = A * 2       # 2
Write(A)        # 2
Read(B)         # 2
B = B * 2       # 2
Write(B)        # 2
```

</td>
</tr>
</tbody>
</table>

Many ways of scheduling the above, nesting indicates the time of execution:

<table class="table table-inverted">
<thead>
<tr class="header">
<th>
serial: T1, T2
</th>
<th>
serial: T2, T1
</th>
<th>
not serial, serializable
</th>
<th>
not serial, not serializable
</th>
</tr>
</thead>
<tbody>
<tr>
<td>

```py
Read(A)         # 1
A = A + 100     # 1
Write(A)        # 1
Read(B)         # 1
B = B + 100     # 1
Write(B)        # 1

    Read(A)         # 2
    A = A * 2       # 2
    Write(A)        # 2
    Read(B)         # 2
    B = B * 2       # 2
    Write(B)        # 2
```
            
</td>
<td>

```py
    Read(A)         # 2
    A = A * 2       # 2
    Write(A)        # 2
    Read(B)         # 2
    B = B * 2       # 2
    Write(B)        # 2

Read(A)         # 1
A = A + 100     # 1
Write(A)        # 1
Read(B)         # 1
B = B + 100     # 1
Write(B)        # 1
```

</td>
<td>

```py
Read(A)         # 1
A = A + 100     # 1
Write(A)        # 1

    Read(A)         # 2
    A = A * 2       # 2
    Write(A)        # 2

Read(B)         # 1
B = B + 100     # 1
Write(B)        # 1

    Read(B)         # 2
    B = B * 2       # 2
    Write(B)        # 2
```

</td>
<td>
```py
Read(A)         # 1
A = A + 100     # 1
Write(A)        # 1

    Read(A)         # 2
    A = A * 2       # 2
    Write(A)        # 2

    Read(B)         # 2
    B = B * 2       # 2
    Write(B)        # 2

Read(B)         # 1
B = B + 100     # 1
Write(B)        # 1
```
</td>
</tr>
<tr>
<td>
A = 2x + 200, B = 2x + 200
</td>
<td>
A = 2x + 100, B = 2x + 100
</td>
<td>
A = 2x + 200, B = 2x + 200
</td>
<td>
A = 2x + 200, B = 2x + 100
</td>
</tr>
</tbody>
</table>

    

###### **Serializable schedules**


### Notations

$$
\begin{align*}
r_T(X) &= \text{T reads X}\\
w_T(X) &= \text{T writes X}\\
r_i(X) &= r_{Ti}(X)\\
w_i(X) &= w_{Ti}(X) \\
 & \\
\text{T1} &: r_1(A); w_1(A); r_1(B), w_1(B); \\
\text{T2} &: r_2(A); w_2(A); r_2(B), w_2(B); 
\end{align*}
$$

We're looking for possible rearrangements of $T1; T2$, which
significantly speeds up our execution without compromising consistency.

For this, we take into account the following observations:

* $r_i(X); r_j(X)$ are not in conflict. (No change in value).
* $r_i(X); w_j(X)$ not in conflict, provided $X\neq Y$.
* $w_i(X); r_j(Y)$ not in conflict, provided $X\neq Y$.
* $w_i(X); w_j(Y)$ not in conflict, provided $X\neq Y$.

Actions of different transactions may be swapped unless:

* involves same database element.
* at least one of them is a write.

We carry out non-conflicting swaps to convert a serializable schedule
into a serial schedule.

* **conflict equivalent**: swaps of adjacent actions interconvert the
  two.


### Locks

Lock an element, if some schedule tries to access, then it is illegal.

Rules:

* Well formed transactions. <br/>
   $$ T_i: T_{j} + l_i(A); p_i(A); u_i(A); $$
* Legal Scheduler: <br/>
  No transactions unlock an existing lock except the one that locked
  it.
* Two-phase Locking: <br/>
  Every transaction, lock requests precede unlock requests.


#### Examples
```py
l1(A); Read(A)  # 1
A = A + 100     # 1
Write(A); u1(A) # 1

    l2(A); Read(A)  # 2
    A = A * 2       # 2
    Write(A); u2(A) # 2

    l2(B); Read(B)  # 2
    B = B * 2       # 2
    Write(B); u2(B) # 2

l1(B); Read(B)  # 1
B = B + 100     # 1
Write(B); u1(B) # 1

```

We assume that deadlocked transactions are rolled back, having no effect
or not appearing in schedule.

Not all serializable schedules are covered by two phase locking. Hence:

$$ \text{2PL} \subset \text{Serializable} $$

#### Improving: Multi-mode locks

Need we exclusively lock all the time? Not necessarily. Hence we
introduce multiple kind of locks.

###### shared + exclusive 

* shared lock or read lock.
* exclusive lock or write lock
* $sl_i(X), xl_i(X), u_i(X)$.

Compatibility matrix:

|   | S     | X     |
| - | -     | -     |
| S | true  | false |
| X | false | false |

###### shared + exclusive + upgrade

A possible deadlock could arise from something having a read lock
requesting a write lock after. Inorder to prevent this and to be
friendly with the write request, an upgrade lock is introduced.

Compatibility matrix:


|   | S     | X     | U     |
| - | -     | -     | -     |
| S | true  | false | true  |
| X | false | false | false |
| U | false | false | false |

###### shared + exclusive + increment

Some operations on data can be swapped, like multiplication by one, two
increment requests - since $a + (b + c) = (a + b) + c$. One example of
implementing this is by implementing an increment lock for addition.

Compatibility matrix:


|   | S     | X     | I     |
| - | -     | -     | -     |
| S | true  | false | true  |
| X | false | false | false |
| I | false | false | true  |


<script type="text/javascript">
    $('table').addClass('table');
</script>
