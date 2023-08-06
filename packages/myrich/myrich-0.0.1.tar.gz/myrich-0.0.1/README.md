# MyRich
Terminal emulator using [Rich](https://rich.readthedocs.io/en/latest/)

## Installing
Install with pip
```bash
$ pip install myrich
```

## Use
Execute the command `myrich`
```bash
$ myrich
(rich) /home/user/$
```

You use the internal command `markdown` for render a Markdown file
```bash
$ myrich
(rich) /home/user/$markdown README.md
```

### Using the Console
You can render the ouput the any command over rich terminal content
```bash
$ myrich
(rich) /home/user/$cat code.py
```

### Using Emoji
You can render the ouput the any command over rich terminal content
```bash
$ myrich
(rich) /home/user/$echo :smiley:
```