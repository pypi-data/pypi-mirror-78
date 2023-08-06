#!/usr/bin/env python3
"""A script that converts mulitple inputs of a java function to a single
Autovalue params class.

This script DOES NOT UNDERSTAND THE JAVA LANGUAGE. It simply uses some simple
parsing. Make sure you look at the result before using the code.

For the usages below, assume we have a class called MyConverter and the
following files:

# sample_function_defs.txt (you don't need the full body if you don't use
# --transform_func_def_with_autovalue option)

  String convertFunc(boolean f1, Optional<String> f2, Optional<Integer> f3, boolean f4) {
    print(f1);
    print(f2);
    print(f3);
    print(f4);
    return "nothing";
  }

# sample_function_defs_without_body.txt

  String convertFunc(boolean f1, Optional<String> f2, Optional<Integer> f3, boolean f4) {

# sample_convert_method_calls_in_test_file.txt (this can be the whole test file)

public void assert1() {
  assertThat(
      converter.convertFunc(
        /* f1= */ false,
        /* f2= */ Optional.empty(),
        Optional.of(123),
        /* f4= */ true)
      ).isEqualTo("nothing");
}

# sample_convert_call_site_file.txt (this should only contain the call site invocation)

converter.convertFunc(false, Optional.empty(), Optional.of(4), true);

# end of all files

Usage: python3 sorno_input_params_autovalue_converter.py sample_function_defs.txt --output_autovalue_class

Output the definition of the autovalue class.
### begin of output
import com.google.auto.value.AutoValue;

/** Input parameters for convertFunc. */
@AutoValue
public abstract static class Params {

  public abstract boolean f1();

  public abstract Optional<String> f2();

  public abstract Optional<Integer> f3();

  public abstract boolean f4();

  public static Builder builder() {
      // TODO
      return new AutoValue_Params.Builder()
    .setF1(false)
    .setF4(false);
  }

  abstract Builder toBuilder();

  /** Builder for {@link Params} */
  @AutoValue.Builder
  public abstract static class Builder {

    public abstract Builder setF1(boolean f1);

    public abstract Builder setF2(Optional<String> f2);

    public abstract Builder setF3(Optional<Integer> f3);

    public abstract Builder setF4(boolean f4);

    public abstract Params build();
  }
}
### end of output

Usage: python3 sorno_input_params_autovalue_converter.py sample_function_defs.txt --transform_func_def_with_autovalue

Transform the function definition to use the generated autovalue class.

### begin of output

  String convertFunc(Params params)) {
    print(params.f1());
    print(params.f2());
    print(params.f3());
    print(params.f4());
    return "nothing";
  }

### end of output

Usage: python3 sorno_input_params_autovalue_converter.py sample_function_defs.txt --convert_method_calls_in_test_file sample_convert_method_calls_in_test_file.txt

Convert method calls in a test file to use the autovalue class.

### begin of output

public void assert1() {
  assertThat(
      converter.convertFunc(Params.builder()
.setF3(Optional.of(123))
.setF4(true)
.build())
      ).isEqualTo("nothing");
}

### end of output

Usage: python3 sorno_input_params_autovalue_converter.py sample_function_defs.txt --convert_call_site_file sample_convert_call_site_file.txt

Convert the original call invocation to use the autovalue class.

### begin of output

converter.convertFunc(Params.builder()
.setF1(false)
.setF2(Optional.empty())
.setF3(Optional.of(4))
.setF4(true)
.build());

### end of output

    Copyright 2020 Heung Ming Tai
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
        http://www.apache.org/licenses/LICENSE-2.0
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import argparse

import re
import sys
import subprocess
from collections import namedtuple


fields = ('type', 'name', 'default_value')
Param = namedtuple('Param', fields, defaults=(None,) * len(fields))

AUTO_VALUE_CLASS_NAME = 'Params'

AUTO_VALUE_GET_METHOD_TEMPLATE = 'public abstract {type} {method_name}();'

AUTO_VALUE_SET_METHOD_TEMPLATE = 'public abstract Builder {method_name}({type} {param_name});'
AUTO_VALUE_CLASS_TEMPLATE = """\
import com.google.auto.value.AutoValue;

