from rich import box
from rich.console import RenderableType
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.pretty import Pretty
from rich.table import Table
from rich.text import Text

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal
from textual.reactive import reactive, watch
from textual.widgets import (
    DataTable,
    Header,
    Footer,
    Static,
    Button,
    Checkbox,
    TextLog,
    Input,
)

from_markup = Text.from_markup

example_table = Table(
    show_edge=False,
    show_header=True,
    expand=True,
    row_styles=["none", "dim"],
    box=box.SIMPLE,
)
example_table.add_column(from_markup("[green]Date"), style="green", no_wrap=True)
example_table.add_column(from_markup("[blue]Title"), style="blue")
example_table.add_column(
    from_markup("[cyan]Production Budget"),
    style="cyan",
    justify="right",
    no_wrap=True,
)
example_table.add_column(
    from_markup("[magenta]Box Office"),
    style="magenta",
    justify="right",
    no_wrap=True,
)
example_table.add_row(
    "Dec 20, 2019",
    "Star Wars: The Rise of Skywalker",
    "$275,000,000",
    "$375,126,118",
)
example_table.add_row(
    "May 25, 2018",
    from_markup("[b]Solo[/]: A Star Wars Story"),
    "$275,000,000",
    "$393,151,347",
)
example_table.add_row(
    "Dec 15, 2017",
    "Star Wars Ep. VIII: The Last Jedi",
    "$262,000,000",
    from_markup("[bold]$1,332,539,889[/bold]"),
)
example_table.add_row(
    "May 19, 1999",
    from_markup("Star Wars Ep. [b]I[/b]: [i]The phantom Menace"),
    "$115,000,000",
    "$1,027,044,677",
)


WELCOME_MD = """

## Textual Demo

Textual is a framework for creating sophisticated applications with the terminal.

"""


RICH_MD = """

Textual is built on Rich, one of the most popular libraries for Python.

Use any Rich *renderable* to add content to a Textual App (this text is rendered with Markdown).

Here are some examples:


"""

CSS_MD = """

Textual uses Cascading Stylesheets (CSS) to create Rich interactive User Interfaces.

- **Easy to learn** - much simpler than browser CSS
- **Live editing** - see your changes without restarting the app!

Here's an example of some CSS used in this app:

"""

EXAMPLE_CSS = """\
Screen {
    layers: base overlay notes;
    overflow: hidden;  
}

Sidebar {    
    width: 40;
    background: $panel;   
    transition: offset 500ms in_out_cubic;    
    layer: overlay;
    
}

Sidebar.-hidden {
    offset-x: -100%;
}"""

DATA = {
    "foo": [
        3.1427,
        (
            "Paul Atreides",
            "Vladimir Harkonnen",
            "Thufir Hawat",
            "Gurney Halleck" "Duncan Idaho",
        ),
    ],
}

WIDGETS_MD = """

Textual widgets are powerful interactive components.

Build your own or use the builtin widgets.

- **Input** Text / Password input.
- **Button** Clickable button with a number of styles.
- **Checkbox** A checkbox to toggle between states.
- **DataTable** A spreadsheet-like widget for navigating data. Cells may contain text or Rich renderables.
- **TreeControl** An generic tree with expandable nodes.
- **DirectoryTree** A tree of file and folders.
- *... many more planned ...* 

"""


MESSAGE = """
We hope you enjoy using Textual.

Here are some links. You can click these!

[@click="app.open_link('https://textual.textualize.io')"]Textual Docs[/]

[@click="app.open_link('https://github.com/Textualize/textual')"]Textual GitHub Repository[/]

[@click="app.open_link('https://github.com/Textualize/rich')"]Rich GitHub Repository[/]


Built with ♥  by [@click="app.open_link(https://www.textualize.io)"]Textualize.io[/]

"""


class Body(Container):
    pass


class Title(Static):
    pass


class DarkSwitch(Horizontal):
    def compose(self) -> ComposeResult:
        yield Checkbox(value=self.app.dark)
        yield Static("Dark mode", classes="label")

    def on_mount(self) -> None:
        watch(self.app, "dark", self.on_dark_change)

    def on_dark_change(self, dark: bool) -> None:
        self.query_one(Checkbox).value = self.app.dark

    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        self.app.dark = event.value


