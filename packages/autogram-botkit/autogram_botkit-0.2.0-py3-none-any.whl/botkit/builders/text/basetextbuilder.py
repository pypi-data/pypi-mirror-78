from typing import Any


class BaseTextBuilder:
    def __init__(self):
        self.parts = []

    def raw(self, text: Any, end=""):
        return self._append_with_end(text, end)

    def spc(self):
        self.parts.append(" ")
        return self

    def br(self):
        self.parts.append("\n")
        return self

    def para(self):
        self.parts.append("\n\n")
        return self

    def _append(self, text: str):
        self.parts.append(text)
        return self

    def _append_with_end(self, text: str, end: str):
        self.parts.append(self._apply_end(text, end))
        return self

    @staticmethod
    def _apply_end(text: str, end: str) -> str:
        if text is None:
            raise ValueError("Trying to append None value.")

        text = str(text)
        end = str(end)

        if text is None:
            raise ValueError(f"Cannot append '{text}' to message.")
        if end == "":
            return text
        else:
            return text + end

    def render(self) -> str:
        if not self.parts:
            return ""
        return "".join(self.parts)
