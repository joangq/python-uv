from typing import Callable, Literal, Protocol, Sequence, final
from rich.console import Console
type AnsiColor = Literal[
    "black",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
    "bright_black",
    "bright_red",
    "bright_green",
    "bright_yellow",
    "bright_blue",
    "bright_magenta",
    "bright_cyan",
    "bright_white",
    "grey0",
    "gray0",
    "navy_blue",
    "dark_blue",
    "blue3",
    "blue1",
    "dark_green",
    "deep_sky_blue4",
    "dodger_blue3",
    "dodger_blue2",
    "green4",
    "spring_green4",
    "turquoise4",
    "deep_sky_blue3",
    "dodger_blue1",
    "green3",
    "spring_green3",
    "dark_cyan",
    "light_sea_green",
    "deep_sky_blue2",
    "deep_sky_blue1",
    "spring_green2",
    "cyan3",
    "dark_turquoise",
    "turquoise2",
    "green1",
    "spring_green1",
    "medium_spring_green",
    "cyan2",
    "cyan1",
    "dark_red",
    "deep_pink4",
    "purple4",
    "purple3",
    "blue_violet",
    "orange4",
    "grey37",
    "gray37",
    "medium_purple4",
    "slate_blue3",
    "royal_blue1",
    "chartreuse4",
    "dark_sea_green4",
    "pale_turquoise4",
    "steel_blue",
    "steel_blue3",
    "cornflower_blue",
    "chartreuse3",
    "cadet_blue",
    "sky_blue3",
    "steel_blue1",
    "pale_green3",
    "sea_green3",
    "aquamarine3",
    "medium_turquoise",
    "chartreuse2",
    "sea_green2",
    "sea_green1",
    "aquamarine1",
    "dark_slate_gray2",
    "dark_magenta",
    "dark_violet",
    "purple",
    "light_pink4",
    "plum4",
    "medium_purple3",
    "slate_blue1",
    "yellow4",
    "wheat4",
    "grey53",
    "gray53",
    "light_slate_grey",
    "light_slate_gray",
    "medium_purple",
    "light_slate_blue",
    "dark_olive_green3",
    "dark_sea_green",
    "light_sky_blue3",
    "sky_blue2",
    "dark_sea_green3",
    "dark_slate_gray3",
    "sky_blue1",
    "chartreuse1",
    "light_green",
    "pale_green1",
    "dark_slate_gray1",
    "red3",
    "medium_violet_red",
    "magenta3",
    "dark_orange3",
    "indian_red",
    "hot_pink3",
    "medium_orchid3",
    "medium_orchid",
    "medium_purple2",
    "dark_goldenrod",
    "light_salmon3",
    "rosy_brown",
    "grey63",
    "gray63",
    "medium_purple1",
    "gold3",
    "dark_khaki",
    "navajo_white3",
    "grey69",
    "gray69",
    "light_steel_blue3",
    "light_steel_blue",
    "yellow3",
    "dark_sea_green2",
    "light_cyan3",
    "light_sky_blue1",
    "green_yellow",
    "dark_olive_green2",
    "dark_sea_green1",
    "pale_turquoise1",
    "deep_pink3",
    "magenta2",
    "hot_pink2",
    "orchid",
    "medium_orchid1",
    "orange3",
    "light_pink3",
    "pink3",
    "plum3",
    "violet",
    "light_goldenrod3",
    "tan",
    "misty_rose3",
    "thistle3",
    "plum2",
    "khaki3",
    "light_goldenrod2",
    "light_yellow3",
    "grey84",
    "gray84",
    "light_steel_blue1",
    "yellow2",
    "dark_olive_green1",
    "honeydew2",
    "light_cyan1",
    "red1",
    "deep_pink2",
    "deep_pink1",
    "magenta1",
    "orange_red1",
    "indian_red1",
    "hot_pink",
    "dark_orange",
    "salmon1",
    "light_coral",
    "pale_violet_red1",
    "orchid2",
    "orchid1",
    "orange1",
    "sandy_brown",
    "light_salmon1",
    "light_pink1",
    "pink1",
    "plum1",
    "gold1",
    "navajo_white1",
    "misty_rose1",
    "thistle1",
    "yellow1",
    "light_goldenrod1",
    "khaki1",
    "wheat1",
    "cornsilk1",
    "grey100",
    "gray100",
    "grey3",
    "gray3",
    "grey7",
    "gray7",
    "grey11",
    "gray11",
    "grey15",
    "gray15",
    "grey19",
    "gray19",
    "grey23",
    "gray23",
    "grey27",
    "gray27",
    "grey30",
    "gray30",
    "grey35",
    "gray35",
    "grey39",
    "gray39",
    "grey42",
    "gray42",
    "grey46",
    "gray46",
    "grey50",
    "gray50",
    "grey54",
    "gray54",
    "grey58",
    "gray58",
    "grey62",
    "gray62",
    "grey66",
    "gray66",
    "grey70",
    "gray70",
    "grey74",
    "gray74",
    "grey78",
    "gray78",
    "grey82",
    "gray82",
    "grey85",
    "gray85",
    "grey89",
    "gray89",
    "grey93",
    "gray93"
]

