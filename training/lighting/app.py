############ Imports ##############
import vizro.plotly.express as px
import vizro.models as vm
from vizro import Vizro
import pandas as pd
from vizro.managers import data_manager


####### Data Manager Settings #####
# Load electricity access data
electricity_data = pd.read_csv(
    "https://ourworldindata.org/grapher/share-of-the-population-with-access-to-electricity.csv"
)
# Sort by year to ensure proper animation direction (left to right = 1990 to 2023)
electricity_data = electricity_data.sort_values('Year')

# Get all countries that have some data and expand them to cover full year range
# This ensures any country selected in the filter will show properly in animations
all_countries = electricity_data['Entity'].unique()
all_years = list(range(1990, 2024))

# Create expanded data for ALL countries to support dynamic filtering
expanded_data = []
for country in all_countries:
    country_data = electricity_data[electricity_data['Entity'] == country].copy()
    if not country_data.empty:
        # Get the country code
        country_code = country_data['Code'].iloc[0] if 'Code' in country_data.columns else ''
        
        # Create base structure for all years
        for year in all_years:
            existing = country_data[country_data['Year'] == year]
            if not existing.empty:
                expanded_data.append(existing.iloc[0].to_dict())
            else:
                # Find the most recent data before this year, or earliest after
                before_data = country_data[country_data['Year'] < year]
                after_data = country_data[country_data['Year'] > year]
                
                if not before_data.empty:
                    # Use most recent data before this year (forward fill)
                    base_data = before_data.iloc[-1].to_dict()
                elif not after_data.empty:
                    # Use earliest data after this year (backward fill)
                    base_data = after_data.iloc[0].to_dict()
                else:
                    continue
                    
                # Create new entry with interpolated year
                base_data['Year'] = year
                expanded_data.append(base_data)

# Convert to DataFrame
final_data = pd.DataFrame(expanded_data).sort_values(['Entity', 'Year'])
data_manager["electricity_data"] = final_data

########### Model code ############
model = vm.Dashboard(
    pages=[
        vm.Page(
            components=[
                vm.Tabs(
                    type="tabs",
                    tabs=[
                        vm.Container(
                            type="container",
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
                                        animation_frame="Year",
                                        animation_group="Entity",
                                        labels={
                                            "Access to electricity (% of population)": "Access to Electricity (%)"
                                        },
                                        range_color=[0, 100],
                                        height=700,
                                    ),
                                )
                            ],
                            title="Global electricity access",
                            layout=vm.Flex(type="flex"),
                        ),
                        vm.Container(
                            type="container",
                            components=[
                                vm.Graph(
                                    id="electricity_trends",
                                    figure=px.line(
                                        data_frame="electricity_data",
                                        x="Year",
                                        y="Access to electricity (% of population)",
                                        color="Entity",
                                        labels={
                                            "Access to electricity (% of population)": "Access to Electricity (%)"
                                        },
                                        height=600,
                                    ),
                                    title="Electricity access trends by country",
                                )
                            ],
                            title="Country trends",
                            layout=vm.Flex(type="flex"),
                        ),
                        vm.Container(
                            type="container",
                            components=[
                                vm.Graph(
                                    id="electricity_histogram",
                                    figure=px.bar(
                                        data_frame="electricity_data",
                                        x="Access to electricity (% of population)",
                                        y="Entity",
                                        orientation="h",
                                        animation_frame="Year",
                                        animation_group="Entity",
                                        labels={
                                            "Access to electricity (% of population)": "Access to Electricity (%)"
                                        },
                                        range_x=[0, 100],
                                        height=700,
                                    ).update_layout(showlegend=False),
                                    title="Electricity access by country",
                                )
                            ],
                            title="Country comparison",
                            layout=vm.Flex(type="flex"),
                        ),
                    ],
                    title="",
                )
            ],
            title="Electricity access dashboard",
            layout=vm.Flex(type="flex"),
            controls=[
                vm.Parameter(
                    targets=["electricity_map.projection"],
                    selector=vm.RadioItems(
                        options=["natural earth", "orthographic"],
                        value="natural earth",
                        title="Map projection",
                    ),
                ),
                vm.Filter(
                    column="Entity",
                    targets=["electricity_trends", "electricity_histogram"],
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
                        title="Select countries to display",
                        extra={"optionHeight": 35},
                    ),
                ),
            ],
        )
    ],
    theme="vizro_light",
)

app = Vizro().build(model)
if __name__ == "__main__":
    app.run(debug=True, port=8050)
