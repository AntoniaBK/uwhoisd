#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from uwhoisd.helpers import get_homedir, check_running
from subprocess import Popen
import time
from pathlib import Path
from typing import Optional, List, Union

import argparse


def launch_cache(storage_directory: Optional[Path]=None) -> None:
    if not storage_directory:
        storage_directory = get_homedir()
    if not check_running('cache'):
        Popen(["./run_redis.sh"], cwd=(storage_directory / 'cache'))


def shutdown_cache(storage_directory: Optional[Path]=None) -> None:
    if not storage_directory:
        storage_directory = get_homedir()
    Popen(["./shutdown_redis.sh"], cwd=(storage_directory / 'cache'))


def launch_whowas(storage_directory: Optional[Path]=None) -> None:
    if not storage_directory:
        storage_directory = get_homedir()
    if not check_running('whowas'):
        Popen(["./run_redis.sh"], cwd=(storage_directory / 'whowas'))


def shutdown_whowas(storage_directory: Optional[Path]=None) -> None:
    if not storage_directory:
        storage_directory = get_homedir()
    Popen(["./shutdown_redis.sh"], cwd=(storage_directory / 'whowas'))


def launch_all() -> None:
    launch_cache()
    launch_whowas()


def check_all(stop: bool=False) -> None:
    backends: List[List[Union[str, bool]]] = [['cache', False], ['whowas', False]]
    while True:
        for b in backends:
            try:
                b[1] = check_running(b[0])  # type: ignore
            except Exception:
                b[1] = False
        if stop:
            if not any(b[1] for b in backends):
                break
        else:
            if all(b[1] for b in backends):
                break
        for b in backends:
            if not stop and not b[1]:
                print(f"Waiting on {b[0]}")
            if stop and b[1]:
                print(f"Waiting on {b[0]}")
        time.sleep(1)


def stop_all() -> None:
    shutdown_cache()
    shutdown_whowas()


def main() -> None:
    parser = argparse.ArgumentParser(description='Manage backend DBs.')
    parser.add_argument("--start", action='store_true', default=False, help="Start all")
    parser.add_argument("--stop", action='store_true', default=False, help="Stop all")
    parser.add_argument("--status", action='store_true', default=True, help="Show status")
    args = parser.parse_args()

    if args.start:
        launch_all()
    if args.stop:
        stop_all()
    if not args.stop and args.status:
        check_all()


if __name__ == '__main__':
    main()
