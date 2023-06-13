from dataclasses import dataclass

from _rg.classes.RenderSettings import RenderSettings
from _rg.classes.renderables.Concatenate import Concatenate
from _rg.classes.renderables.Renderable import Renderable


@dataclass
class Table(Renderable):
    data: list[list[Renderable | str]]
    horizontal_lines: bool = False
    vertical_lines: bool = False

    column_count = None

    def class_specific_render(self, render_settings: RenderSettings) -> list[str | Renderable]:
        self.column_count = max(len(row) for row in self.data)
        l = [rf"\SetTblrInner{{rowsep=0mm, leftsep=1mm, rightsep=4mm}}"]
        if self.vertical_lines:
            l.append(fr"\begin{{tblr}}{{|{'l|' * self.column_count}}}")
        else:
            l.append(fr"\begin{{tblr}}{{{'l' * self.column_count}}}")
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
