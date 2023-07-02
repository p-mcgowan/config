# all credit goes to https://github.com/SublimeText/Origami

# palette
# { "caption": "Panel: new", "command": "panel" },
# { "caption": "Panel: delete", "command": "destroy_panel" },

# bindings
# { "keys": ["ctrl+shift+alt+up"], "command": "create_panel", "args": { "direction": "up" } },
# { "keys": ["ctrl+shift+alt+down"], "command": "create_panel", "args": { "direction": "down" } },
# { "keys": ["ctrl+shift+alt+left"], "command": "create_panel", "args": { "direction": "left" } },
# { "keys": ["ctrl+shift+alt+right"], "command": "create_panel", "args": { "direction": "right" } },
#
# { "keys": ["ctrl+shift+alt+delete"], "command": "destroy_panel" },
#
# { "keys": ["ctrl+alt+up"], "command": "goto_panel", "args": { "direction": "up" } },
# { "keys": ["ctrl+alt+down"], "command": "goto_panel", "args": { "direction": "down" } },
# { "keys": ["ctrl+alt+left"], "command": "goto_panel", "args": { "direction": "left" } },
# { "keys": ["ctrl+alt+right"], "command": "goto_panel", "args": { "direction": "right" } },
#
# { "keys": ["ctrl+k", "ctrl+alt+up"], "command": "move_current_to_panel", "args": { "direction": "up" } },
# { "keys": ["ctrl+k", "ctrl+alt+down"], "command": "move_current_to_panel", "args": { "direction": "down" } },
# { "keys": ["ctrl+k", "ctrl+alt+left"], "command": "move_current_to_panel", "args": { "direction": "left" } },
# { "keys": ["ctrl+k", "ctrl+alt+right"], "command": "move_current_to_panel", "args": { "direction": "right" } },


import sublime
import sublime_plugin
import copy
from functools import partial

XMIN, YMIN, XMAX, YMAX = range(4)

def increment_if_greater_or_equal(x, threshold):
    if x >= threshold:
        return x + 1
    return x


def decrement_if_greater(x, threshold):
    if x > threshold:
        return x - 1
    return x


def pull_up_cells_after(cells, threshold):
    return [
        [x0, decrement_if_greater(y0, threshold), x1, decrement_if_greater(y1, threshold)]
        for (x0, y0, x1, y1) in cells
    ]


def push_right_cells_after(cells, threshold):
    return [
        [increment_if_greater_or_equal(x0, threshold), y0, increment_if_greater_or_equal(x1, threshold), y1]
        for (x0, y0, x1, y1) in cells
    ]


def push_down_cells_after(cells, threshold):
    return [
        [x0, increment_if_greater_or_equal(y0, threshold), x1, increment_if_greater_or_equal(y1, threshold)]
        for (x0, y0, x1, y1) in cells
    ]


def pull_left_cells_after(cells, threshold):
    return [
        [decrement_if_greater(x0, threshold), y0, decrement_if_greater(x1, threshold), y1]
        for (x0, y0, x1, y1) in cells
    ]

def opposite_direction(direction):
    if direction == "up":
        return "down"
    if direction == "right":
        return "left"
    if direction == "down":
        return "up"
    if direction == "left":
        return "right"

def cells_adjacent_to_cell_in_direction(cells, cell, direction):
    if direction == "up":
        return [c for c in cells if cell[YMIN] == c[YMAX]]
    if direction == "right":
        return [c for c in cells if cell[XMAX] == c[XMIN]]
    if direction == "down":
        return [c for c in cells if cell[YMAX] == c[YMIN]]
    if direction == "left":
        return [c for c in cells if cell[XMIN] == c[XMAX]]
    raise Exception('Unsupported direction "{}"'.format(direction))

