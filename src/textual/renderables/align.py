from __future__ import annotations

from rich.console import Console, ConsoleOptions, RenderableType, RenderResult
from rich.measure import Measurement
from rich.segment import Segment
from rich.style import Style

from ..geometry import Size
from ..css.types import AlignHorizontal, AlignVertical
from .._segment_tools import align_lines


class Align:
    def __init__(
        self,
        renderable: RenderableType,
        size: Size,
        style: Style,
        horizontal: AlignHorizontal,
        vertical: AlignVertical,
    ) -> None:
        self.renderable = renderable
        self.size = size
        self.style = style
        self.horizontal = horizontal
        self.vertical = vertical

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        lines = console.render_lines(self.renderable, options, pad=False)

        new_line = Segment.line()
        for line in align_lines(
            lines,
            self.style,
            self.size,
            self.horizontal,
            self.vertical,
        ):
            yield from line
            yield new_line

    def __rich_measure__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> Measurement:
        width, _ = self.size
        return Measurement(width, width)
