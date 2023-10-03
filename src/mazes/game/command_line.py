import argparse
import logging
import sys

from .game_loop import GameLoop


class CommandError(Exception):
    pass


class CommandLine:
    def __init__(self) -> None:
        self._log_option: str | None = None

    def execute(self) -> int:
        try:
            self.parse_arguments()
            self.run()
            return 0
        except CommandError as e:
            message = e.args[0]
            sys.stderr.write(f"{message}\n")
            result = e.args[1] if len(e.args) == 2 else 1
            return result

    def parse_arguments(self) -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-L",
            "--log",
            choices=["debug", "info", "warning", "error"],
            default="warning",
        )

        args = parser.parse_args()

        self._log_option = args.log

    def run(self) -> None:
        logging.basicConfig(level=self.log_level)
        game_loop = GameLoop()
        game_loop.execute()

    @property
    def log_level(self) -> int:
        match self._log_option:
            case "debug":
                return logging.DEBUG

            case "info":
                return logging.INFO

            case "warning":
                return logging.WARNING

            case _:
                return logging.WARNING


def main() -> int:
    cli = CommandLine()
    return cli.execute()
