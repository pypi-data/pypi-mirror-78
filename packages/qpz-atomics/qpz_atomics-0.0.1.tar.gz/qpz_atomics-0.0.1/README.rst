===========
qpz_atomics
===========


This library provides atomic functions implementations and make them available to several quantum simulation backends.


Description
===========

* Status

The library is under active development but in a very ealy stage. 


* Design principles

-   Backend mappings
-   Modularity
-   Tests


* Usage

Look at the `examples/examples.py` file. The library is instantiated for each node (as if the nodes were independent computers, each loading its version of the library). 

Other sources of inspirations are the tests defined in the `tests` directory

New atomic functions will be added following the list established by extracting atomic functions from the Quantum Protocol Zoo.