DEFAULT_ACCENT_COLORS: Sequence[AnsiColor] =\
     ("blue", "cyan", "magenta", "yellow")

class Formatter[T](Protocol):
    def __call__(self, value: object, depth: int) -> T: ...
    @staticmethod
    def constant(value: T) -> "Formatter[T]":
        def _(*args: object, **kwargs: object) -> T:
            return value
        return _
    @staticmethod
    def cycle(values: Sequence[T]) -> "Formatter[T]":
        def _(value: object, depth: int) -> T:
            return values[depth % len(values)]
        return _


class AccentColorizer(Formatter[str]):
    def __call__(self, value: object, depth: int) -> str: ...


class PipeFormatter(Formatter[str]):
    def __call__(self, value: object, depth: int) -> str: ...


def rich_colorize(text: str, color: str):
    return f"[{color}]{text}[/{color}]"

class ValueColorizer(Formatter[AnsiColor]):
    def __call__(self, x: object, depth: int) -> AnsiColor: ...

class ColorizerRule(Protocol):
    def can_apply(self, x: tuple[object, object]) -> bool: ...
    def __call__(self, x: tuple[object, object]) -> AnsiColor: ...

class StatusColorizerRule(ColorizerRule):
    def __init__(self, default_color: AnsiColor):
        self.default_color = default_color

    def can_apply(self, x: tuple[object, object]) -> bool:
        k,v = x
        return k in ('status', )

    def __call__(self, x: tuple[object, object]) -> AnsiColor:
        k,v = x

        status_map = dict[str, AnsiColor](
                paused     = "bold yellow",
                restarting = "yellow",
                removing   = "red",
                running    = "green",
                dead       = "bold red",
                created    = "blue",
                exited     = "italic red",
            )
            
        return status_map.get(v, self.default_color)

class NoneColorizerRule(ColorizerRule):
    def can_apply(self, x: tuple[object, object]) -> bool:
        k,v = x
        return v is None
    
    def __call__(self, x: tuple[object, object]) -> AnsiColor:
        return "violet"

class PIDColorizerRule(ColorizerRule):
    def __init__(self, default_color: AnsiColor):
        self.default_color = default_color

    def can_apply(self, x: tuple[object, object]) -> bool:
        k,v = x
        return k in ('pid', )
    
    def __call__(self, x: tuple[object, object]) -> AnsiColor:
        return self.default_color


class ExitCodeColorizerRule(ColorizerRule):
    def can_apply(self, x: tuple[object, object]) -> bool:
        k,v = x
        return k in ('exit_code', 'returncode')
    
    def __call__(self, x: tuple[object, object]) -> AnsiColor:
        k,v = x
        return "bold red" if v != 0 else "bold green"

