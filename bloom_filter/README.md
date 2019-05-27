[Original article (chinese)]

When we design an algorithm, we often have to consider the balance between time efficiency and space efficiency. Changing space with time, or changing space for space is an inevitable operation in most cases. If I tell you that there is such a data structure, it is excellent in terms of time efficiency and space efficiency. Unexpected surprises, surprises are not pleasant surprises? !

Today we will discuss a data structure commonly used in big data processing: [Bloom Filter]. The main purpose of the Bloom filter is to retrieve whether an element is in a collection.
This is a data structure that people love and hate. Because it takes up very little space and provides constant time queries; but at the same time, it also has some inevitable shortcomings, such as it has a certain false positive rate of $\($false positive rate$\)$;
At the same time, the original version of Bloom Filter cannot delete elements.

 This article focuses on the following:

* The basic concept of Bloom Filter
* Calculation of main parameters of Bloom Filter

Introduction to Bloom Filter
=================

One of the most common operations we encounter during data processing is the **membership query**. The so-called membership query is to determine whether an element exists in a given collection.
The easiest way to do this is to store the collection data in a linked list structure, and then each query is the traversal of the linked list. When the amount of data becomes larger, this linked list structure is certainly not optimized enough, because each
The time complexity of the secondary query is $O\(n\)$. There is often a follow up problem during the interview, so that the efficiency of the query is improved. At this time, the tree structure is often debuted because they can make the efficiency of the query change.
Is $O\(logn\)$. Of course, the tree structure can still be optimized, using our great hashing methods, such as Chain Hashing and Bit Strings, or a simple hash table.
Get the time complexity of $O\(\frac{n}{k}\)$. Here is a question, when interviewing, you can guess the method you need to use according to the complexity of the question, although it may not be 100% correct.
, but almost can guess that it is not far from ten.

At this time, if the interviewer continues to ask, is there any way to make the time and space more complex? Then, you can safely say to him: yes, yes, it is the legendary Bloom Filter.
The idea of ​​Bloom Filter is very simple. The physical structure of a Bloom Filter is actually a bit vector. Each bit of this bit vector is initially set to 0. At the same time, each Bloom Filter
All are accompanied by k hash functions. The process of inserting elements into the Bloom Filter is to calculate this element with each hash function, thus changing the bit corresponding to the result to 1. If the current bit is already 1,
Then keep this bit unchanged during the insertion process.

