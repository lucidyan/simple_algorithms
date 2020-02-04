# Exact Bayesian Inference for A/B testing
<sup>**author: Evan Haas**</sup>

## Part I
<sup>09 Dec 2009</sup>
<sup>[Source](https://web.archive.org/web/20100929074846/http://sirevanhaas.com/?p=30)</sup>

In this three part series I’m going to talk about statistics in the context of [A/B Testing](http://en.wikipedia.org/wiki/A/B_Testing). Part I discusses how to analyze experiments using traditional techniques from the [frequentist](http://en.wikipedia.org/wiki/Frequentist) school. Part II will discuss the [Bayesian approach](http://en.wikipedia.org/wiki/Bayesian_probability), and Part III will provide an implementation of the Bayesian method. Much of the information is adapted from the excellent [Information Theory, Inference, and Learning Algorithms](http://www.inference.phy.cam.ac.uk/mackay/itila/) by David MacKay, chapter 37.

For simplicity, I’m going to talk about the simplest case, which is when only one test is run at a time, the two alternatives are assumed not to interact with each other, and outcome is binary – mathematicians call this a Bernoulli process. Working with these assumptions, we can model each of the alternatives as a binomial distribution with an unknown rate of success. Alternative A has $n_a$ trials and $c_a$ conversions, giving us a success frequency of $f_a=\frac{c_a}{n_a}$. Likewise, for alternative B we have $n_b$ trials, $c_b$ conversions, and $f_b=\frac{c_b}{n_b}$. Given this information, we want to know whether one of the alternatives is better in a statistically significant way.

To review, the traditional way to answer this question would be to assume a Gaussian distribution, since it is a good approximation of the binomial distribution with a large enough sample, and use the null hypothesis: $f_a=f_b$, reflecting our prior belief that the two alternatives will have equal conversion rates. We would then use a two sample Z-test to determine if our results differ significantly from what the null hypothesis predicts:

$$z=\frac{f_a-f_b}{\sqrt{f_a\frac{1-f_a}{n_a}+f_b\frac{1-f_b}{n_b}}}$$
(n.b. keep in mind that the null hypothesis assumes our two conversion frequencies are equal).

Finally, using this value we look in our handy Standard normal table and find the p-value, to determine the probability that we got this result by chance, assuming the truth of the null hypothesis. For example, let’s say we look up the value in the table and see that our p-value is 0.04. This means that if we were to run our experiment a large number of times, and the null hypothesis is true, about 4% of those times we would see results at least as extreme as the ones we recorded. Since a p-value of 0.05 is typically accepted as the threshold for statistical significance, we would conclude that the null hypothesis can be rejected – there is a statistically significant difference between $f_a$ and $f_b$.

Overall it’s a pretty simple procedure, so what are the downsides? The first is that approximating a binomial distribution with a normal distribution is not exact. There are a number of rules that can be used to determine when the approximation is valid – see Wikipedia for a discussion of these rules. A second problem is that this simple test doesn’t tell us anything about the magnitude of the difference between $f_a$ and $f_b$ - it only tells us how confident we can be in rejecting the null hypothesis that the two are equal. Finally, it does not allow us to answer a very natural question about the data :
“What is the probability that $f_a > f_b$?”

To solve these problems we will turn to Bayesian methods in part II.

___

## Part II

<sup>28 Jan 2010</sup>
<sup>[Source](https://web.archive.org/web/20100929074856/http://sirevanhaas.com/?p=64)</sup>

In part one we learned how to determine whether one alternative is better than another using classical statistical methods. While these methods are easy to perform, they unfortunately don’t answer the questions that we intuitively want to see answered – “What is the probability that A is better than B?” or “How much better is A than B?”. Remember that the z-test from part one only tells us how confident we can be in rejecting the null hypothesis that the two alternatives are equal.

Enter Bayes Theorem. Using this magical piece of mathematics, we can actually give an exact answer to the question, “What is the probability, given these results, that A has a higher conversion frequency than B?” In the following equations, for convenience, I will refer to the probability of conversion $f_a$ as $f_a+$, and the probability of not converting, $1–f_a+$, as $f_a−$.

The value we are interested in is the posterior probability distribution $Pr(f_a,f_b|D)$ of $f_a+$ and $f_b+$, given the observed data $D \equiv \{c_a,c_b,n_a,n_b\}$:

$$Pr(f_a,f_b|D)=\frac{Pr(f_a,f_b|n_a,n_b)Pr(c_a,c_b|f_a+,f_b+,n_a,n_b)}{Pr(c_a,c_b|n_a,n_b)}$$

Ok, so how do we actually use this? Let’s start by writing down the probability distributions that we know.

The easiest one to write is the joint prior distribution for $f_a+$ and $f_b+$: It’s uniformly 1, reflecting our initial belief that all values of $f_a+$ and $f_b+$ are equally likely:

$$Pr(f_a+,f_b+|n_a,n_b)=1$$

Next we have the probability of the observed data – $Pr(Pr(c_a,c_b|n_a,n_b))$ . For a given conversion rate, the probability distribution for c conversions in n trials is $(^n_c)f^c_{+}f^{n-c}_-$. So, we need to integrate the joint distribution over all possible values of $f$:

$$ \int_0^1(^{n_a}\_{c_a})f_{a^+}^{c_a}f_{a^-}^{n_a-c_a}df_a \int_0^1(^{n_b}\_{c_b})f_{b^+}^{c_b}f_{b^-}^{n_b-c_b}df_b= $$

$$ =(^{n_a}\_{c_a})\frac{c_a!(n_a-c_a)!}{(n_a+1)!}(^{n_b}\_{c_b})\frac{c_b!(n_b-c_b)!}{(n_b+1)!}= $$

$$ =\frac{1}{(n_a+1)(n_b+1)} $$

The final component is called the likelihood:

$$Pr(c_a,c_b|D)=(^{n_a}\_{c_a})f_{a^+}^{c_a}f_{a^-}^{n_a-c_a}(n_b+1)f_{b^+}^{c_b}f_{b^-}^{n_b-c_b}$$

Putting it all together, we have:

$$(n_a+1)(^{n_a}\_{c_a})f_{a^+}^{c_a}f_{a^-}^{n_a-c_a}(n_b+1)(^{n_b}\_{c_b})f_{b^+}^{c_b}f_{b^-}^{n_b-c_b}$$

Now that we have the joint posterior distribution of $f_a$ and $f_b$, we can easily find the answer to our original question – we just need to integrate over the region where $f_a<f_b$ ! In other words:

$$Pr(f_{a+} \lt f_{b+})=\int_0^1\int_{f_a+}^1\frac{(^{n_a}\_{c_a})f_{a^+}^{c_a}f_{a^-}^{n_a-c_a}(^{n_b}\_{c_b})f_{b^+}^{c_b}f_{b^-}^{n_b-c_b}}{\frac{1}{(n_a+1)(n_b+1)}}=$$

$$=\frac{(n_a+1)!}{c_a!(n_a-c_a)!}\frac{(n_b+1)!}{c_b!(n_b-c_b)!}\int_0^1f_{a+}^{c_a}(1-f_{a+})^{n_a-c_a}\int_{f_a+}^1f_{b+}^{c_b}(1-f_{b+})^{n_b-c_b}$$

So now we’ve got a very difficult-looking integral instead of a straightforward computation like in part 1. Where do we go from here? Normal people would throw this equation into a numeric solver and get a very close approximation to the answer. However, since I can’t afford Mathematica, we’re going to have to solve this one exactly. Stay tuned for part 3 to see how.
