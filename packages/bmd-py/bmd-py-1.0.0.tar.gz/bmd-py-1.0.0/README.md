# Bash to Markdown Documentation
[![builds.sr.ht status](https://builds.sr.ht/~vlnk/bmd.svg)](https://builds.sr.ht/~vlnk/bmd?)

`bmd` is the dumbest documentation framework you could find on the earth !
It changes your bash scripts into a useful Markdown documentation.

## Features
1. It removes the `shebang` line for an aesthetic output.
2. It removes the `#` string of your bash comments.

> You should **write all your bash comments into a compliant markdown format**, and then *it will work*.

Also, we don't care about all the Markdown flavours. Choose the one for your use cases.

But, let's dissipate all doubts by seeing a compatibility table :

| Flavor         | bmd |
|----------------|-----|
| GFM            | ✅   |
| ExtraMark      | ✅   |
| All the others | ✅   |
## Getting started

Start by documenting a hello world :

```sh
# hello.sh: My Hello World bash script
# ------------------------------------
#
# This **hello world** comes from my *heart*.
# See [Hello World!](https://en.wikipedia.org/wiki/%22Hello,_World!%22_program)
# ```sh
echo "Hello World!"
# ```
```

Indeed, your script code will *never* be compliant with any Markdown formats.

So, the purposed solution is to encapsulate your code in a code block with **the 3 backticks**.
You can specify the script langage, and you'll have a formated code rendering !
The drawback is : your documentation will be an *annoted* bash script.
## The bash way : bmd.sh
### How it works ?

It is 2 `sed` commands. That's all folks.

```sh
bmd () {
  cat ${1} | \
  sed "/^#!/d" | \
  sed "s/^# \?//"
}
```

### How to use it ?

I suggest to do `./bmd.sh bmd.sh`, but please, follow the help :

```sh
usage () {
  echo "bmd - Bash to Markdown Documentation, changes your bash "
  echo ""
  echo "USAGE: ./bmd.sh INPUT"
  echo ""
  echo "Change the INPUT script to a Markdown documentation"
}

if [ ${#} != 1 ]; then
  usage
else
  bmd ${1}
fi
```
## The python way : bmd.py
### How it works?

The python script do the same thing as the bash one but without `sed`, it uses `regex` instead

```py 
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
```
## Contributing

Don't hesitate to submit issues in the [`bmd` tracker](https://todo.sr.ht/~vlnk/bmd).

# Testing
Each new contribution should be applied with an associated **unit test**.
The [`bmd CI`](https://builds.sr.ht/~vlnk/bmd) is triggered on every push.
```makefile
.PHONY: test
test:
	./tasks/test.sh

```
# Documenting
I recommand you to use the `pre-commit` hook in order to always generate the new `README.md` file:

```sh
cd bmd
ln hooks/* .git/hooks/
```
```makefile
.PHONY: doc
doc:
	./tasks/doc.sh 'README.md'

```
# Building and publishing
Check the supported distributions:
+ [python](https://pypi.org/project/bmd-py/)

Don't forget to be logged before publishing a new `bmd` package.
```makefile
.PHONY: build-py
build-py:
	python3 setup.py sdist

.PHONY: check-py
check-py: build-py
	twine check dist/*

.PHONY: publish-py
 publish-py: clean build-py
	twine upload dist/*

clean:
	if [ -d 'dist' ]; then rm -rd 'dist'; fi
	if [ -d 'bmd_py.egg-info' ]; then rm -rd 'bmd_py.egg-info'; fi
```
## Foire aux Questions
+ **Is it a joke ?** Yes, and no. I wrote this for my own usage, I hope it would be useful for your owns.
+ **Is it tested with all the flavours ?** Of course not.
+ **Where did you get this dumb idea ?** From the [`rustdoc`][1] tool.
+ **Is it a meta program?** Drugs help to think about it.

KISS, [@vlnk][2]

[1]: https://doc.rust-lang.org/rustdoc/what-is-rustdoc.html
[2]: https://git.sr.ht/~vlnk/
