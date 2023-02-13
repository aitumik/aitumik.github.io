---
title: "Regular Expression Engine"
date: 2023-02-04T00:41:46+03:00
draft: true
---

# Regular Expressions

Regular expressions are notations for describing sets of character strings
A matched string is a set of characters described by a certain regular expression
The simplest regular expression is a single literal character except for metacharacters
Metacharacters include `+?*.` and should be escaped by `\`

Two regular expressions can be alternated or concatenated to form a new regular expression
For example if `e1` matches `s` and `e2` matches `t` then `e1|e2` matches `s` or `t` while `e1e2` matches `st`
`*,+,?` are all repetition operators i.e `e1*` matches **0 or more** `ts`, `e1+` matches **1 or more ts** and `e1?` matches **0 or 1 ts**

The operator precedence,from weakest to strongest is first alternation,concatenation and then repetion operators
Parentheses can be used to force different meanings for example ab|cd is same as (ab)|(bc) and `ab*` is same as `a(b*)`

The above is the traditional syntax
Perl added more operators to be concise but not perfomant :- degrades performance
One extension of the syntax is backreferences (dog|cat)\1 matches dogdog or catcat
This is bad for perfomance for languages like perl 

# Finite Automata

Finite Automata can also be used to describe a set of character strings just like regular expressions
For example to describe a(bb)+a the following finite state machine can be used 

![DFA State Machine](/finite-automaton.png)

where s0... s4 are the states s0 being the start start and s4 the matching state

Given a string like `abbbba` as the input the machine will follow the following paths starting from the start state `s0`
at each stage the input being read will propel the state machine to the next state ending in the matching state. If at any 
given state the input being read doesn't transition the machine to the next state it halts

The state described above is what is called deterministic finite automat(a|on). Its deterministic because at any given 
state the input will propel us to atmost one new state
Machines that are forced to choose between two states to transition into are non-deterministic and are called NFA for 
non-deterministic finite automata.

The above diagram can be converted to an NFA by branching on `s2` rather than `s3`
![NFA State Machine](/finite-automaton.png)

     a           b           b          a 
s0 ------> s1 -------> s2 -------> s3 ------> s4
           |............|
                b

If it then reads a `b` in `s2` it can either go to a in hopes of reading `bb` or `s3` in hopes of reading an `a` but since
it can't look a head it can't possibly know. This is an NFA. Its therefore important to let the NFA guess correctly the next state.
Sometimes its important for NFAs to have branches to follow without any input. At anytime an NFA can choose to follow a path without an input
Changing the above NFA to add unlabelled path 

     a           b           b          a 
s0 ------> s1 -------> s2 -------> s3 ------> s4
           |.......................|

This concisely describes `a(bb)+a` as compared to the previous one

# Converting RE to NFA

REs turn out to have same exact power with NFA i.e NFAs can generate REs and vice versa.
For example an NFA to describe a character would look like 
    a
s0 ----->            = describes a character `a`

    e1         e2
s0 -----> s1 ------> = describes concatenation `e1e2`

      e1
   -------> s1
   |                 = identifies `e1|e2`
s0 |  e2
   |------> s3

Notice the dangling pointers, they will later be glued together 
NFAs for `e*` `e?` and `e+` can also be constructed.
Theres is one NFA for each re expression excluding the parenthesis.
The process of converting REs to NFAs was first described by Ken Thompson

# Regular Expression search algorithms
To test whether the RE matches the string convert the RE to NFA and then run the string on the NFA and 
if you end up in an accepting state then that RE matches the string. NFAs can guess the paths to follow given 
two conflicting paths. 
