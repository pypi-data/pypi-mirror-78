""" A file selector component.
If tkinter is installed, this component is a button which opens the file dialog.
If tkinter is not installed, this component is a text input.
"""
import os
from typing import Optional, List

import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input

try:
    import tkinter
    from tkinter import filedialog

    tkinter_imported = True
except ModuleNotFoundError:
    tkinter_imported = False


class FileSelector:
    def __init__(
        self, id_: str, select_type: str = "file", filters: Optional[List[str]] = None
    ):
        """

        Parameters
        ----------
        id_: str
            id of the html element
        select_type: str, "file" or "folder" (default = "file")
            Whether the component should allow selection of a folder or a file.
        filters: List[str], optional (default = None)
            If set, a filter of allowed file type extensions.
        """
        self._id = id_
        self.select_type = select_type
        self.filters = filters
        self._listeners = []

    @property
    def html(self):
        if tkinter_imported:
            if self.select_type == "file":
                text = "#### Select File"
            else:
                text = "#### Select Folder"

            component = dbc.Button(
                [dcc.Markdown(text)], id=self._id, block=True, color="Link",
            )
        else:
            if self.select_type == "file":
                text = "Path to data file, e.g. ~/data/mydata.arff"
            else:
                text = "Path to folder, e.g. ~/data/"
            component = dbc.Input(id=self._id, placeholder=text, type="text",)
        return component

    def callback(self):
        if tkinter_imported:

            def get_file(_):
                tkinter.Tk().withdraw()
                if self.select_type == "file":
                    res = tkinter.filedialog.askopenfilename(filetypes=self.filters)
                else:
                    res = tkinter.filedialog.askdirectory()
                self._on_file_selected(res)

            field = "n_clicks"
        else:

            def get_file(text):
                if os.path.exists(text):
                    self._on_file_selected(text)

            field = "value"

        io_ = ([], [Input(self._id, field)])
        return io_, get_file

    def _on_file_selected(self, file: str):
        for listener in self._listeners:
            listener(file)
