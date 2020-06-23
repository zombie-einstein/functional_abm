==============
Functional ABM
==============

Prototype Functional Agent Based Modelling API

Introduction
============

This is a prototype attempt to create a simple modelling API
based on graph computation and functional patterns, where
most ABM use OOP based patterns (probably rightly so!).

Though the resulting pattern is not strictly speaking
*functional* (it ended altering the state of the model in place)
it does provide a convenient API for quickly building
models.

Usage
=====
*Several examples of a few basic models can be found in the*
`\examples` *folder*

Agents are defined by an update function that defines
how an agent updates it's state each time it is activated
during the simulation.

Once decorated this function is wrapped as part of a
recurrent computational graph connecting agents in a causal
manner.

Update functions should follow this pattern:

.. code-block::

    def update(t, antecedents, state, descendants):
        # Perform updates
        return next_step

Where the arguments are:

- **t:** The current time/step of the simulation
- **antecedents:** Input states that precede this agent
- **state:** The state owned by (and updated by) this node
- **descendants:** Nodes downstream of this agent, that can
  also be altered by this node

the update function should alter the agents state
(and any descendants were applicable) in place and then
only return the next time/step the agent will be activated.

Decorating an update function wth the `agent` decorator
creates a new `type` wrapping the update function and
allowing states to be assigned as arguments to each instance
of an agent using the update function.

Multiple agents types can be created using multiple update
functions, and arbitrary structures used to hold the state
of the model (numpy arrays, graphs etc.).
