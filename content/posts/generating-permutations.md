---
title: "Generating Permutations"
date: 2026-02-25T12:00:00+03:00
draft: false
summary: "A gentle introduction into generating permutations"
---

## Generating Permutations

Suppose we have a set `A = {1,2,3,4,5}`. How many subsets of A contain exactly 3 elements? You can start by asking the 
question, how many total subsets of `A` are there in total. There are total of `A*` subsets of A also known as the power set. 

The way you do this is for each element of A we need to decide if that element should be included in the subset. We will need 
to decide yes or no for all elements in the set. Therefore the power set is  ```$ 2 ^ n $``` where `n` is the number
of elements in a set

The next question to ask can be out of all those 32 subsets, how many of them contain only 3 elements? You can say there 
are 5 choices to choose from, when you choose the first element, there are remaining 4 elements to choose from for the 
second item, then 3 for the third item. The product rule would say `5 * 4 * 3` which is `60`. That cannot be correct 
since we have the powerset as `32`. 

> I still need to understand subsets and supersets. Understand it from first principles

## Binomial Coefficients

- 



## Combinatorics

