############ Imports ##############
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
def books_per_publication_year(data_frame):
    # Group the data by 'Original Publication Year' and count the number of books for each year
    year_counts = (
        data_frame.groupby("Original Publication Year")
        .size()
        .reset_index(name="Total Books")
    )

    # Sort the data by 'Original Publication Year'
    year_counts = year_counts.sort_values("Original Publication Year")

    # Create a bar chart
    fig = go.Figure(
        data=[
            go.Bar(
                x=year_counts["Original Publication Year"], y=year_counts["Total Books"]
            )
        ]
    )

    # Update layout
    fig.update_layout(
        title="Total Number of Books by Original Publication Year",
        xaxis_title="Original Publication Year",
        yaxis_title="Total Books",
    )

    return fig


@capture("graph")
def cumulative_pages_books(data_frame):
    # Convert 'Date Read' to datetime
    data_frame["Date Read"] = pd.to_datetime(data_frame["Date Read"])

    # Extract year from 'Date Read'
    data_frame["Year Read"] = data_frame["Date Read"].dt.year

    # Group by 'Year Read' and calculate cumulative pages and total books
    yearly_data = (
        data_frame.groupby("Year Read")
        .agg({"Number of Pages": "sum", "Book Id": "count"})
        .reset_index()
    )
    yearly_data["Cumulative Pages"] = yearly_data["Number of Pages"].cumsum()

    # Create figure
    fig = go.Figure()

    # Add cumulative pages line
    fig.add_trace(
        go.Scatter(
            x=yearly_data["Year Read"],
            y=yearly_data["Cumulative Pages"],
            mode="lines+markers",
            name="Cumulative Pages",
            yaxis="y1",
        )
    )

    # Add total books bar
    fig.add_trace(
        go.Bar(
            x=yearly_data["Year Read"],
            y=yearly_data["Book Id"],
            name="Total Books",
            yaxis="y2",
            opacity=0.6,
        )
    )

    # Update layout
    fig.update_layout(
        title="Cumulative Pages and Total Books Read Per Year",
        xaxis=dict(title="Year"),
        yaxis=dict(title="Cumulative Pages", side="left"),
        yaxis2=dict(title="Total Books", overlaying="y", side="right"),
        legend=dict(x=0.1, y=0.9),
    )

    return fig


@capture("graph")
def ratings_tornado(data_frame):
    # Sort the data by 'My Rating' and 'Average Rating'
    data_frame = data_frame.sort_values(
        by=["My Rating", "Average Rating"], ascending=[False, False]
    )

    # Create a tornado chart
    fig = go.Figure()

    # Add bars for 'My Rating'
    fig.add_trace(
        go.Bar(
            y=data_frame["Title"],
            x=-data_frame["My Rating"],
            name="My Rating",
            orientation="h",
            text=data_frame["Title"],
            textposition="inside",
            hoverinfo="x+y+text",
        )
    )

    # Add bars for 'Average Rating'
    fig.add_trace(
        go.Bar(
            y=data_frame["Title"],
            x=data_frame["Average Rating"],
            name="Average Rating",
            orientation="h",
            text=data_frame["Title"],
            textposition="inside",
            hoverinfo="x+y+text",
        )
    )

    # Update layout
    fig.update_layout(
        barmode="overlay",
        title="Tornado Chart of My Rating vs Average Rating",
        xaxis=dict(
            title="Rating",
            tickvals=[-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5],
            ticktext=["5", "4", "3", "2", "1", "0", "1", "2", "3", "4", "5"],
        ),
        yaxis=dict(title="Book Title"),
        legend=dict(x=0.5, y=1.1, orientation="h"),
    )

    return fig


@capture("graph")
def categories_pie_chart(data_frame):
    # Combine 'Fiction' and 'FICTION' into a single category
    data_frame["Categories"] = data_frame["Categories"].replace("FICTION", "Fiction")

    # Count the number of books in each category
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
                vm.Graph(
                    id="cumulative_pages_books",
                    figure=cumulative_pages_books(data_frame="book_reading_data"),
                ),
                vm.Graph(
                    id="books_per_publication_year",
                    figure=books_per_publication_year(data_frame="book_reading_data"),
                ),
                vm.Graph(
                    id="ratings_tornado",
                    figure=ratings_tornado(data_frame="book_reading_data"),
                ),
                vm.Graph(
                    id="categories_pie_chart",
                    figure=categories_pie_chart(data_frame="book_reading_data"),
                ),
            ],
            title="Recent reading",
            layout=vm.Layout(grid=[[0, 0], [1, 1], [2, 2], [3, 3]]),
            controls=[],
        )
    ],
    title="Recent reading",
)

