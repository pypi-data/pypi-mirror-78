#!/bin/env python
# ## The python way : bmd.py
# ### How it works?
#
# The python script do the same thing as the bash one but without `sed`, it uses `regex` instead
#
# ```py 
import click
import regex

SCRIPT_COMMENT_REGEX = r'^# ?'
SHEBANG_REGEX = r'^#!'

@click.command()
@click.argument('input')
def bmd(input):
  """Change the INPUT script to a Markdown documentation"""
  with open(input) as f:
    output = []

    for line in f:
      if (regex.match(SHEBANG_REGEX, line)):
        continue
      elif (regex.match(SCRIPT_COMMENT_REGEX, line)):
        output.append(
          regex.sub(SCRIPT_COMMENT_REGEX, '', line)
        )
      else:
        output.append(line)

    print(''.join(output), end='')

if __name__ == '__main__':
    bmd()
# ```
