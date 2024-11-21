############ Imports ##############
import vizro.tables as vt
import vizro.models as vm
from vizro.models.types import capture
import plotly.graph_objects as go
import pandas as pd
from vizro.models.types import capture

import plotly.graph_objects as go
import pandas as pd
from vizro.models.types import capture


####### Function definitions ######
@capture("graph")
def pages_books_totals_chart(data_frame):
    # Convert 'Date Read' to datetime
    data_frame["Date Read"] = pd.to_datetime(data_frame["Date Read"])

    # Extract year from 'Date Read'
    data_frame["Year Read"] = data_frame["Date Read"].dt.year

    # Calculate cumulative pages read by year
    cumulative_pages = data_frame.groupby("Year Read")["Number of Pages"].sum().cumsum()

    # Calculate total books read by year
    total_books = data_frame.groupby("Year Read").size()

    # Create figure
    fig = go.Figure()

    # Add line chart for cumulative pages
    fig.add_trace(
        go.Scatter(
            x=cumulative_pages.index,
            y=cumulative_pages,
            mode="lines",
            name="Cumulative Pages",
            yaxis="y1",
        )
    )

    # Add bar chart for total books
    fig.add_trace(
        go.Bar(x=total_books.index, y=total_books, name="Total Books", yaxis="y2")
    )

    # Update layout
    fig.update_layout(
        title="Cumulative Pages and Total Books Read by Year",
        xaxis_title="Year",
        yaxis=dict(title="Cumulative Pages", side="left"),
        yaxis2=dict(title="Total Books", overlaying="y", side="right"),
        legend=dict(x=0.1, y=0.9),
    )

    return fig


@capture("graph")
def scatter_chart(data_frame):
    # Filter the data_frame for rows where 'My Rating' is greater than 0
    filtered_df = data_frame[data_frame["My Rating"] > 0]

    # Create a scatter plot
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(
        go.Scatter(
            x=filtered_df["Date Read"],
            y=filtered_df["My Rating"],
            mode="markers",
            text=filtered_df["Title"] + " by " + filtered_df["Author"],
            marker=dict(size=10, color="blue"),
        )
    )

    # Update layout
    fig.update_layout(
        title="Books Read with My Rating",
        xaxis_title="Date Read",
        yaxis_title="My Rating",
        hovermode="closest",
    )

    return fig


####### Data Manager Settings #####
#######!!! UNCOMMENT BELOW !!!#####
# from vizro.managers import data_manager
# data_manager["book_reading_data"] = ===> Fill in here <===


########### Model code ############
model = vm.Dashboard(
    pages=[
        vm.Page(
            components=[
                vm.AgGrid(
                    id="recent_reading_grid",
                    figure=vt.dash_ag_grid(data_frame="book_reading_data"),
                )
            ],
            title="Recent reading",
            layout=vm.Layout(grid=[[0]]),
            controls=[],
        ),
        vm.Page(
            components=[
                vm.Graph(
                    id="pages_books_totals_chart",
                    figure=pages_books_totals_chart(data_frame="book_reading_data"),
                )
            ],
            title="Pages and Book totals",
            layout=vm.Layout(grid=[[0]]),
            controls=[
                vm.Filter(
                    column="Year Published",
                    targets=["pages_books_totals_chart"],
                    selector=vm.RangeSlider(type="range_slider"),
                )
            ],
        ),
        vm.Page(
            components=[
                vm.Card(
                    id="rating_gap_chart",
                    text="Failed to build component: rating_gap_chart",
                ),
                vm.Graph(
                    id="scatter_chart",
                    figure=scatter_chart(data_frame="book_reading_data"),
                ),
            ],
            title="Types of book",
            layout=vm.Layout(grid=[[0, 1]]),
            controls=[],
        ),
    ],
    title="Book Reading Dashboard",
)