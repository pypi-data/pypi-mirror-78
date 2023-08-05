import pickle
import hashlib
import logging
import re
import copy
import math

from .utils import *

import logging

from .exceptions import *

class parsers:
  class variables:
    @staticmethod
    def parse_string(text):
      start_tok = "${"
      end_tok = "}"
      si = text.find(start_tok)
      while si >= 0:
        ei = text.find(end_tok,si)
        sii = text.find(start_tok,si+1)
        if sii >= 0 and sii < ei:
          # we found another start token before the end
          si = sii
          continue

        if ei < 0:
          # no end token found
          break

        name = text[si+2:ei].strip()
        yield name,si,ei+1
        si = text.find(start_tok,ei)

  class expressions:
    @staticmethod
    def parse_string(text):
      start_tok = "$("
      end_tok = ")"
      si = text.find(start_tok)
      N = len(text)
      while si >= 0:
        level = 1
        i = si+len(start_tok)-1
        while i < N and level > 0:
          i += 1
          if text[i] == start_tok[-1]:
            level += 1
            continue
          if text[i] == end_tok[0]:
            level -= 1
            continue
        ei = i
          
        if level > 0:
          break

        expression = text[si+2:ei].strip()
        yield expression,si,ei+1
        si = text.find(start_tok,ei)




def variable_expansion(text,context,default=None,do_not_expand_if_value_contains_expression=False):
  expanded_text = ""
  ei = 0
  logger = logging.getLogger('renderconftree')
  for result in parsers.variables.parse_string( text ):
    expanded_text += text[ei:result[1]]
    name = result[0]
    if name in context:
      value = context[name]
      if value is text:
        raise CircularDependency(f"Circular dependency detected. String '{text}' refers to itself.")

      if do_not_expand_if_value_contains_expression:
        if next(parsers.expressions.parse_string(value),None) is None:
          expanded_text += value
        else:
          expanded_text += text[result[1]:result[2]]
      else:
        if result[1] == 0 and result[2] == len(text):
          # the entire string is a variable,
          # we can just return the value
          return value

        expanded_text += str(value)

    else:
      logger.debug(f"Variable '{name}' not found in context.")
      if default is not None:
        expanded_text = str(default)
      else:
        expanded_text += text[result[1]:result[2]]
    ei = result[2]
  expanded_text += text[ei:]
  return expanded_text

allowed_expression_names = {
# We have to explicitly list any name
# (function, variable, etc) that we want to
# be available in the expression evaluation.
# 
# Note that just saying 'math' is allowed
# does not work. Each allowed function needs
# to be listed. We are addeing 'math' and 'm'
# here so that the user can call functions with
# math. or m. prefixed if they like.
    'float' : float,
    'int' : int,
    'abs' : abs,
    'sum' : sum,
    'min' : min,
    'max' : max,
    'round' : round,
# we could set these to None, and the the user
# would have to call them with math. or m. prefixed.
# Setting them to the math functions allows the
# user to call them without the prefix.
    'math' : math,
    'm' : math,
    'acos'     :  math.acos,
    'acosh'     :  math.acosh,
    'asin'      :  math.asin,
    'asinh'     :  math.asinh,
    'atan'      :  math.atan,
    'atan2'     :  math.atan2,
    'atanh'     :  math.atanh,
    'ceil'      :  math.ceil,
    'copysign'  :  math.copysign,
    'cos'       :  math.cos,
    'cosh'      :  math.cosh,
    'degrees'   :  math.degrees,
    'dist'      :  math.dist,
    'erf'       :  math.erf,
    'erfc'      :  math.erfc,
    'exp'       :  math.exp,
    'expm1'     :  math.expm1,
    'fabs'      :  math.fabs,
    'factorial' :  math.factorial,
    'floor'     :  math.floor,
    'fmod'      :  math.fmod,
    'frexp'     :  math.frexp,
    'fsum'      :  math.fsum,
    'gamma'     :  math.gamma,
    'gcd'       :  math.gcd,
    'hypot'     :  math.hypot,
    'isclose'   :  math.isclose,
    'isfinite'  :  math.isfinite,
    'isinf'     :  math.isinf,
    'isnan'     :  math.isnan,
    'isqrt'     :  math.isqrt,
    'ldexp'     :  math.ldexp,
    'lgamma'    :  math.lgamma,
    'log'       :  math.log,
    'log1p'     :  math.log1p,
    'log10'     :  math.log10,
    'log2'      :  math.log2,
    'modf'      :  math.modf,
    'pow'       :  math.pow,
    'radians'   :  math.radians,
    'remainder' :  math.remainder,
    'sin'       :  math.sin,
    'sinh'      :  math.sinh,
    'sqrt'      :  math.sqrt,
    'tan'       :  math.tan,
    'tanh'      :  math.tanh,
    'trunc'     :  math.trunc,
    'prod'      :  math.prod,
    'perm'      :  math.perm,
    'comb'      :  math.comb,
    'pi'        :  math.pi,
    'e'         :  math.e,
    'tau'       :  math.tau,
    'inf'       :  math.inf,
    'nan'       :  math.nan,
    }

