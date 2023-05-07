# QEC 2023 Hackathon at ETHZ

This repo contains our solutions to the challenge from Moody's Analytics, where we are expected to use Quantum Monte Carlo to calculate the expected profit of an European Call Option. 

In task 2, we implemented the [Fourier Quantum Monte Carlo Integration](https://quantum-journal.org/papers/q-2022-09-29-823). 

The highlight of our solution is that, in task 3, we proposed an interesting parallelization based on the use of multiple ancilla in the estimation circuit for $\mathbb{E}[cos(n\omega x)]$. Say we use $m$ ancilla. By parallelizing CTRL-Rotation gates acting on different source and target, each shot takes the same time as before, but from each shot we can obtain an $m$-bit measurement result, instead of just $1$. Therefore, we can reduce both the number of shots and the number of times calling the probability encoding circuit by a factor of $m$. This speed-up is limited by the number of discretizing qubit $N$, because $m>N$ leads to idling ancilla at each time step.


