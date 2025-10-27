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