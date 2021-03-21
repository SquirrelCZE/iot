import urwid
import urwid.curses_display
from lurwid import *
from conn import conn
import sys
import statistics
import math
import argparse

parser = argparse.ArgumentParser(description="Plots value from database")
parser.add_argument("sensor_type", type=str, help="Type of the sensor to be plotted")
parser.add_argument("spot_tag", type=str, help="Spot at which the values were measured")

args = parser.parse_args()


graph = urwid.BarGraph(
    ["normal", ("bar", "\u2502"), "normal"],
    ["normal", "barline", "normal"],
)

gscale = urwid.GraphVScale([], 0)

type_t = urwid.Text(("vals", args.sensor_type), align="right")
cur_t = urwid.Text("", align="right")
min_t = urwid.Text("", align="right")
avg_t = urwid.Text("", align="right")
max_t = urwid.Text("", align="right")
spot_t = urwid.Text(("vals", args.spot_tag), align="right")

stats = urwid.ListBox(
    [
        urwid.Text("type"),
        type_t,
        urwid.Text("cur"),
        cur_t,
        urwid.Text("min"),
        min_t,
        urwid.Text("avg"),
        avg_t,
        urwid.Text("max"),
        max_t,
        urwid.Text("spot"),
        spot_t,
    ]
)

from_date = urwid.Text("")
mid_date = urwid.Text("", align="center")
to_date = urwid.Text("", align="right")

cols = urwid.Columns(
    [
        (4, gscale),
        urwid.Frame(graph, footer=urwid.Columns([from_date, mid_date, to_date])),
        (10, stats),
    ],
    dividechars=1,
)


def fmtdate(d):
    return d.strftime("%H:%M")


def ceil(val, mult=1):
    return math.ceil(val / mult) * mult


def floor(val, mult=1):
    return math.floor(val / mult) * mult


def interp(step, fr, to, steps):
    return step * (to - fr) / steps + fr


def update(loop, _):
    cur = conn.cursor()
    limit = loop.screen.get_cols_rows()[0] - 16
    cur.execute(
        "SELECT value, measured_at FROM {} WHERE spot_tag = %(spot_tag)s ORDER BY measured_at DESC LIMIT %(lim)s".format(
            args.sensor_type
        ),
        {"lim": limit, "spot_tag": args.spot_tag},
    )

    data = list(cur.fetchall())
    data.reverse()

    vals = [x[0] for x in data]

    vmin = floor(min(vals), 5)
    vmax = ceil(max(vals), 5)

    top = int((vmax - vmin) * 10)

    gdata = [
        [
            int((x - vmin) * 10),
        ]
        for x in vals
    ]
    graph.set_data(bardata=gdata, top=top)

    vscale = [[0, vmin], [top - 2, vmax]]

    cols.contents[0] = (
        urwid.GraphVScale(
            [
                (
                    1 + interp(x, vscale[0][0], vscale[1][0], 5),
                    "{:>4}".format(int(interp(x, vscale[0][1], vscale[1][1], 5))),
                )
                for x in range(0, 6)
            ],
            top,
        ),
        cols.options("given", 4),
    )

    from_date.set_text(fmtdate(data[0][1]))
    mid_date.set_text(fmtdate((data[-1][1] - data[0][1]) / 2 + data[0][1]))
    to_date.set_text(fmtdate(data[-1][1]))

    def set_val(item, val):
        item.set_text(("vals", "{:.2f}".format(val)))

    set_val(cur_t, vals[-1])
    set_val(min_t, min(vals))
    set_val(avg_t, statistics.mean(vals))
    set_val(max_t, max(vals))

    loop.set_alarm_in(60, update)


loop = urwid.MainLoop(cols, palette)
loop.set_alarm_in(1, update)
loop.run()