def eval_expression(text,allowed_names={}):
  code = compile(text,"<string>","eval")
  for name in code.co_names:
    if name not in allowed_names:
      raise NameError(f"Use of name '{name}' not allowed in expressions.")
  return eval(code, {'__buildins__':{}}, allowed_names )

def expression_substitution(text,context,*,allowed_names=allowed_expression_names,paranoid=False,expand_variables=False):
  if paranoid:
    allowed_names = {}
  expanded_text = ""
  ei = 0
  logger = logging.getLogger('renderconftree')
  for result in parsers.expressions.parse_string( text ):
    expanded_text += text[ei:result[1]]
    expression = result[0]
    # expand any nested expressions first.
    expression = expression_substitution(expression,context,allowed_names=allowed_names,paranoid=paranoid,expand_variables=expand_variables)
    try:
      if expand_variables:
        expression = variable_expansion(expression,context)
      allowed_names['context'] = context
      r = eval_expression(expression,allowed_names)
      if result[1] == 0 and result[2] == len(text):
        # the entire string is an expression,
        # we can just return the result
        return r
      else:
        expanded_text += str(r)
    except Exception as e:
      logger.debug(f"Exception thrown during expression evaluation: {expression} -> {str(e)}")
      expanded_text += text[result[1]:result[2]]
    ei = result[2]
  expanded_text += text[ei:]
  

  return expanded_text

def render_tree( tree, *, modify_in_place=False,allowed_names=allowed_expression_names, strict = False, history = None ):
  '''
  Given a tree data structure (nested dict/list), this function will loop through all all leaf nodes containing expressions
  and replace their value with the result of the expression. Expressions are specified using the bash/zsh command substitution
  syntax, $(...).

  Expressions may contain variable references. Variables references are specified using the bash/zsh variable expansion syntax,
  ${varname}. Variable references may refer to other leaf nodes in the tree and and use a filesystem path style key. For example,
  ${x} woudl refer to an item named 'x' in the on the same branch, but ${/x} would refer to an item named 'x' at the tree root.
  Multiple levels can be given, and references to items "above" are also supported (i.e. ${/example/simulations/x} or ${../x}).
  Variable references will be replaced with value of the node they refer to.

  Rendering is repeated until doing so no longer changes the tree. This allows tree notes to reference another node that itself
  references another node.

  positional arguments:
  tree -- The nested tree data structure to render.

  keyword-only arguments:
  modify_in_place -- If True, the tree will be rendered in place. If False, a copy of the tree will be made first.
  allowed_names -- The scope that will be passed as the to the eval(...)
                   function's local scope. The global scope will be empty, so any variables,
                   functions, classes, etc. that should be available to the expression must be
                   specified here. The default provides some common math functions and modules.
  strict -- If True, check that all expresses were evaluated and throw an exception if any were not.
  history -- Used for debugging. If a list is provided, a copy of the tree after each expression is evaluated will be appended.
  '''
  if type(tree) is fspathtree:
    if modify_in_place:
      rendered_tree = tree
    else:
      rendered_tree = copy.deepcopy(tree)
  else:
    if modify_in_place:
      rendered_tree = fspathtree(tree)
    else:
      rendered_tree = fspathtree(copy.deepcopy(tree))

  # replace expressions
  # - loop through all leaf nodes that are strings.
  # - evaluate each value as an expression.
  # - repeat until all expressions are evaluated, or we enter a circular loop.

  # we use a hash of the tree pickled to detect circular dependencies that would
  # lead to an infinite loops.
  hashes = dict()
  hash =  hashlib.sha1( pickle.dumps(rendered_tree) ).hexdigest()
  hashes[hash] = hashes.get(hash,0) + 1
  while hashes.get( hash, 0 ) < 2: # repeat until we get the same tree twice
    if history is not None:
      history.append( copy.deepcopy(rendered_tree) )
    # loop through all leaf notes that have string values
    for k,v in rendered_tree.get_all_leaf_node_paths(predicate = lambda k,v: type(v) in (str,bytes), transform = lambda k,v : (k,v) ):
      try:
        new_v = variable_expansion(v,rendered_tree[k.parent])
      except CircularDependency as e:
        raise CircularDependency(f"Circular dependency detected. Value '{v}' of key '{k}' refers to itself.")

      if type(new_v) in (str,bytes): # make sure variable expansion didn't return a different type
        new_v = expression_substitution(new_v,rendered_tree[k.parent],expand_variables=True)
      rendered_tree[k] = new_v
    hash =  hashlib.sha1( pickle.dumps(rendered_tree) ).hexdigest()
    hashes[hash] = hashes.get(hash,0) + 1

  if strict: # check for un-evaluated expressions or variables
    unparsed_exps_and_vars = []
    for k,v in rendered_tree.get_all_leaf_node_paths(predicate = lambda k,v: type(v) in (str,bytes), transform = lambda k,v : (k,v) ):
      unparsed_exps_and_vars += [ r[0] for r in parsers.expressions.parse_string(v) ]
      unparsed_exps_and_vars += [ r[0] for r in parsers.variables.parse_string(v) ]
    if len(unparsed_exps_and_vars) > 0:
      raise UnparsedExpressions("Failed to replace one or more expressions or variables: "+str(unparsed_exps_and_vars))

  return rendered_tree