class PaneCommand(sublime_plugin.WindowCommand):
    def get_layout(self):
        layout = self.window.layout()
        rows = layout["rows"]
        cols = layout["cols"]
        cells = layout["cells"]
        return rows, cols, cells

    def get_cells(self):
        return self.get_layout()[2]

    def adjacent_cell(self, direction):
        cells = self.get_cells()
        current_cell = cells[self.window.active_group()]
        adjacent_cells = cells_adjacent_to_cell_in_direction(cells, current_cell, direction)
        rows, cols, _ = self.get_layout()

        if direction in ("left", "right"):
            MIN, MAX, fields = YMIN, YMAX, rows
        else:  # up or down
            MIN, MAX, fields = XMIN, XMAX, cols

        cell_overlap = []
        for cell in adjacent_cells:
            start = max(fields[cell[MIN]], fields[current_cell[MIN]])
            end = min(fields[cell[MAX]], fields[current_cell[MAX]])
            overlap = end - start  # / (fields[cell[MAX]] - fields[cell[MIN]])
            cell_overlap.append(overlap)

        if len(cell_overlap) != 0:
            cell_index = cell_overlap.index(max(cell_overlap))
            return adjacent_cells[cell_index]
        return None

    def travel_to_pane(self, direction):
        adjacent_cell = self.adjacent_cell(direction)
        if adjacent_cell:
            cells = self.get_cells()
            new_group_index = cells.index(adjacent_cell)
            self.window.focus_group(new_group_index)

    def create_pane(self, direction):
        rows, cols, cells = self.get_layout()
        current_group = self.window.active_group()

        old_cell = cells.pop(current_group)
        new_cell = []

        if direction in ("up", "down"):
            cells = push_down_cells_after(cells, old_cell[YMAX])
            rows.insert(old_cell[YMAX], (rows[old_cell[YMIN]] + rows[old_cell[YMAX]]) / 2)
            new_cell = [old_cell[XMIN], old_cell[YMAX], old_cell[XMAX], old_cell[YMAX] + 1]
            old_cell = [old_cell[XMIN], old_cell[YMIN], old_cell[XMAX], old_cell[YMAX]]

        elif direction in ("right", "left"):
            cells = push_right_cells_after(cells, old_cell[XMAX])
            cols.insert(old_cell[XMAX], (cols[old_cell[XMIN]] + cols[old_cell[XMAX]]) / 2)
            new_cell = [old_cell[XMAX], old_cell[YMIN], old_cell[XMAX] + 1, old_cell[YMAX]]
            old_cell = [old_cell[XMIN], old_cell[YMIN], old_cell[XMAX], old_cell[YMAX]]

        if new_cell:
            if direction in ("left", "up"):
                focused_cell = new_cell
                unfocused_cell = old_cell
            else:
                focused_cell = old_cell
                unfocused_cell = new_cell
            cells.insert(current_group, focused_cell)
            cells.append(unfocused_cell)
            layout = {"cols": cols, "rows": rows, "cells": cells}  # type: sublime.Layout
            self.window.set_layout(layout)

            next_group = self.window.active_group()
            self.window.run_command("focus_group", { "group": current_group })
            self.window.run_command("move_to_group", { "group": next_group })

    def move_current_to_group(self, direction):
        current_group = self.window.active_group()
        self.travel_to_pane(direction)
        next_group = self.window.active_group()
        self.window.run_command("focus_group", { "group": current_group })
        self.window.run_command("move_to_group", { "group": next_group })


    def destroy_current_pane(self):
        # Out of the four adjacent panes, one was split to create this pane.
        # Find out which one, move to it, then destroy this pane.
        cells = self.get_cells()

        current = cells[self.window.active_group()]

        target_dir = None
        for dir in ("up", "right", "down", "left"):
            c = self.adjacent_cell(dir)
            if not c:
                continue
            if dir in ("up", "down"):
                if c[XMIN] == current[XMIN] and c[XMAX] == current[XMAX]:
                    target_dir = dir
            elif dir in ("left", "right"):
                if c[YMIN] == current[YMIN] and c[YMAX] == current[YMAX]:
                    target_dir = dir
        if target_dir:
            self.travel_to_pane(target_dir)
            self.destroy_pane(opposite_direction(target_dir))

    def destroy_pane(self, direction, only_on_empty=False):
        if direction == "self":
            self.destroy_current_pane()
            return

        window = self.window
        rows, cols, cells = self.get_layout()
        current_group = window.active_group()

        cell_to_remove = None
        current_cell = cells[current_group]

        adjacent_cells = cells_adjacent_to_cell_in_direction(cells, current_cell, direction)
        if len(adjacent_cells) == 1:
            cell_to_remove = adjacent_cells[0]

        if cell_to_remove:
            active_view = window.active_view()
            group_to_remove = cells.index(cell_to_remove)
            has_content = len(window.sheets_in_group(group_to_remove)) > 0
            if only_on_empty and has_content:
                return

            dupe_views = self.duplicated_views(current_group, group_to_remove)
            for d in dupe_views:
                window.focus_view(d)
                window.run_command('close')
            if active_view:
                window.focus_view(active_view)

            cells.remove(cell_to_remove)
            if direction == "up":
                rows.pop(cell_to_remove[YMAX])
                adjacent_cells = cells_adjacent_to_cell_in_direction(cells, cell_to_remove, "down")
                for cell in adjacent_cells:
                    cells[cells.index(cell)][YMIN] = cell_to_remove[YMIN]
                cells = pull_up_cells_after(cells, cell_to_remove[YMAX])
            elif direction == "right":
                cols.pop(cell_to_remove[XMIN])
                adjacent_cells = cells_adjacent_to_cell_in_direction(cells, cell_to_remove, "left")
                for cell in adjacent_cells:
                    cells[cells.index(cell)][XMAX] = cell_to_remove[XMAX]
                cells = pull_left_cells_after(cells, cell_to_remove[XMIN])
            elif direction == "down":
                rows.pop(cell_to_remove[YMIN])
                adjacent_cells = cells_adjacent_to_cell_in_direction(cells, cell_to_remove, "up")
                for cell in adjacent_cells:
                    cells[cells.index(cell)][YMAX] = cell_to_remove[YMAX]
                cells = pull_up_cells_after(cells, cell_to_remove[YMIN])
            elif direction == "left":
                cols.pop(cell_to_remove[XMAX])
                adjacent_cells = cells_adjacent_to_cell_in_direction(cells, cell_to_remove, "right")
                for cell in adjacent_cells:
                    cells[cells.index(cell)][XMIN] = cell_to_remove[XMIN]
                cells = pull_left_cells_after(cells, cell_to_remove[XMAX])

            layout = {"cols": cols, "rows": rows, "cells": cells}  # type: sublime.Layout
            window.set_layout(layout)

    def duplicated_views(self, original_group, duplicating_group):
        original_views = self.window.views_in_group(original_group)
        original_buffers = {v.buffer_id() for v in original_views}
        potential_dupe_views = self.window.views_in_group(duplicating_group)
        return [pd for pd in potential_dupe_views if pd.buffer_id() in original_buffers]

class MoveCurrentToPanelCommand(PaneCommand):
    def run(self, direction):
        self.move_current_to_group(normalize_direction[direction])

class GotoPanelCommand(PaneCommand):
    def run(self, direction):
        self.travel_to_pane(normalize_direction[direction])

class CreatePanelCommand(PaneCommand):
    def run(self, direction):
        self.create_pane(normalize_direction[direction])

class DestroyPanelCommand(PaneCommand):
    def run(self):
        self.destroy_current_pane()

normalize_direction = {
    "up": "up",
    "u": "up",
    "right": "right",
    "r": "right",
    "down": "down",
    "d": "down",
    "left": "left",
    "l": "left"
}

class PanelCommand(sublime_plugin.TextCommand):
    """Prompt for command."""

    def run(self, edit):
        self.view.window().show_input_panel('New panel (Up, Right, Down, Left):', '', self.on_done, None, None)

    def on_done(self, text):
        self.view.window().run_command('create_panel', { 'direction': normalize_direction[text] })

