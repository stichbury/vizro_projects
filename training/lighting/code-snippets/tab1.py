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
                                        range_color=[0, 100],
                                        height=700,
                                    ),
                                )
                            ],
                            title="Global electricity access",
                            layout=vm.Flex(type="flex"),
                        ),
