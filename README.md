# Melkman

## Dependencies

* [Tcl/Tk](http://tcl.sourceforge.net/)

## Run (CLI)

~~~sh
python main.py
~~~

## Modes

* **Interactive**: the user adds/removes points to form a simple polygonal chain.
Each point is processed by the Melkman algorithm to determine if it contributes
to the convex hull.
* **Step**: a simple polygonal chain is generated. Points can be processed one
at a time by the Melkman algorithm. Points can also be removed from the hull.
* **Test**: test the algorithm's robustness by applying it to 5000 generated
simple polygonal chain.
