import shlex
import subprocess
from contextlib import contextmanager
from typing import Any, Iterator, List, Sequence

from _pytest.monkeypatch import MonkeyPatch


class CaptureCommand:
    __slots__ = ["monkeypatch", "commands", "outputs"]

    def __init__(self, monkeypatch: MonkeyPatch):
        self.monkeypatch = monkeypatch
        self.commands: List[List[str]] = []
        self.outputs = []

    # This function is designed for capturing the run_subprocess decorator only.
    # It is not intended to capture subprocess.run calls generally. For example,
    # `args` has a much more constrained type than subprocess.run normally allows.
    def _run_stub(self, args: Sequence[str], **_kwargs: Any) -> None:
        self.commands.append(list(args))
        output = self.outputs.pop(0) if self.outputs else None
        return subprocess.CompletedProcess(args=args, returncode=0, stdout=output)

    @contextmanager
    def __call__(self) -> Iterator[None]:
        with self.monkeypatch.context() as mp:
            mp.setattr(subprocess, "run", self._run_stub)
            yield

    def enqueue_outputs(self, *outputs: Sequence[str]) -> None:
        self.outputs.extend(outputs)

    def assert_command(self, *commands: str) -> None:
        assert len(self.commands) == len(commands)
        for (actual, expected) in zip(self.commands, commands):
            assert actual == shlex.split(expected)
