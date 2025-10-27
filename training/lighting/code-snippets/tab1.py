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