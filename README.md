# Melkman

## Dependencies

* [pygame](https://www.pygame.org)
* [numpy](http://www.numpy.org/)

## Run (CLI)

~~~sh
python main.py
~~~

## Modes

* **Interactive**: the user adds point to form a simple polygonal chain. Each
point is processed by the Melkman algorithm to determine if it contributes to
the convex hull.
* **Step**: a simple polygonal chain is generated. Then, each time the user left
clicks, a point is processed with the Mekman algorithm.

## Actions

| Inputs     | Actions                                    |
|------------|--------------------------------------------|
| Left click | Process next point                         |
| Tab        | Switch mode                                |
| Shift      | Enable cursor horizontal & vertical guides |
