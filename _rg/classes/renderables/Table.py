from dataclasses import dataclass
from functools import reduce

from _rg.classes.RenderSettings import RenderSettings, RenderFormat
from _rg.classes.renderables.Concatenate import Concatenate
from _rg.classes.renderables.Renderable import Renderable


@dataclass
class Table(Renderable):
    data: list[list[Renderable | str]]
    horizontal_lines: bool = False
    vertical_lines: bool = False
    table_params: dict = None

    column_count = None

    def class_specific_render(self, render_settings: RenderSettings) -> list[str | Renderable]:
        if render_settings.render_format != RenderFormat.LATEX:
            return reduce(lambda a, b: a + b, self.data)  # Sum doesn't work on lists

        self.column_count = max(len(row) for row in self.data)

        if self.table_params is None:
            self.table_params = {}
        if self.vertical_lines:
            self.table_params.setdefault("colspec", "|" + "l|" * self.column_count)
        else:
            self.table_params.setdefault("colspec", "l" * self.column_count)
        table_params_str = ','.join(f"{table_param[0]}={{{table_param[1]}}}" for table_param in self.table_params.items())

        l = [rf"\SetTblrInner{{rowsep=0mm, leftsep=1mm, rightsep=4mm}}"]
        l.append(fr"\begin{{tblr}}{{{table_params_str}}}")
        if self.horizontal_lines:
            l.append(r"\hline")

        for row_data in self.data:
            l.append(Row(row_data, self))
            l.append(r"\\" + (r"\hline" if self.horizontal_lines else ""))

        l.append(r"\end{tblr}\phantom{}\\") # TODO Without phantom, the next line is flush against the table, but this is totally a hack
        return l


@dataclass
class Row(Renderable):
    data: list[Renderable | str]
    table: Table

    def class_specific_render(self, render_settings: RenderSettings) -> list[str | Renderable]:
        if len(self.data) == 1:
            return [Concatenate([fr"\SetCell[c={self.table.column_count}]{{l}}", self.data[0]])]
        else:
            sub_l = []
            first = True
            for cell in self.data:
                if not first:
                    sub_l.append("&")
                sub_l.append(cell)
                first = False
            return sub_l

    def __str__(self):
        return f"row containing {self.data}"
