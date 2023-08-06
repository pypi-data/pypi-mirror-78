#!/usr/bin/env python3

import click
import json
import os
import pathlib
import multiprocessing

from .utils import say, get_command_path, get_data_path, colored

commands = {}


def check_folders():
    data_path = get_data_path()
    if not os.path.exists(data_path):
        os.makedirs(data_path, exist_ok=True)
        with open(get_command_path(), 'w+') as f:
            f.write(json.dumps({}))


def load_commands():
    global commands
    path = get_command_path()

    with open(path, 'r') as f:
        try:
            commands = json.loads(f.read())
        except:
            commands = {}


def save_commands():
    global commands

    with open(get_command_path(), 'w+') as f:
        f.write(json.dumps(commands))


def add_command(name, script):
    commands[name] = script
    save_commands()
    say(f"Command {name} saved!", "success")
    say("Type " + colored(f"euclid run {name}", "white",
                          attrs=["underline"]) + " to execute it.")


def group_command(group_name, command_string):
    global commands

    command_array = command_string.split(" ")

    for command in command_array:
        if command not in commands:
            say(f"Command {command} not found.", 'error')
            say(f"Group won't be created.", 'error')
            return -1

    commands[group_name] = command_array

    save_commands()
    say(f"Group {group_name} saved!", "success")
    say("Type " + colored(f"euclid run {group_name}", "white",
                          attrs=["underline"]) + " to execute it.")


def run_group_parallel(group, **kwargs):
    process_pool = multiprocessing.Pool(processes=len(group))
    process_pool.map(run_command, group)


def run_group(group, **kwargs):
    if kwargs.get('parallel', False):
        return run_group_parallel(group, **kwargs)

    for command in group:
        run_command(command)


def run_command(name, **kwargs):
    if name not in commands:
        say(f"Command {name} not found.", 'error')
        return 10

    command = commands[name]

    if type(command) is list:
        say(f"Executing group {name}")
        run_group(command, **kwargs)
    else:
        os.system(command)

    return 0


@click.group()
@click.version_option("1.0.0")
def main():
    check_folders()
    load_commands()


@main.command()
@click.argument('name')
@click.argument('script')
def add(name, script):
    add_command(name, script)


@main.command()
@click.argument('name')
@click.option('--parallel', '-p', is_flag=True, default=False)
def run(name, **kwargs):
    run_command(name, **kwargs)


@main.command()
@click.argument('group_name')
@click.argument('command_string')
def group(group_name, command_string):
    group_command(group_name, command_string)
