# Grab — a unix filter for extracting tokens

Grabs specified tokens from lines on stdin.

`usage: grab.py [-h] command [projection]`

Each character in `command` specifies a token. `grab` will scan the input line for each token in command and print them tab-separated.

If `projection` is specified, only these tokens are printed (0-indexed). Indices are numbers from 0–9.

## Installation

`$ pip install futils-grab`

## Examples

- grab first two numbers from each line: `grab dd`
- grab "-quoted string and number: `grab Qd`
- grab three numbers, print them in reverse order: `grab ddd 210`
- grab client and http status from apache log: `<access.log grab iqd 02`

## Known token types

- *d* (integer)
- *i* (IPv4 address)
- *a* Address (hostname or IP)
- *e* (email address)
- *q* (single-quoted string)
- *Q* (double-quoted string)
- *w* (word)
- *[* (square-bracketed text)

## Override or define new token types

You can define your own token types in `~/.grabrc`, as a JSON object that maps token type (single character) to Python Regex.

```
$ cat ~/.grabrc
{
    "b": "foo.?"
}
```