Take a look at the Bloom Filter sample diagram:
![Image](https://github.com/sophiesongge/sophiesongge.github.io/blob/master/images/Bloom_Filter.png?raw=true)

In this example, our Bloom Filter consists of a 30-bit Bit Vector and three Hash Functions. We insert the three elements $S_1$, $S_2$ and $S_3$ into this Bloom Filter.
Then query the other three new elements $S_1$, $S_x$ and $S_y$. As shown in the figure, $S_1$ and $S_x$ will be considered as belonging to this Bloom Filter, because the corresponding bit is 1 and $S_y$ is considered
Does not belong to this Bloom Filter. However, $S_x$ is a false positive answer because we didn't insert this element when we inserted it. False Positive's answer was caused by Hash Collision. We can change the length of BF according to the number of elements to be inserted, thus reducing the false positive rate.

Calculation of main parameters of Bloom Filter
===========================

There are four main parameters that affect the performance of the Bloom Filter:

* n : The maximum number of elements that need to be inserted into the Bloom Filter
* m : number of bits in the Bloom Filter
* k : number of Hash Functions
* p : False Positive rate of Bloom Filter

The number of elements that need to be inserted into the Bloom Filter is known to us, or at least roughly estimated. So when building a Bloom Filter, you mainly need to set the number of bits to limit the false positive rate.
the size of. Or control the size of the false positive rate at a fixed value to estimate the length of the bit of the Bloom Filter.

Before introducing the parameter calculation of Bloom Filter, I would like to introduce a classic model in probability theory, [Balls into Bins] model. This model has a very wide range of applications in the field of Computer Science. It involves n balls and m boxes.
Each time, randomly put a ball into one of the boxes. After placing all the balls in the box, we observe the number of balls in each box. We call this number the load of each box, and we want to know: What is the maximum load per box? Bloom
 The idea of ​​Filter draws a lot from the Balls and Bins problem. The difference is that we throw each "ball" multiple times with multiple hash functions. The false positive is related to the load of each "box". Below we will introduce step by step
How each parameter is calculated in the Bloom Filter.

Let us first look at a lemma:

**Lemma 1:** With k Hash Functions, insert n elements into a m-bit Bloom Filter, then the probability that any bit of this Bloom Filter is 0 will not be greater than $e^ {\frac {-k*n}{m}}$

This Lemma calculates the probability that any bit in the Bloom Filter is 0. The calculation idea is similar to the probability that any box in the balls into bins model is empty.

**prove:**
After inserting an element with a Hash Function, the probability that a particular bit is 0 is: $1 - \frac{1}{m}$

So, after inserting an element with k Hash Functions, the probability that a particular bit is 0 is: $(1 - \frac{1}{m})^{kn}$

And: $\lim\limits_{m\to\infty}(1-\frac{1}{m})^{kn}=e^{\frac{-kn}{m}}$

**Lemma 2:** Suppose we use [Simple Uniform Hashing Functions] to insert the Bloom Filter. The False Positive rate p of this Bloom Filter is a function of m, n and k, and p = $(1-e^ {-\frac{nk}{m}})^k$

**prove:**
The Simple Uniform Hashing function hashes each element to one of m bits with equal probability. When a certain hash function is used to process a certain element, the probability that a particular bit $b_x$ is not set to 1 is: $1-\frac{1}{m}$

So, when using k Hash Function to process this element, the probability that a particular bit $b_x$ is not set to 1 is: $(1-\frac{1}{m})^k$

Then, when n elements are processed with k Hash Functions, the probability that a particular bit $b_x$ is not set to 1 is: $(1-\frac{1}{m})^{kn }$

Conversely, the probability that this bit is set to 1 is: $1-(1-\frac{1}{m})^{kn}$

In the query phase, if all the hash bits of this element in the Bloom Filter are set to 1, then this element is considered to exist in the query set. So the probability of False Positive is:

p = $(1-(1-\frac{1}{m})^{kn})^k$

In view of:

$\lim\limits_{x\to0}(1+x)^{\frac{1}{x}}=e$

$\lim\limits_{m\to\infty}(-\frac{1}{m})=0$

$\Rightarrow$ $\lim\limits_{m\to\infty}(1-(1-\frac{1}{m})^{kn})^k$ = $\lim\limits_{m\to\ Infty}(1-(1-\frac{1}{m})^{-m\times\frac{-kn}{m}})^k$ = $(1-e^{-\frac{nk }{m}})^k$

<font color="red">I Note: Many people think that p = $(1-e^{-\frac{nk}{m}})^k$ is the probability of a Bloom Filter's False Positive, here I hope To clarify, in fact, it is the probability that an element is considered to belong to a Bloom Filter, so this probability actually includes True Positive. But it is the upper bound of the false positive, so in this paper we still use the probability that this probability is false positive as the basis for the calculation. </font>
<br>
**Lemma 3:** Suppose we use k hash functions to insert n elements into a Bloom Filter with m bits, then the expected number of non-zero bits is: $m\cdot(1-e ^{\frac{-kn}{m}})$

** Proof: ** Suppose $X_j$ is a set of random variables, and $X_j$=1 when the jth bit is 0, and $X_j$ is 0. Then, according to Lemma 2, $E\left[X_j\right]$ = $(1-\frac{1}{m})^{kn} \approx e^{\frac{-kn}{m}}$

Suppose X is a random variable representing the number of bits that are still 0, then: $E\left[X\right]$ = $E\left[\sum_{i=1}^{m} X_i\right ]$ = $\sum_{i=1}^{m} E\left[X_i\right] \approx me^{\frac{-kn}{m}} $

So the expectation of the number of non-zero bits is: $m\cdot(1-e^{\frac{-kn}{m}})$

Increasing the number of bits in a Bloom Filter can reduce the chance of Hash Collisions and reduce the probability of False Positive. But the more bits the Bloom Filter has, the more hard disk space it has. Here, we assume that if half of the bit of a Bloom Filter is reset to 1, the Bloom Filter achieves a balance between space and Hash Collisions (of course you can make other assumptions here).
Under this assumption, we can calculate the relationship between the main parameters of the Bloom Filter.

Suppose that when a Bloom Filter reaches equilibrium, it contains n elements. The following equation describes the relationship between the number of bits in the Bloom Filter, the number of hash functions used, and the number of inserted elements. :$m = \frac{k \cdot n}{50\%} = 2 \cdot k \cdot n $ bits

**Lemma 4:** When $e^{-\frac{nk}{m}}$ = $\frac{1}{2}$, the False Positive probability p reaches a minimum. At this point: k = ln2 $\times \frac{m}{n}$, p = $\frac{1}{2}^k$ = $2^{-ln2 \times \frac{m}{n}} $

**Certificate: ** According to Lemma 2, $p$ = $(1-e^{-\frac{nk}{m}})^k$

So, p can be thought of as a function of k: $p$ = $f(k)$ = $(1-e^{-\frac{nk}{m}})^k$

Then: $f(k) = (1 - b^{-k})^k,b = e^{-\frac{n}{m}}$ (1)

Taking the log values ​​on both sides of equation (1), you can get: $ln[ f(k)] = k \cdot ln(1-b^{-k})$ (2)

Deriving on both sides of equation (2) gives: $\frac{1}{f(x)} \cdot f'(x) = ln(1-b^{-k}) + k \cdot \frac{ 1}{1-b^{-k}} \cdot (-1) \cdot (-b^{-k}) \cdot ln(b)
                = ln(1-b^{-k}) + k \cdot \frac{b^{-k} \cdot ln(b)}{1-b^{-k}}$ (3)

When equation (3) is equal to 0, equation (2) reaches a minimum. At this time you can get: $ln(1-b^{-k}) + k \cdot \frac{b^{-k} \cdot ln(b)}{1 - b^{-k}} = 0$ (4)

$\Rightarrow (1- b^{-k}) \cdot ln(1- b^{-k}) = b^{-k} \cdot ln(b^{-k})$ (5)

According to the symmetry of the two sides of equation (5), we can get: $1 - b^{-k} = b^{-k}$ (6)

$\Rightarrow e^{-\frac{kn}{m}} = \frac{1}{2}$ (7)

$\Rightarrow k = ln2 \cdot \frac{m}{n}$ (8)

So: $p = f(k) = (1-\frac{1}{2})^{k} = (\frac{1}{2})^k = 2 ^ {ln2 \cdot \frac{m }{n}}$

The following theorem can be withdrawn by Lemma 4:

**Theorem 1:** Knowing that a Bloom Filter has a False Positive of p and that the maximum number of elements to be inserted is n, the length of this Bloom Filter should be: $m = - \frac{n \cdot lnp} {(ln2)^2}$

The number of Hash Functions to be used should be: $k = ln2 \cdot \frac{m}{n} = log_2\frac{1}{p}$


Delete elements in the Bloom Filter
==================

Before introducing the implementation of Bloom Filter, I would like to discuss with you about the deletion of elements in the Bloom Filter. The traditional Bloom Filter described above has no way to delete, because because of Hash Collision, simply resetting the corresponding bit of the element to be deleted to 0 will accidentally delete other elements.

In order to solve this problem, we can replace each bit with a counter. To delete an element, we can reduce the counter of the corresponding bit. This variant of Bloom Filter is called Counting Bloom Filter. Although it adds a delete operation to the Bloom Filter, it also increases the 'footprint' of the Bloom Filter.

So is it possible to still use bit vector as the implementation of Bloom Filter, and add delete function? The answer is yes, one of my favorite implementations is called Shifting Bloom Filter. It was proposed in a 2016 article on VLDB, where we briefly introduce its ideas. In this article, the authors found that usually we need to re-Bloom Filter
Stores two types of information, (1) whether the element exists in the data set (2) additional information of the element. Traditional BF has been well solved (1). In SFB, the author uses an offset to store additional information about the element. This offset is also a hash function. When $h_i(e)$ is set to 1, SFB will be $ H_i(e)+o(e)$ is also set to 1. Interested students can read [this article].
We will not repeat them.


[Original article (chinese)]: https://sophiesongge.github.io/big/data/2016/09/06/bloom-filter.html
[Bloom Filter]: https://en.wikipedia.org/wiki/Bloom_filter
[Balls into Bins]: https://en.wikipedia.org/wiki/Balls_into_bins
[Simple Uniform Hashing Functions]: https://en.wikipedia.org/wiki/SUHA_(computer_science)
[This article]: http://www.vldb.org/pvldb/vol9/p408-yang.pdf
[put code]: https://github.com/sophiesongge/BloomFilter/blob/master/src/BloomFilter/BloomFilter/BloomFilter.java