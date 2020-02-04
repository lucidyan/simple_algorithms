# Exact Bayesian Inference for A/B testing

## Part I
<sup>**author: Evan Haas**</sup><br/>
<sup> 2009.12.09 </sup><br/>
<sup>[Source](https://web.archive.org/web/20100929074846/http://sirevanhaas.com/?p=30)</sup>

In this three part series I’m going to talk about statistics in the context of [A/B Testing](http://en.wikipedia.org/wiki/A/B_Testing). Part I discusses how to analyze experiments using traditional techniques from the [frequentist](http://en.wikipedia.org/wiki/Frequentist) school. Part II will discuss the [Bayesian approach](http://en.wikipedia.org/wiki/Bayesian_probability), and Part III will provide an implementation of the Bayesian method. Much of the information is adapted from the excellent [Information Theory, Inference, and Learning Algorithms](http://www.inference.phy.cam.ac.uk/mackay/itila/) by David MacKay, chapter 37.

For simplicity, I’m going to talk about the simplest case, which is when only one test is run at a time, the two alternatives are assumed not to interact with each other, and outcome is binary – mathematicians call this a Bernoulli process. Working with these assumptions, we can model each of the alternatives as a binomial distribution with an unknown rate of success. Alternative A has $n_a$ trials and $c_a$ conversions, giving us a success frequency of $f_a=\frac{c_a}{n_a}$. Likewise, for alternative B we have $n_b$ trials, $c_b$ conversions, and $f_b=\frac{c_b}{n_b}$. Given this information, we want to know whether one of the alternatives is better in a statistically significant way.

To review, the traditional way to answer this question would be to assume a Gaussian distribution, since it is a good approximation of the binomial distribution with a large enough sample, and use the null hypothesis: $f_a=f_b$, reflecting our prior belief that the two alternatives will have equal conversion rates. We would then use a two sample Z-test to determine if our results differ significantly from what the null hypothesis predicts:

$$z = \frac{f_a - f_b}{\sqrt{\frac{f_a \left({1 - f_a}\right)}{n_a} + \frac{f_b \left({1 - f_b}\right)}{n_b} }} $$
(n.b. keep in mind that the null hypothesis assumes our two conversion frequencies are equal).

Finally, using this value we look in our handy Standard normal table and find the p-value, to determine the probability that we got this result by chance, assuming the truth of the null hypothesis. For example, let’s say we look up the value in the table and see that our p-value is 0.04. This means that if we were to run our experiment a large number of times, and the null hypothesis is true, about 4% of those times we would see results at least as extreme as the ones we recorded. Since a p-value of 0.05 is typically accepted as the threshold for statistical significance, we would conclude that the null hypothesis can be rejected – there is a statistically significant difference between $f_a$ and $f_b$.

Overall it’s a pretty simple procedure, so what are the downsides? The first is that approximating a binomial distribution with a normal distribution is not exact. There are a number of rules that can be used to determine when the approximation is valid – see Wikipedia for a discussion of these rules. A second problem is that this simple test doesn’t tell us anything about the magnitude of the difference between $f_a$ and $f_b$ - it only tells us how confident we can be in rejecting the null hypothesis that the two are equal. Finally, it does not allow us to answer a very natural question about the data :
“What is the probability that $f_a > f_b$?”

To solve these problems we will turn to Bayesian methods in part II.

___

## Part II

<sup>**author: Evan Haas**</sup><br/>
<sup> 2010.01.28 </sup><br/>
<sup>[Source](https://web.archive.org/web/20100929074856/http://sirevanhaas.com/?p=64)</sup>

In part one we learned how to determine whether one alternative is better than another using classical statistical methods. While these methods are easy to perform, they unfortunately don’t answer the questions that we intuitively want to see answered – “What is the probability that A is better than B?” or “How much better is A than B?”. Remember that the z-test from part one only tells us how confident we can be in rejecting the null hypothesis that the two alternatives are equal.

Enter Bayes Theorem. Using this magical piece of mathematics, we can actually give an exact answer to the question, “What is the probability, given these results, that A has a higher conversion frequency than B?” In the following equations, for convenience, I will refer to the probability of conversion $f_a$ as $f_a+$, and the probability of not converting, $1–f_a+$, as $f_a−$.

The value we are interested in is the posterior probability distribution $Pr(f_{a+},f_{b+}|D)$ of $f_{a+}$ and $f_{b+}$, given the observed data $D \equiv \{c_a,c_b,n_a,n_b\}$:

$$Pr(f_{a+},f_{b+}|D)=\frac{Pr(f_{a+},f_{b+}|n_a,n_b)Pr(c_a,c_b|f_{a+},f_{b+},n_a,n_b)}{Pr(c_a,c_b|n_a,n_b)}$$

Ok, so how do we actually use this? Let’s start by writing down the probability distributions that we know.

The easiest one to write is the joint prior distribution for $f_{a+}$ and $f_{b+}$: It’s uniformly 1, reflecting our initial belief that all values of $f_{a+}$ and $f_{b+}$ are equally likely:

$$Pr(f_{a+},f_{b+}|n_a,n_b)=1$$

Next we have the probability of the observed data – $Pr(c_a,c_b|n_a,n_b)$ . For a given conversion rate, the probability distribution for $c$ conversions in $n$ trials is ${n \choose c} {f_+}^c {f_-}^{n-c}$. So, we need to integrate the joint distribution over all possible values of $f$:

$$ \int_0^1 {{n_a \choose c_a} {f_{a+}}^{c_a} {f_{a-}}^{n_a-c_a}\,df_a} \int_0^1 {{n_b \choose c_b} {f_{b+}}^{c_b} {f_{b-}^{n_b-c_b}}\,df_b}= $$

$$ ={n_a \choose c_a} \frac{{c_a}! \left({n_a-c_a}\right)!}{\left({n_a+1} \right)!} {n_b \choose c_b} \frac{{c_b}! \left({n_b-c_b}\right)!}{\left({n_b+1} \right)!}= $$

$$ =\frac{1}{\left(n_a+1\right)\left(n_b+1\right)} $$

The final component is called the likelihood:

$$Pr(c_a, c_b | D) = {n_a \choose c_a} f_{a+}^{c_a} f_{a-}^{n_a-c_a} {n_b \choose c_b} f_{b+}^{c_b} f_{b-}^{n_b-c_b}$$

Putting it all together, we have:

$$\left(n_a + 1\right) {n_a \choose c_a} f_{a+}^{c_a} f_{a-}^{n_a-c_a} \left(n_b + 1\right) {n_b \choose c_b} f_{b+}^{c_b} f_{b-}^{n_b-c_b}
$$

Now that we have the joint posterior distribution of $f_a$ and $f_b$, we can easily find the answer to our original question – we just need to integrate over the region where $f_a<f_b$ ! In other words:

$$Pr(f_{a+} < f_{b+}) = \int_0^1 \!\! {\int_{f_{a+}}^1 { \frac{{n_a \choose c_a} f_{a+}^{c_a} f_{a-}^{n_a-c_a} {n_b \choose c_b} f_{b+}^{c_b} f_{b-}^{n_b-c_b}}{\frac{1}{\left(n_a+1\right)\left(n_b+1\right)}} } }$$

$$=\frac{(n_a+1)!}{c_a!(n_a-c_a)!}\frac{(n_b+1)!}{c_b!(n_b-c_b)!}\int_0^1f_{a+}^{c_a}(1-f_{a+})^{n_a-c_a}\int_{f_{a+}}^1f_{b+}^{c_b}(1-f_{b+})^{n_b-c_b}$$

So now we’ve got a very difficult-looking integral instead of a straightforward computation like in part 1. Where do we go from here? Normal people would throw this equation into a numeric solver and get a very close approximation to the answer. However, since I can’t afford Mathematica, we’re going to have to solve this one exactly. Stay tuned for part 3 to see how.

___

## Part III

<sup>**author: Antti Rasinen**</sup><br/>
<sup> 2011.12.29 </sup><br/>
<sup>[Source](https://web.archive.org/web/20130331072458/http://arsatiki.posterous.com/bayesian-ab-testing-with-theory-and-code)</sup>

At my last employer I looked briefly into [A/B tests](http://en.wikipedia.org/wiki/A/B_testing). Many of the proposed solutions rely on classical statistical tests, such as the z-test or G-test. These tests are not very appealing to me. They solve an approximate problem exactly; I prefer the converse.

To my delight, I found a three-part series by Sir Evan Haas, which discussed using Bayesian inference on A/B tests. Sadly, only parts I and part II are available. The blog seems to have died out before part III ever came out. Part II ended with a cliffhanger: a hairy integral and a promise "solved in Part III". 

For the last year and a half I've thought about the problem on and off. WolframAlpha could not solve the integral in a meaningful fashion. I plotted the joint probability distribution with R, but this left me wanting more.

A month ago I bumped into Bayesian networks (although I prefer "probabilistic graphical models"). This triggered a problem solving cascade in my mind. I finally managed to crack the problem! Both approximately and exactly! Oh happy times! Oh groovy times!

#### A simple variant

In his articles, Evan considers the whole joint probability distribution at once. That approach leads quickly into a mathematical briar patch with eye-poking indices and double integrals. However, the thorny mess becomes simpler with some theory.

So let us look at a simpler case–estimating the conversion rate for only one alternative. More precisely, what do we know about the conversion rate, if we've seen s conversions out of n trials? How is the probability distributed?

This is incidentally the oldest trick in the book. I mean this literally. The essay, in which Thomas Bayes debuted his formula, was dedicated to finding out the answer to this very question. His ["An Essay towards solving a Problem in the Doctrine of Chances"](https://en.wikipedia.org/wiki/An_Essay_towards_solving_a_Problem_in_the_Doctrine_of_Chances) is available on the Internet.

I will use different symbols than Evan does. Sorry about that. The unknown conversion rate is denoted by $r$. Our data consists of the number of successes $s$ and the number of failures $f$  in $n$ trials. Note that $n = s + f$.

Let's use the same binomial model as Evan for our likelihood. That is, we assume the number of successes s to be distributed according to the binomial distribution: $s \sim Binomial(s + f, r)$.

At this point I found the missing ingredient: [conjugate priors](http://en.wikipedia.org/wiki/Conjugate_prior). A conjugate prior means that our posterior "looks the same" as the prior itself. Both the posterior and the prior belong to a "same family." Their difference is usually in the parameters of the distribution. This allows algebraically nice updating rules for the posterior. In this case, the rules are very very pleasant.

The conjugate prior for the binomial distribution is the beta distribution $Beta(\alpha, \beta)$. Limiting our prior in this way seems foolish and constricting. What if there are no sane parameter choices for the prior? Fear not! The $Beta(1, 1)$ distribution is the same as the uniform distribution over (0, 1). It is a good choice for this application, where we do not know anything about the conversion rate.

The updating rule for the posterior is now exceedingly simple:

$$r \sim Beta(s + 1, f  + 1)$$

In general, if our prior is distributed according to Be(α, β), then the posterior is

$$r \sim Beta(\alpha + s, \beta + f)$$

This is a wonderful result. We can mostly omit the Bayesian mechanism that led us here. Instead, we can simply use the beta distribution! (Turns out that people in medicine and other fields have known this result for ever.)

#### Example time

Let's assume we've seen 5 conversions out of 100 trials. This means that $s$ = 5 and $f$ = 100-5 = 95. You can use WolframAlpha for plotting.

http://www.wolframalpha.com/input/?i=BetaDistribution%5B6%2C96%5D

If we have more data, our estimate improves. For 50 conversions and 1000 trials, we get the following PDF:

https://www.wolframalpha.com/input/?i=BetaDistribution%5B51%2C951%5D

The probability mass is now very sharply centered around 0.05.

#### Numerical solutions to the full problem

Since we now have a handle what happens with a single variant, let's crack the full problem. Given the successes $s_1$, $s_2$ and respective failures $f_1$, $f_2$ for the two variants, what is the probability $P(r_1 \gt r_2)$? This is the 2D integral in Evan's Part II. (I'm not going to repeat it here.)

Originally I solved the question by integrating the joint distribution numerically over a 100 x 100 grid. If This gives rather good results. Sadly, I can not find the code I used.
After discovering that the distribution is a joint distribution of two independent beta distributions, I realized I can also use simulation. This is conceptually super simple.

First, generate $N$ pairs of random samples from the joint distribution. Since they are independent, you need only pick the first item in the pair from the first beta distribution and similarly for the second item. You may need to generate a lot of samples, if the two rates are close to each other.

Count how many of the pairs have the first number greater than the second. Let us call this number $k$.

Then you can get the estimate for the probability $P(r_1 \gt r_2)$ simply dividing $k / N$.

Below is a simple implementation in Python:
```python
from __future__ import division
from random import betavariate
import math
import sys

def sample(s1, f1, s2, f2):
    p1 = betavariate(s1 + 1, f1 + 1)
    p2 = betavariate(s2 + 1, f2 + 1)
    return 1 if p1 > p2 else 0

def odds(p):
    return p / (1 - p)

def main():
    if len(sys.argv) != 6:
        sys.exit("Usage: %s n_iter succ1 fail2 succ2 fail2" % sys.argv[0])
    
    total, s1, f1, s2, f2 = map(int, sys.argv[1:])
    count = sum(sample(s1, f1, s2, f2) for k in range(total))
    o = odds(count / total)
    b = 10 * math.log(o, 10)
    print odds(count / total), "to 1 or", b, "dB"

if __name__ == "__main__":
    main()
```
<sup>[Source](https://gist.github.com/arsatiki/1395348/6dccd38d608437ccd1a9a15aa856b326e86898ce)</sup>

#### An exact solution! Hallelujah!

First of all, don't thank me. Thank John D. Cook. [His article about random inequalities](http://www.johndcook.com/blog/2008/08/21/random-inequalities-v-beta-distributions/) contained the hint that when one of the parameters is an integer, we can compute a closed solution. One? *All of our parameters are integers!*

My solution follows the mathematical form given in the [linked PDF article "Exact Calculation of Beta Inequalities
John Cook" by John Cook](https://web.archive.org/web/20140217082236/http://www.mdanderson.org/education-and-research/departments-programs-and-labs/departments-and-divisions/division-of-quantitative-sciences/research/biostats-utmdabtr-005-05.pdf). The code is below.

```python
from __future__ import division
import math
import sys

def gamma(n):
    return math.factorial(n - 1)

def h(a, b, c, d):
    num = gamma(a + c) * gamma(b + d) * gamma(a + b) * gamma(c + d)
    den = gamma(a) * gamma(b) * gamma(c) * gamma(d) * gamma(a + b + c + d)

    return num / den

def g0(a, b, c):
    return gamma(a + b) * gamma(a + c) / (gamma(a + b + c) * gamma(a))

def hiter(a, b, c, d):
    while d > 1:
        d -= 1
        yield h(a, b, c, d) / d

def g(a, b, c, d):
    return g0(a, b, c) + sum(hiter(a, b, c, d))

def print_odds(p):
    o = p / (1 - p)
    b = 10 * math.log(o, 10)

    if o > 1:
        s = "%.4f to 1" % o
    else:
        s = "1 to %.4f" % (1 / o)
    
    print s, "or %.4f dB" % b


def main():
    if len(sys.argv) != 5:
        sys.exit("Usage: %s succ1 fail1 succ2 fail2" % sys.argv[0])
    
    s1, f1, s2, f2 = map(int, sys.argv[1:])

    print_odds(g(s1 + 1, f1 + 1, s2 + 1, f2 + 1))

if __name__ == "__main__":
    main()
```
<sup>[Source](https://gist.github.com/arsatiki/1395348/f0275f529d322d3c23e18201f26890f5a09dcb51)</sup>

The code is a rather straightforward translation. I'd rather have used recursion, but the Python call stack blows up when $d$ is anything significant.

Also note that my code is numerically insane (and slow). If you wanted to do this for a living, you'd better use the lgamma function to compute the logarithm of the gamma function. Gamma functions are in effect factorials. They grow very very fast; a float or even a double will overflow  quickly.  For example, the g0 function would be
 
```python
exp(lgamma(a+b) + lgamma(a+c) - lgamma(a+b+c) - lgamma(a))
```

You'd also want to use the permutation tricks mentioned in the article to recurse on the smallest parameter.

#### Summary

- The distribution of the conversion rate for one variant is the beta distribution. (This applies when our model is the binomial model. More complex approaches are of course possible.)
- You can solve $P(A \gt B)$ it numerically (in two ways) or exactly.
- These are all known results.
