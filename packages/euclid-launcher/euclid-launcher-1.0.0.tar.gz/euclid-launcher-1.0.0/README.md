# Euclid

A project manager and script launcher made in Python.

## Commands

Commands are simple one-line bash scripts that will be saved for execution later.

### Add command

```bash
euclid add <script-name> "<script>"
```

Example:

```bash
euclid add hello-world "echo Hello World"
```

### Running commands

```bash
euclid run <script-name>
```

Example:

```bash
euclid run hello-world
```

## Groups

For running many commands together, you can group them.\
Running a group will run all the commands <b>synchronously</b> by default, however you can use the <b>parallel flag</b> that is shown down below.

### Add group

```bash
euclid group <group-name> "<script1-name> <script2-name>"
```

Example:

```bash
euclid group hi-all "hello-world hello-you"
```

### Running Groups

```bash
euclid run <group-name>
```

Example:

```bash
euclid run hi-all
```

### Running Groups in Parallel

```bash
euclid run -p <group-name>
# or
euclid run --parallel <group-name>
```