class Welcome(Container):
    def compose(self) -> ComposeResult:
        yield Static(Markdown(WELCOME_MD))
        yield Button("Start", variant="success")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.app.add_note("[b magenta]Start!")
        self.app.query_one(".location-first").scroll_visible(speed=50, top=True)


class OptionGroup(Container):
    pass


class SectionTitle(Static):
    pass


class Message(Static):
    pass


class Sidebar(Container):
    def compose(self) -> ComposeResult:
        yield Title("Textual Demo")
        yield OptionGroup(Message(MESSAGE))
        yield DarkSwitch()


class AboveFold(Container):
    pass


class Section(Container):
    pass


class Column(Container):
    pass


class Text(Static):
    pass


class QuickAccess(Container):
    pass


class LocationLink(Static):
    def __init__(self, label: str, reveal: str) -> None:
        super().__init__(label)
        self.reveal = reveal

    def on_click(self) -> None:
        self.app.query_one(self.reveal).scroll_visible(top=True)
        self.app.add_note(f"Scrolling to [b]{self.reveal}[/b]")


class LoginForm(Container):
    def compose(self) -> ComposeResult:
        yield Static("Username", classes="label")
        yield Input(placeholder="Username")
        yield Static("Password", classes="label")
        yield Input(placeholder="Password", password=True)
        yield Static()
        yield Button("Login", variant="primary")


class DemoApp(App):
    CSS_PATH = "demo.css"
    TITLE = "Textual Demo"
    BINDINGS = [
        ("ctrl+s", "app.toggle_class('Sidebar', '-hidden')", "Sidebar"),
        ("ctrl+t", "app.toggle_dark", "Toggle Dark mode"),
        ("f1", "app.toggle_class('TextLog', '-hidden')", "Notes"),
        Binding("ctrl+c,ctrl+q", "app.quit", "Quit", show=True),
    ]

    show_sidebar = reactive(False)

    def add_note(self, renderable: RenderableType) -> None:
        self.query_one(TextLog).write(renderable)

    def compose(self) -> ComposeResult:
        yield Container(
            Sidebar(classes="-hidden"),
            Header(),
            TextLog(classes="-hidden", wrap=False, highlight=True, markup=True),
            Body(
                QuickAccess(
                    LocationLink("TOP", ".location-top"),
                    LocationLink("Rich", ".location-rich"),
                    LocationLink("CSS", ".location-css"),
                    LocationLink("Widgets", ".location-widgets"),
                ),
                AboveFold(Welcome(), classes="location-top"),
                Column(
                    Section(
                        SectionTitle("Rich"),
                        Text(Markdown(RICH_MD)),
                        Static(Pretty(DATA, indent_guides=True), classes="pretty pad"),
                        Static(example_table, classes="table pad"),
                    ),
                    classes="location-rich location-first",
                ),
                Column(
                    Section(
                        SectionTitle("CSS"),
                        Text(Markdown(CSS_MD)),
                        Static(
                            Syntax(
                                EXAMPLE_CSS, "css", theme="material", line_numbers=True
                            )
                        ),
                    ),
                    classes="location-css",
                ),
                Column(
                    Section(
                        SectionTitle("Widgets"),
                        Text(Markdown(WIDGETS_MD)),
                        LoginForm(),
                        DataTable(),
                    ),
                    classes="location-widgets",
                ),
            ),
        )
        yield Footer()

    def action_open_link(self, link: str) -> None:
        self.app.bell()
        import webbrowser

        webbrowser.open(link)

    def on_mount(self) -> None:
        self.add_note("Textual Demo app is running")
        table = self.query_one(DataTable)
        table.add_column("Foo", width=20)
        table.add_column("Bar", width=20)
        table.add_column("Baz", width=20)
        table.add_column("Foo", width=20)
        table.add_column("Bar", width=20)
        table.add_column("Baz", width=20)
        table.zebra_stripes = True
        for n in range(20):
            table.add_row(*[f"Cell ([b]{n}[/b], {col})" for col in range(6)])


app = DemoApp()
if __name__ == "__main__":
    app.run()
