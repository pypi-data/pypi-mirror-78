#!/bin/env python
# ## The python way : bmd.py
# ## Installing
#
# `bmd` is published on *PyPi* under the `bmd-py` package.
# You should be able to install it with:
#
# ```sh
# pip install bmd-py
# bmd.py --help
# ```sh
#
# ### How it works?
#
# The python script do the same thing as the bash one but without `sed`, it uses `regex` instead
#
# ```py
import click
import regex

SHEBANG_REGEX = r'^#!'
REGEX_HELP='Specify the TEXT regex pattern to remove.'

@click.command()
@click.argument('input')
@click.option('-r', '--regex', 'pattern', default='^# ?', show_default=True, help=REGEX_HELP)
def bmd(input, pattern):
  """Change the script file INPUT to a Markdown documentation."""
  with open(input) as f:
    output = []

    for line in f:
      if not regex.match(SHEBANG_REGEX, line):
        if regex.match(pattern, line):
          output.append(
            regex.sub(pattern, '', line)
          )
        else:
          output.append(line)

    print(''.join(output), end='')

if __name__ == '__main__':
    bmd()
# ```
