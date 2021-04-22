#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC
import logging

from .helpers import long_sleep, shutdown_requested, set_running, unset_running


class AbstractManager(ABC):

    script_name: str

    def __init__(self, loglevel: int=logging.DEBUG):
        self.loglevel = loglevel
        self.logger = logging.getLogger(f'{self.__class__.__name__}')
        self.logger.setLevel(loglevel)
        self.logger.info(f'Initializing {self.__class__.__name__}')

    async def _to_run_forever_async(self) -> None:
        pass

    def _to_run_forever(self) -> None:
        pass

    def run(self, sleep_in_sec: int) -> None:
        self.logger.info(f'Launching {self.__class__.__name__}')
        while True:
            if shutdown_requested():
                break
            try:
                set_running(self.script_name)
                self._to_run_forever()
            except Exception:
                self.logger.exception(f'Something went terribly wrong in {self.__class__.__name__}.')
            finally:
                unset_running(self.script_name)
            if not long_sleep(sleep_in_sec):
                break
        self.logger.info(f'Shutting down {self.__class__.__name__}')
