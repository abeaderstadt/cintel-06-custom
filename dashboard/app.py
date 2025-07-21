# --------------------------------------------------------
# Imports
# --------------------------------------------------------

import pandas as pd
from pathlib import Path
import faicons as fa
import plotly.express as px

# Shiny Imports
from shiny import reactive, render
from shiny.express import input, ui
from shinywidgets import render_plotly
from faicons import icon_svg

# --------------------------------------------------------
# Load Data and Set Up App
# --------------------------------------------------------

app_dir = Path(__file__).parent
ui.include_css(app_dir / "styles.css")

# Load the cleaned tips.csv file
tips: pd.DataFrame = pd.read_csv(Path(__file__).parent / "tips.csv")

# Calculate bill range for slider
bill_rng = (min(tips.total_bill), max(tips.total_bill))

# --------------------------------------------------------
# UI Setup: Page Options and Sidebar
# --------------------------------------------------------

ui.page_opts(title="Tipping Behavior Insights🍴", fillable=True)

with ui.sidebar(open="desktop"):
    ui.input_slider(
        "total_bill",
        "Bill amount",
        min=bill_rng[0],
        max=bill_rng[1],
        value=bill_rng,
        pre="$",
    )
    ui.input_checkbox_group(
        "time",
        "Food service",
        ["Lunch", "Dinner"],
        selected=["Lunch", "Dinner"],
        inline=True,
    )
    ui.input_checkbox_group(
    "sex",
    "Sex",
    ["Male", "Female"],
    selected=["Male", "Female"],
    inline=True,
    )
    ui.input_action_button("reset", "Reset filter")

# --------------------------------------------------------
# UI: Value Boxes
# --------------------------------------------------------

ICONS = {
    "users": fa.icon_svg("users", "solid"),
    "hand-holding-heart": fa.icon_svg("hand-holding-heart", fill="white"),
    "currency-dollar": fa.icon_svg("dollar-sign"),
    "ellipsis": fa.icon_svg("ellipsis"),
}

with ui.layout_columns(fill=False):
    with ui.value_box(showcase=ICONS["users"], class_="bg-secondary text-white"):
        "Total tippers"

        @render.express
        def total_tippers():
            tips_data().shape[0]

    with ui.value_box(showcase=ICONS["hand-holding-heart"], class_="bg-secondary text-white"):
        "Average tip"

        @render.express
        def average_tip():
            d = tips_data()
            if d.shape[0] > 0:
                perc = d.tip / d.total_bill
                f"{perc.mean():.1%}"

    with ui.value_box(showcase=ICONS["currency-dollar"], class_="bg-secondary text-white"):
        "Average bill"

        @render.express
        def average_bill():
            d = tips_data()
            if d.shape[0] > 0:
                bill = d.total_bill.mean()
                f"${bill:.2f}"

# --------------------------------------------------------
# UI: Main Dashboard Cards
# --------------------------------------------------------

with ui.layout_columns(col_widths=[6, 6]):

    # Card 1: Data Table
    with ui.card(full_screen=True):
        ui.card_header("Tips data")

        @render.data_frame
        def table():
            return render.DataGrid(tips_data())

    # Card 2: Scatterplot
    with ui.card(full_screen=True):
        with ui.card_header(class_="d-flex justify-content-between align-items-center"):
            "Total bill vs tip"
            with ui.popover(title="Add a color variable", placement="top"):
                ICONS["ellipsis"]
                ui.input_radio_buttons(
                    "scatter_color",
                    None,
                    ["none", "sex", "smoker", "day", "time"],
                    inline=True,
                )

        @render_plotly
        def scatterplot():
            d = tips_data()
            color = input.scatter_color()
            fig = px.scatter(
                d,
                x="total_bill",
                y="tip",
                color=None if color == "none" else color,
            )
            if len(d) > 1:
                import numpy as np
                import plotly.graph_objs as go

                coef = np.polyfit(d.total_bill, d.tip, 1)
                poly1d_fn = np.poly1d(coef)
            
                x_line = np.linspace(d.total_bill.min(), d.total_bill.max(), 100)
                y_line = poly1d_fn(x_line)
            
                fig.add_trace(go.Scatter(
                    x=x_line,
                    y=y_line,
                    mode="lines",
                    line=dict(color="black", dash="dash"),
                    name="Trendline"
                ))
            return fig
        
    # Card 3: Tip by Sex Chart
    with ui.card(full_screen=True):
        ui.card_header("Average Tip by Sex")

        @render_plotly
        def tip_by_sex():
            dat = tips_data()
            if dat.empty:
                return px.bar(title="No data to display.")

            summary = dat.groupby("sex")["tip"].mean().reset_index()
            return px.bar(
                summary,
                x="sex",
                y="tip",
                color="sex",
                title="Average Tip by Sex",
                labels={"tip": "Average Tip ($)", "sex": "Sex"},
            )

    # Card 4: Total Tips by Day of Week
    with ui.card(full_screen=True):
        ui.card_header("Total Tips by Day of Week")

        @render_plotly
        def total_tips_by_day():
            dat = tips_data()
            if dat.empty:
                return px.bar(title="No data to display.")

            summary = dat.groupby("day")["tip"].sum().reset_index()
            return px.bar(
                summary,
                x="day",
                y="tip",
                color="day",
                title="Total Tips by Day of Week",
                labels={"tip": "Total Tips ($)", "day": "Day of Week"},
                category_orders={"day": ["Thur", "Fri", "Sat", "Sun"]},
            )

ui.include_css(app_dir / "styles.css")

# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------


@reactive.calc
def tips_data():
    bill = input.total_bill()
    idx1 = tips.total_bill.between(bill[0], bill[1])
    idx2 = tips.time.isin(input.time())
    idx3 = tips.sex.isin(input.sex())
    filtered = tips[idx1 & idx2 & idx3].copy()
    filtered['tip_pct'] = filtered['tip'] / filtered['total_bill'] 
    return filtered

@reactive.effect
@reactive.event(input.reset)
def _():
    ui.update_slider("total_bill", value=bill_rng)
    ui.update_checkbox_group("time", selected=["Lunch", "Dinner"])
