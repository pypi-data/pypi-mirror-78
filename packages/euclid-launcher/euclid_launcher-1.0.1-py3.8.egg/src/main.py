#!/usr/bin/env python3

import click
import json
import os
import pathlib
import multiprocessing
import requests
import yaml

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


def run_group(name, group, **kwargs):
    say(f"Executing group {name}")

    if kwargs.get('parallel', False):
        return run_group_parallel(group, **kwargs)

    for command in group:
        run_command(command)


def run_web(link, **kwargs):
    global commands

    obj = yaml.safe_load(requests.get(link).text)
    group_name = list(obj.keys())[0]
    commands_list = list(obj[group_name].keys())

    for command in commands_list:
        commands[command] = obj[group_name][command]

    kwargs.pop('web')
    run_group(group_name, commands_list, **kwargs)


def run_command(name, **kwargs):
    if kwargs.get('web', False):
        return run_web(name, **kwargs)

    if name not in commands:
        say(f"Command {name} not found.", 'error')
        return 10

    command = commands[name]

    if type(command) is list:
        run_group(name, command, **kwargs)
    else:
        os.system(command)

    return 0


def export_command(name):
    if name not in commands:
        say(f"Command {name} not found.", 'error')
        return 10

    command = commands[name]
    group_name = name
    obj = {group_name: {}}

    if type(command) is not list:
        obj[group_name][group_name] = command
    else:
        for c in command:
            obj[group_name][c] = commands[c]

    print(yaml.dump(obj))


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
@click.option('--web', '-w', is_flag=True, default=False)
@click.option('--parallel', '-p', is_flag=True, default=False)
def run(name, **kwargs):
    run_command(name, **kwargs)


@main.command()
@click.argument('name')
def export(name):
    export_command(name)


@main.command()
@click.argument('group_name')
@click.argument('command_string')
def group(group_name, command_string):
    group_command(group_name, command_string)
