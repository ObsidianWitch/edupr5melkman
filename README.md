# Melkman

## Run (CLI)

~~~sh
python main.py
~~~

# Modes

* **Interactive**: the user adds point to form a simple polygonal chain. Each
point is processed by the Melkman algorithm to determine if it contributes to
the convex hull.
* **Step**: a simple polygonal chain is generated. Then, each time the user left
clicks, a point is processed with the Mekman algorithm.

## Actions

| Inputs     | Actions            |
|------------|--------------------|
| Left click | process next point |
| Tab        | switch mode        |