class FalsyColorizerRule(ColorizerRule):
    def can_apply(self, x: tuple[object, object]) -> bool:
        k,v = x
        return not bool(v)
    
    def __call__(self, x: tuple[object, object]) -> AnsiColor:
        return "bold red"

@final
class DEFAULT_VALUE_COLORIZER(ValueColorizer):
    def __init__(self, colors: Sequence[AnsiColor], rules: None | Sequence[ColorizerRule] = None):
        self.rules = rules or []
        self.colors = colors

    def __call__(self, x: tuple[object, object], depth: int) -> AnsiColor:
        c_i = self.colors[depth % len(self.colors)]

        DEFAULT_COLORIZER_RULES: Sequence[ColorizerRule] = [
            StatusColorizerRule(default_color=c_i),
            NoneColorizerRule(),
            PIDColorizerRule(default_color=c_i),
            ExitCodeColorizerRule(),
            FalsyColorizerRule(),
        ]

        DEFAULT_COLORIZER_RULES.extend(self.rules)

        for rule in DEFAULT_COLORIZER_RULES:
            if rule.can_apply(x): return rule(x)

        return c_i

DEFAULT_VALUE_COLORS: Sequence[AnsiColor] = ("bold green", "bold yellow", "bold magenta", "bold cyan")

class BulletFormatter(Formatter[str]):
    def __call__(self, value: object, depth: int) -> str: ...

def build_rich_dict(
    d: dict,
    title: str,
    depth: int,
    accent_colorizer: AccentColorizer,
    pipe_formatter: PipeFormatter,
    value_colorizer: ValueColorizer,
    bullet_formatter: BulletFormatter,
) -> list[str]:
    """Build a sequence of Rich-printable strings from a dict."""

    bullet = bullet_formatter(None, depth)

    def pipe_segment(d: int) -> str:
        return f" {pipe_formatter(None, d)} "

    accent = accent_colorizer(None, depth)

    colorized_title = rich_colorize(f"{bullet} {title}", f'bold {accent}')

    colorized_parent_pipes = "".join(
        rich_colorize(pipe_segment(i), accent_colorizer(None, i))
        for i in range(depth)
    )

    lines: list[str] = []
    if depth == 0:
        lines.append(colorized_title + "\n")
    else:
        lines.append(f"{colorized_parent_pipes}{colorized_title}\n")

    for k, v in d.items():
        my_pipe = pipe_segment(depth)
        pipe_str = rich_colorize(my_pipe, accent)
        if depth > 0:
            pipe_str = f"{colorized_parent_pipes}{pipe_str}"

        if isinstance(v, dict):
            lines.extend(build_rich_dict(v, k, depth + 1, accent_colorizer, pipe_formatter, value_colorizer, bullet_formatter))
        else:
            value_color = value_colorizer((k, v), depth)
            lines.append(f"{pipe_str}{k}: {rich_colorize(str(v), value_color)}\n")

    return lines


def print_rich_dict(
    data: dict,
    title: str,
    console: Console | None = None,
    accent_colorizer: AccentColorizer | None = None,
    pipe_formatter: PipeFormatter | None = None,
    value_colorizer: ValueColorizer | None = None,
    bullet_formatter: BulletFormatter | None = None,
) -> str:
    """Pretty-print a dict recursively. Returns a Rich-printable string."""
    console = console or Console()

    accent_colorizer = accent_colorizer or AccentColorizer.cycle(DEFAULT_ACCENT_COLORS)
    value_colorizer  = value_colorizer or DEFAULT_VALUE_COLORIZER(DEFAULT_VALUE_COLORS)
    bullet_formatter = bullet_formatter or BulletFormatter.constant(" ┏━")
    pipe_formatter   = pipe_formatter or PipeFormatter.constant("[dim]\u2503[/dim]")
    
    lines = build_rich_dict(
        data, 
        title, 
        0, 
        accent_colorizer, 
        pipe_formatter, 
        value_colorizer, 
        bullet_formatter
    )

    console.print("".join(lines).strip())
    return console