# Render Configuration Files

Configure your application with rendered configuration trees. I.e., configuration trees that contain leaves with
references to other leaves and computations.

## Features

`renderconftree` is a module that allows you to write configuration files containing python expressions and variable references.
These can be used to do simple variable substitution (have one parameter in your configuration file be automatically
set to the value of another parameter) or more complicated computations (have the value of a parameter
be automatically calculated from one or more other parameters). It has the following features:

  - Recursive parameter substitution. Configuration data is stored in a
    tree-like object (i.e. nested dict/list) and parameter substitution occurs at all levels.
  - Parameter calculation. Configuration data can be computed using Python expressions.
  - It is file format agnostic. `renderconftree` does not parse configuration files. It relies on a "loader".
    If you have a function that can take a string containing the text of your configuration file and return
    a configuration tree (nested dict/list) then you can use `renderconftree`.

## Installation

`renderconftree` is available on PyPi

```
pip install renderconftree
```



## Examples
YAML is a great language for writing configuration files. It is simple to write, configuration options
can be stored in a logical hierarchy, and it is easy to get into your Python code. `renderconftree` simply
adds the power of Python to your YAML file so you can do something like:

    #! /usr/bin/python

    from renderconftree.read import *

    text = '''
    var1 : 1
    var2 : some string
    var3 : 3
    var4 : $(${var3} + math.pi + 2)
    var5 : $(${var4} + 2.0)
    nest1 :
      var1 : 11
      var2 : $(${var3} + 12}}
      var3 : $(${var1} + 12}}
      var4 : $(${var3} + 12}}
      var5 : $(${/nest1/var3} + 12)
    '''


    config = readConfig( text )
    print(yaml.dump(config, default_flow_style=False))

The YAML configuration file is loaded into a nested dictionary/list. Each value in
the tree is then parsed for expressions (text inside of $()).
If an
expression is found it is evaluated (using Python's `eval()` function) and the
parameter value is replaced with the result.
If the expression contains a variable reference
(text inside of ${}) the variables value is inserted into the expression before it is evaluated.
The tree itself is passed into the
evaluation context, so parameters in the dictionary can be accessed
within the expression.

This is extremely useful if you write code that does numerical calculations, like a physics simulation.
Consider the following configuration for a physics simulation that solves the 2D heat equation using a Finite-Difference method. You might have a
configuration file that looks like this.

    # heat solver configuration
    grid:
      x:
        min : 0
        max : 10
        N   : 100
      y:
        min : 0
        max : 20
        N   : 200
    time:
      start : 0
      stop : 10
      dt : 0.001

Now suppose you want to be able to set the grid size (N) based on a desired resolution. You could either 1) modify your code to accept a dx and dy
configuration parameter, or 2) make your configuration file dynamic with `renderconftree`.

    # heat solver configuration
    grid:
      x:
        min : 0
        max : 10
        N   : $( (${max} - ${min})/0.1 )
      y:
        min : 0
        max : 20
        N   : $( (${max} - ${min})/0.1 )
    time:
      start : 0
      stop : 10
      dt : 0.001

If you chose to modify your code to a accept a resolution parameter, you would have to write logic to check which parameter was specified, N or dx. But what
if both where given? This can be especially tedious if your simulation is not written in a scripting language like Python, but in C or C++.
By using `renderconftree`, you keep your configuration logic in your application simple while having power to create configurations that auto-compute
parameter values. What if you want the x and y resolution to be the same, but you would like to be able to easily change it?

    # heat solver configuration
    grid:
      res : 0.001
      x:
        min : 0
        max : 10
        N   : $( (${max} - $(min})/${../res} )
      y:
        min : 0
        max : 20
        N   : $( (${max} - ${min})/${../res} )
    time:
      start : 0
      stop : 10
      dt : 0.001

Note that the `res` parameter is accessed using a filesystem-style path. This is provided by the [`fspathtree` class](https://github.com/CD3/fspathtree), which is a lightweight
wrapper around Python's `dict` and `list` objects that `renderconftree` uses.

Don't like YAML? No problem, just
provide the `readConfig` function with a parser that reads your preferred format from a string and
returns a nested dict. So, to read JSON,

    from renderconftree.read import *
    import json

    with open('myConfig.json', 'r') as f:
      text = f.read()

    config = readConfig( text, parser=json.loads )

Don't want to learn YAML or JSON? Just use INI,

    from renderconftree.read import *
    from renderconftree.parsers import ini
    import json

    with open('myConfig.ini', 'r') as f:
      text = f.read()

    config = readConfig( text, parser=ini.load )


## Command line utility
    
If your application isn't using Python, you can use `renderconftree`. A command-line utility
named `render-config-file` is provided that can read a configuration file,
render the configuration tree, and write it back out. A variety of formats are supported, and
the output format can be different than the input format, so you can even use this script
to translate configuration file formats.
