############ Imports ##############
import vizro.plotly.express as px
import vizro.models as vm
from vizro import Vizro
import pandas as pd
from vizro.managers import data_manager


####### Data Manager Settings #####
data_manager["electricity_data"] = pd.read_csv(
    "https://ourworldindata.org/grapher/share-of-the-population-with-access-to-electricity.csv"
)

########### Model code ############
model = vm.Dashboard(
    pages=[
        vm.Page(
            components=[
                vm.Graph(
                    id="electricity_map",
                    figure=px.choropleth(
                        data_frame="electricity_data",
                        locations="Code",
                        color="Access to electricity (% of population)",
                        hover_name="Entity",
                        hover_data={
                            "Access to electricity (% of population)": ":.1f%",
                            "Code": False,
                            "Year": False,
                        },
                        labels={
                            "Access to electricity (% of population)": "Access to Electricity (%)"
                        },
                        color_continuous_scale="Blues",
                        range_color=[0, 100],
                        height=600,
                    ),
                    title="Global Access to Electricity",
                )
            ],
            title="Electricity Access Map",
            layout=vm.Flex(),
            controls=[
                vm.Filter(
                    column="Year",
                    targets=["electricity_map"],
                    selector=vm.Slider(
                        min=1990,
                        max=2023,
                        step=1,
                        value=2023,
                        marks={year: str(year) for year in range(1990, 2024, 5)},
                        title="Select Year",
                    ),
                )
            ],
        ),
        vm.Page(
            components=[
                vm.Graph(
                    id="electricity_trends",
                    figure=px.line(
                        data_frame="electricity_data",
                        x="Year",
                        y="Access to electricity (% of population)",
                        color="Entity",
                    ),
                    title="Electricity Access Trends by Country",
                )
            ],
            title="Country Trends",
            layout=vm.Flex(),
            controls=[
                vm.Filter(
                    column="Entity",
                    targets=["electricity_trends"],
                    selector=vm.Dropdown(
                        multi=True,
                        value=[
                            "United States",
                            "China",
                            "Brazil", 
                            "India",
                            "Afghanistan",
                            "Rwanda",
                            "Haiti",
                        ],
                        title="Select Countries to Display",
                        extra={"optionHeight": 35},
                    ),
                )
            ],
        ),
        vm.Page(
            components=[
                vm.Graph(
                    id="electricity_histogram",
                    figure=px.bar(
                        data_frame="electricity_data",
                        x="Access to electricity (% of population)",
                        y="Entity",
                        orientation="h",
                        color="Entity",
                    ),
                    title="Electricity Access by Country",
                )
            ],
            title="Country Comparison",
            controls=[
                vm.Filter(
                    column="Year",
                    targets=["electricity_histogram"],
                    selector=vm.Slider(
                        min=1990,
                        max=2023,
                        step=1,
                        value=2023,
                        marks={year: str(year) for year in range(1990, 2024, 5)},
                        title="Select Year",
                    ),
                ),
                vm.Filter(
                    column="Entity",
                    targets=["electricity_histogram"],
                    selector=vm.Dropdown(
                        multi=True,
                        value=[
                            "United States",
                            "China",
                            "Brazil",
                            "India",
                            "Afghanistan",
                            "Rwanda",
                            "Haiti",
                        ],
                        title="Select Countries to Display",
                        extra={"optionHeight": 35},
                    ),
                )
            ],
        ),
    ],
    theme="vizro_light",
    title="Electricity Access Dashboard",
)

app = Vizro().build(model)
if __name__ == "__main__":
    app.run(debug=True, port=8050)