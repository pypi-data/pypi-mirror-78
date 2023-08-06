# Vivarium

**WARNING: This project is deprecated and no longer maintained.** Please
use
[`vivarium-core`](https://github.com/vivarium-collective/vivarium-core)
and
[`vivarium-cell`](https://github.com/vivarium-collective/vivarium-cell)
instead.

Vivarium is a multiscale platform for simulating cells in dynamic
environments, within which they can grow, divide, and thrive.

![vivarium](doc/_static/snapshots_fields.png)

## Documentation and Tutorials
Visit [Vivarium documentation](https://wc-vivarium.readthedocs.io/)

## Concept

A Vivarium is a "place of life" -- an enclosure for raising organisms in controlled environments for observation or
research. Typical vivaria include aquariums or terrariums.  The vivarium provided in this repository is a computational
vivarium for developing colonies of whole-cell model agents in dynamic environments. Its framework is a synthesis of
whole-cell modeling, agent-based modeling, multi-scale modeling, and modular programming.

Vivarium is a framework for composing hybrid models of different cellular processes into agents, and placing many agents
into a shared spatial environment to observe their interactions. Vivarium is distributed in that these agents can run in
different threads or on different computers, and upon cell division new threads are allocated. The agents communicate
through message passing and are coordinated by the environmental simulation which receives all of the messages,
integrates them, and responds to each agent with their new updated local environments.
