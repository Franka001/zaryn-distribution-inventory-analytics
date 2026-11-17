"""Render the committed synthetic reporting snapshot; not a live report."""
import csv
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def render(folder="reports"):
    folder = Path(folder)
    with (folder / "dashboard_data.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    distribution = "due" in rows[0]
    if distribution:
        due = sum(int(r["due"]) for r in rows)
        timely = sum(int(r["timely"]) for r in rows)
        eligible = sum(int(r["eligible"]) for r in rows)
        complete = sum(int(r["complete"]) for r in rows)
        cards = [("Due units", str(due)), ("On-time quantity fill", f"{timely/due:.0%}" if due else "N/A"), ("Outstanding units", str(sum(int(r["outstanding"]) for r in rows))), ("On-time line completion", f"{complete/eligible:.0%}" if eligible else "N/A")]
        title = "Wholesale Fulfillment Overview | 31 Jan 2026"
        labels = [r["key"] for r in rows]
        a, b = [int(r["net"]) for r in rows], [int(r["shipped"]) for r in rows]
        right_labels, right_values = labels, [int(r["outstanding"]) for r in rows]
        headings = ("Net ordered vs shipped by cutoff / units", "Outstanding units by order line")
        note = "Fixed order snapshot. O3 cancelled; O4 not yet due. Future shipments excluded. No inventory balances shown."
    else:
        cards = [("Change events", str(len(rows))), ("Active orders", rows[-1]["active_orders"]), ("Ending value / cents", rows[-1]["balance_cents"]), ("Source sequences", rows[0]["sequence"] + " to " + rows[-1]["sequence"])]
        title = "Modernization Data-State Overview"
        labels = [r["sequence"] for r in rows]
        a, b = [int(r["balance_cents"]) for r in rows], None
        right_labels, right_values = labels, [int(r["active_orders"]) for r in rows]
        headings = ("Reconstructed source value by event / cents", "Active orders after each source event")
        note = "Synthetic source replay; one assumed currency. Not live pipeline monitoring or proof of an SSIS migration."
    fig = plt.figure(figsize=(16, 9), facecolor="#eef3f8")
    fig.text(.05, .93, "ZARYN DATA ENGINEERING", fontsize=23, weight="bold", color="#123047")
    fig.text(.05, .86, title, fontsize=20, color="#123047")
    for i, (label, value) in enumerate(cards):
        fig.text(.05+i*.235, .75, label, fontsize=11, color="#526575")
        fig.text(.05+i*.235, .68, value, fontsize=29, weight="bold", color="#247f88")
    left, right = fig.add_axes([.07,.25,.40,.30]), fig.add_axes([.57,.25,.36,.30])
    x = list(range(len(labels)))
    if b is None:
        left.plot(x, a, color="#247f88", marker="o", linewidth=3)
    else:
        left.bar([n-.18 for n in x], a, .36, color="#123047", label="Net ordered")
        left.bar([n+.18 for n in x], b, .36, color="#269d9b", label="Shipped")
        left.legend(frameon=False)
    left.set_xticks(x, labels)
    right.bar(right_labels, right_values, color="#269d9b")
    for ax, heading in zip((left, right), headings):
        ax.set_title(heading, loc="left", pad=18, fontsize=11)
        ax.set_ylim(bottom=0)
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", alpha=.15)
        ax.set_axisbelow(True)
    fig.text(.05,.14,note,fontsize=10,color="#526575")
    fig.text(.05,.07,"SYNTHETIC DATA | STATIC PYTHON REPORT | NOT A POWER BI SCREENSHOT",fontsize=11,color="#247f88")
    fig.savefig(folder / "dashboard.png", dpi=160, facecolor=fig.get_facecolor())
    plt.close(fig)


if __name__ == "__main__":
    render()
