# The Transistor

The core of most computers today are constructed out of MOS transistor. MOS stand for metal-oxide semiconductor. The elctrical properties of metal-oxide semiconductor are well beyond the scope of what we want to understand. The are our lowest level of abstraction which means
if the transistors start misbehaving we are at their mercy.


Still it is useful to know that there are two types of MOS transistors P-type and N-Type they both operate very similarly

Instead of a a wall switch we could have an N-type or P-type MOS transistor close or open the ciruit. The transistor has three terminals the source,gate and the drain.


# Logic Gates

A step up higher from the transistor are the the logic gates i.e the AND,OR,NOR,NAND and NOT logic functions. In this chapter we construct transistor circuits that  implement these logics


# NOT gate

This is the simplest logic block. You give it an input of 1 it returns 0 and the same in reverse
To build a not gate from the transitor you you can use a P-type transistor that is if you supply voltage to it it closes the connection if you don't its open.The N-type is the same except in reverse


```verilog
module not(a,b);

input a;
input b;

assign b = ~a;

endmodule
```

# OR and NOR gate

This can be made out of two P-type and two N-type transistors. 
