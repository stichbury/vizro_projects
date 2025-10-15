############ Imports ##############
import vizro.plotly.express as px
import vizro.models as vm
from vizro import Vizro
import pandas as pd
from vizro.managers import data_manager


####### Data Manager Settings #####
data_manager["gapminder_data"] = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv"
)

########### Model code ############
model = vm.Dashboard(
    pages=[
        vm.Page(
            components=[
                vm.Graph(
                    type="graph",
                    figure=px.scatter(
                        data_frame="gapminder_data",
                        x="gdpPercap",
                        y="lifeExp",
                        color="continent",
                        size="pop",
                        hover_name="country",
                    ),
                    title="Life Expectancy vs GDP per Capita",
                )
            ],
            title="Scatter Plot",
            layout=vm.Flex(type="flex", direction="column"),
        ),
        vm.Page(
            components=[
                vm.Graph(
                    type="graph",
                    figure=px.line(
                        data_frame="gapminder_data",
                        x="year",
                        y="lifeExp",
                        color="continent",
                    ),
                    title="Life Expectancy Over Time",
                )
            ],
            title="Line Chart",
            layout=vm.Flex(type="flex", direction="column"),
        ),
        vm.Page(
            components=[
                vm.Graph(
                    type="graph",
                    figure=px.bar(
                        data_frame="gapminder_data", x="continent", y="lifeExp"
                    ),
                    title="Average Life Expectancy by Continent (2007)",
                )
            ],
            title="Bar Chart",
            layout=vm.Flex(type="flex", direction="column"),
        ),
    ],
    theme="vizro_dark",
    title="Gapminder Dashboard",
)

app = Vizro().build(model)
if __name__ == "__main__":
    app.run(debug=True, port=8050)