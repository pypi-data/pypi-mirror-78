from typing import List


class ErrorsCollector:
    def __init__(self):
        self.errors: List[str] = []

    def add_error(self, msg: str) -> None:
        self.errors.append(msg)

    def have_errors(self) -> bool:
        return len(self.errors) > 0
