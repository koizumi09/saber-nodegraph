# Saber Node-Graph
*A Node-Graph based **Visual Programming** wrapper for Python*

Author : Sagar Kowe 

`Saber` is a Node Graph based Visual Programming interface that is essentially a Node Graph implementation through `Excalidraw`, interpreted by a `python` powered backend. 

- Supports all the libraries and built-ins of Python.
- Typing is based off Python's typing.
- Heavily inspired from Unreal Engine's Blueprints and Node editors.

`Saber` is named after my late cat Saber, may she rest in peace. Made free and open source to immortalize her name and contribute to the community.

## Get Started
By default, the excalidraw file being executed is `main.excalidraw` in the root of this repository. All the node graph building goes there.

Run the `main.py` to execute the `main.excalidraw` `Saber` graph.

Learn more about graph scripting in [[Saber Graph Visual Programming Guide.excalidraw]]

## Structure
The execution of the graph is rather straightforward (yet nuanced).

1. First, the imports and global elements are extracted from their respective frames.
2. Every valid element of the drawing is then converted into an object corresponding to its class.
	- Classes are - 
		- `Element` base class
		- `Arrow`, `Pin` and `Node` basic classes
			- `Arrow` - Stores source and target pointed by arrows.
				 - `ValueFlow` : Passing of values
				 - `ControlFlow` : Controls where the control flows
			- `Pin` - Pins for parameters, returns and branching using multiple exec pins
				- `Parameter` : Pin for passing parameter into a function (Node).
				- `Return`: Pin for using the returned value of a function.
				- `Exec`: Pin for when a function can branch of into multiple `ControlFlow`
			- `Node` - Base class for all Functions, Variables and Expressions
				- `Function` - Calls a function based on the text provided. Can take parameters and can give returns. Can branch too.
				- `Variable` - Gets the value of stored variables or updates it using an expression, other variable or function.
				- `Expression` - Standard python expressions. Haven't done much testing but most work.
3. Execution starts from the 'Start' node. 
4. Executes the current node and moves on to the next node.
5. When a node requires a certain value, that value is recursively computed and any functions, variables and expressions needed to generate that value are executed in a chain.

## Developer Notes
All the logic and documentation is further contained within the classes. Definitions are provided in `src/classes`.

Some config data is present in the `__init__.py` script in `src/core`. 
- Script locations can be changed here.
- Colors and stuff can be modified here.
- Also contains some core functions for reading and running the graph.

`nodes.py` has most of the functionality. Also has all the imports, globals and important dictionaries. `variable_map` here stores the scope and key-values of used variables.

`main.py` has an `initialize_node_graph()` function that initially converts every valid element into a node and stores it in a dict `node_graph` in main. Keys are the element IDs and values the objects.