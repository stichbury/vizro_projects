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

    # Calculate cumulative pages read per year
    cumulative_pages = data_frame.groupby("Year Read")["Number of Pages"].sum().cumsum()

    # Calculate total books read per year
    total_books = data_frame.groupby("Year Read").size()

    # Create figure with secondary y-axis
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

    # Update layout for dual y-axes
    fig.update_layout(
        title="Cumulative Pages and Total Books Read Per Year",
        xaxis_title="Year",
        yaxis_title="Cumulative Pages",
        yaxis2=dict(title="Total Books", overlaying="y", side="right"),
        legend=dict(x=0.1, y=0.9),
    )

    return fig


@capture("graph")
def tornado_chart(data_frame):
    # Sort the data by 'Title' for consistent ordering
    data_frame = data_frame.sort_values("Title")

    # Create the figure
    fig = go.Figure()

    # Add My Rating bars (left side)
    fig.add_trace(
        go.Bar(
            y=data_frame["Title"],
            x=-data_frame["My Rating"],  # Negative for left side
            name="My Rating",
            orientation="h",
            marker=dict(color="blue"),
        )
    )

    # Add Average Rating bars (right side)
    fig.add_trace(
        go.Bar(
            y=data_frame["Title"],
            x=data_frame["Average Rating"],
            name="Average Rating",
            orientation="h",
            marker=dict(color="orange"),
        )
    )

    # Update layout
    fig.update_layout(
        title="Tornado Chart of My Rating vs Average Rating",
        barmode="overlay",
        xaxis=dict(
            title="Rating",
            tickvals=[-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5],
            ticktext=["5", "4", "3", "2", "1", "0", "1", "2", "3", "4", "5"],
        ),
        yaxis=dict(title="Book Title"),
        legend=dict(x=0.5, y=1.1, orientation="h", xanchor="center"),
    )

    return fig


@capture("graph")
def categories_pie_chart(data_frame):
    # Combine 'Fiction' and 'FICTION' into a single category 'Fiction'
    data_frame["Categories"] = data_frame["Categories"].replace("FICTION", "Fiction")

    # Group by 'Categories' and count the number of books in each category
    category_counts = data_frame["Categories"].value_counts()

    # Create a pie chart
    fig = go.Figure(
        data=[go.Pie(labels=category_counts.index, values=category_counts.values)]
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
                vm.Filter(column="Book Id", targets=["pages_books_totals_chart"])
            ],
        ),
        vm.Page(
            components=[
                vm.Graph(
                    id="tornado_chart",
                    figure=tornado_chart(data_frame="book_reading_data"),
                ),
                vm.Graph(
                    id="categories_pie_chart",
                    figure=categories_pie_chart(data_frame="book_reading_data"),
                ),
            ],
            title="Types of book",
            layout=vm.Layout(grid=[[0, 1]]),
            controls=[],
        ),
    ],
    title="Book Reading Dashboard",
)