/** Input parameters for {func_name}. */
@AutoValue
public abstract static class {autovalue_class_name} {{
  {get_methods_defs}

  public static Builder builder() {{
      // TODO
      return new AutoValue_{autovalue_class_name}.Builder(){build_default_calls};
  }}

  abstract Builder toBuilder();

  /** Builder for {{@link {autovalue_class_name}}} */
  @AutoValue.Builder
  public abstract static class Builder {{
    {set_methods_defs}

    public abstract {autovalue_class_name} build();
  }}
}}
"""


class App(object):
    def __init__(self, args):
      self.args = args
      self.func_def_input_file = args.func_def_input_file

    def run(self):
      func_def_str = open(self.func_def_input_file).read()
      func_name = get_func_name(func_def_str)
      params = get_params(func_def_str)

      if self.args.output_autovalue_class:
        print_autovalue_class(self.get_autovalue_class_name(), func_name, params)

      if self.args.convert_method_calls_in_test_file:
        content = open(self.args.convert_method_calls_in_test_file).read()
        print(replace_content_for_test_file(self.get_autovalue_class_name(), func_name, params, content))

      if self.args.convert_call_site_file:
        content = open(self.args.convert_call_site_file).read()
        print(replace_content_for_call_site_file(self.get_autovalue_class_name(), func_name, params, content))

      if self.args.transform_func_def_with_autovalue:
        print(transform_func_def(self.get_autovalue_class_name(), func_name, params, func_def_str))

      return 0

    def get_autovalue_class_name(self):
      return self.args.autovalue_class_name


def get_func_name(s):
  """
  Gets the function name from a string.

  E.g. "void func(type f1)" -> "func"
  """
  pre_open_paren_str = s.split('(')[0]
  if ' ' not in pre_open_paren_str:
    return pre_open_paren_str

  return pre_open_paren_str[pre_open_paren_str.rindex(' ') + 1:]


def get_params(s):
  """
  Gets the list of input parameters (class Param) from a string.

  E.g. "void func(int f1, String f2)" -> [Param(...), Param(...)]
  """
  post_open_paren_str = s.split('(', 1)[1]
  params_str = get_until_close_paren(post_open_paren_str)
  params_strs = [s.strip() for s in params_str.split(',')]

  params = []
  for param_str in params_strs:
    # Need to prevent the case that the type and parameter names are separated
    # by newlines or more than one spaces, so replace all whitespaces to
    # single space.
    param_fragments = re.sub(r'\s+', ' ', param_str).split(' ')
    t, param_name = param_fragments[-2], param_fragments[-1]
    if t == 'Boolean':
      t = 'boolean'

    if t == 'boolean':
      param = Param(type=t, name=param_name, default_value='false')
    else:
      param = Param(type=t, name=param_name)

    params.append(param)

  return params


def get_until_close_paren(s):
  """
  Gets the string up to the closing parenthesis ')', bypassing all pairs
  of parentheses in-betwee.

  E.g. "false, (long) 123, 4).getSomething()" -> "false, (long) 123, 4"
  """
  open_paren_count = 0
  for i in range(len(s)):
    c = s[i]
    if c == ')':
      if open_paren_count:
        open_paren_count -= 1
      else:
        return s[:i]
    elif c == '(':
      open_paren_count += 1

  # no idea what to do, so just return s
  return s


def print_autovalue_class(autovalue_class_name, func_name, params):
  get_methods_defs_strs = []
  set_methods_defs_strs = []
  build_default_calls_strs = []
  for param in params:
    get_methods_defs_strs.append(AUTO_VALUE_GET_METHOD_TEMPLATE.format(
        type=param.type,
        method_name=param.name,
    ))

    set_method_name = 'set' + upperfirst(param.name)
    set_methods_defs_strs.append(AUTO_VALUE_SET_METHOD_TEMPLATE.format(
        method_name=set_method_name,
        type=param.type,
        param_name=param.name,
    ))

    if param.default_value:
      build_default_calls_strs.append('.{set_method_name}({value})'.format(
          set_method_name=set_method_name,
          value=param.default_value,
      ))

  get_methods_defs = '\n'.join(['\n  ' + s for s in get_methods_defs_strs])
  set_methods_defs = '\n'.join(['\n    ' + s for s in set_methods_defs_strs])

  build_default_calls = ''.join(['\n    ' + s for s in build_default_calls_strs])

  print(AUTO_VALUE_CLASS_TEMPLATE.format(
      autovalue_class_name=autovalue_class_name,
      func_name=func_name,
      get_methods_defs=get_methods_defs,
      set_methods_defs=set_methods_defs,
      build_default_calls=build_default_calls,
  ))


def upperfirst(s):
  return s[0].upper() + s[1:]


def replace_content_for_test_file(autovalue_class_name, func_name, params, content):
  func_name_anchor = '.' + func_name + '('
  output = ""
  while func_name_anchor in content:
    # E.g. "abcd blah.func(f1, f2, f3) hello"
    # is splitted to "abcd blah" and "f1, f2, f3) hello"
    pre, post = content.split(func_name_anchor, 1)

    # E.g. "f1, f2, f3"
    input_args_str = get_until_close_paren(post)
    replaced_input_args = replace_test_input_args_with_autovalue_class(autovalue_class_name, input_args_str, params)
    output += pre + func_name_anchor + replaced_input_args
    content = post[len(input_args_str):]

  # need to append the remaining content which does not have the func name
  # anchor
  output += content

  return output


def replace_content_for_call_site_file(autovalue_class_name, func_name, params, content):
  func_name_anchor = '.' + func_name + '('
  output = ""
  while func_name_anchor in content:
    # E.g. "abcd blah.func(f1, f2, f3) hello"
    # is splitted to "abcd blah" and "f1, f2, f3) hello"
    pre, post = content.split(func_name_anchor, 1)

    # E.g. "f1, f2, f3"
    input_args_str = get_until_close_paren(post)
    replaced_input_args = replace_input_args_with_autovalue_class(autovalue_class_name, input_args_str, params)
    output += pre + func_name_anchor + replaced_input_args
    content = post[len(input_args_str):]

  # need to append the remaining content which does not have the func name
  # anchor
  output += content

  return output


def replace_test_input_args_with_autovalue_class(autovalue_class_name, input_args_str, params):
  """
  Replaces input arguments string with an object of the autovalue class.
  Because this is for the test file, we assume "false" and "Optional.empty()"
  are not significant.

  E.g. "false, 3, Optional.empty(), "abc", true" -> "Params.builder()
    .setF2(3)
    .setF4("abc")
    .setF5(true)
    .build()
  """
  # E.g. "12, /* comment= */ 34, 45" -> ["12", "34", "45"]
  input_arg_strs = parse_input_arg_strs(input_args_str)
  output = autovalue_class_name + ".builder()"
  cleaned_arg_strs = [clean_input_arg(s) for s in input_arg_strs]

  for arg, param in zip(cleaned_arg_strs, params):
    if can_skip_arg(arg):
      continue
    output += "\n.set%s(%s)" % (upperfirst(param.name), arg)
  output += "\n.build()"
  return output


def replace_input_args_with_autovalue_class(autovalue_class_name, input_args_str, params):
  """
  Replaces input arguments string with an object of the autovalue class.

  E.g. "false, 3, Optional.empty(), "abc", true" -> "Params.builder()
    .setF1(false)
    .setF2(3)
    .setF3(Optional.empty())
    .setF4("abc")
    .setF5(true)
    .build()
  """
  # E.g. "12, /* comment= */ 34, 45" -> ["12", "34", "45"]
  input_arg_strs = parse_input_arg_strs(input_args_str)
  output = autovalue_class_name + ".builder()"
  cleaned_arg_strs = [clean_input_arg(s) for s in input_arg_strs]

  for arg, param in zip(cleaned_arg_strs, params):
    output += "\n.set%s(%s)" % (upperfirst(param.name), arg)
  output += "\n.build()"
  return output


def parse_input_arg_strs(s):
  """
  Parses the input values out from a string.

  E.g. "12, /* comment= */ 34, func(8,9)" ->
    ["12", "/* comment= */ 34", "func(8,9)"]
  """
  input_arg_strs = []
  sofar = []
  num_open_parens = 0
  for c in s:
    if c == ',' and not num_open_parens:
      input_arg_strs.append(''.join(sofar))
      sofar.clear()
      continue

    sofar.append(c)
    if c == '(':
      num_open_parens += 1
    if c == ')':
      num_open_parens -= 1

  if sofar:
    input_arg_strs.append(''.join(sofar))

  return input_arg_strs


def clean_input_arg(s):
  # strip out comments
  if "*/" in s:
    s = s.split("*/", 1)[1]

  return s.strip()


def can_skip_arg(arg):
  return arg in ("false", "Optional.empty()")


def transform_func_def(autovalue_class_name, func_name, params, func_def_str):
  """
  Transforms a function defintion with the the use of an auto value class.

  It does the following:
    1) Replace the input parameters with the auto value class alone.
    2) Replace all instances of the input parameters with the fetching
       of the corresponding fields from the params object.

  For example, given the following function definition:

  String convertFunc(type1 f1, type2 f2) {
    return f1 + f1 + f2;
  }

  It becomes (assuming the autovalue class name is Params):

  String convertFunc(Params params) {
    return params.f1() + params.f1() + params.f2();
  }
  """
  output = ""
  params_var_name = "params"

  # The example is splitted into:
  # "String convertFunc" and "type1 f1, type2 f2) {..."
  pre, post_open_paren_str = func_def_str.split('(', 1)
  output += pre
  output += "(%s %s)" % (autovalue_class_name, params_var_name)

  # params_str is "type1 f1, type2"
  params_str = get_until_close_paren(post_open_paren_str)
  # Skipped the params_str.
  # post_input_params_str is " {
  #   return f1 + f1 + f2;
  # }"
  post_input_params_str = post_open_paren_str[len(params_str) + 1:]

  for param in params:
      # Replaces all param name with a fetch of a field from the
      # autovalue class. E.g. "f1 + f2" -> "params.f1() + params.f2()".
      post_input_params_str = re.sub(
        r"\b%s\b" % param.name,
        "%s.%s()" % (params_var_name, param.name),
        post_input_params_str,
      )

  output += post_input_params_str
  return output


def parse_args(cmd_args):
  description = __doc__.split("Copyright 2018")[0].strip()

  parser = argparse.ArgumentParser(
    description=description,
    formatter_class=argparse.RawDescriptionHelpFormatter,
  )
  parser.add_argument("func_def_input_file", help="A file with the function definition")
  parser.add_argument("--autovalue_class_name", default=AUTO_VALUE_CLASS_NAME)
  parser.add_argument(
    "--output_autovalue_class",
    action="store_true",
    help="Output the definition of the autovalue class.")
  parser.add_argument(
    "--convert_method_calls_in_test_file",
    help="Convert method calls in a test file to use the autovalue class.")
  parser.add_argument(
	"--convert_call_site_file",
    help="Convert the original call invocation to use the autovalue class.")
  parser.add_argument(
    "--transform_func_def_with_autovalue", action="store_true",
    help="Transform the function definition by using the autovalue class.")

  args = parser.parse_args(cmd_args)
  return args


def main():
  args = parse_args(sys.argv[1:])

  app = App(args)
  sys.exit(app.run())


if __name__ == '__main__':
  main()
