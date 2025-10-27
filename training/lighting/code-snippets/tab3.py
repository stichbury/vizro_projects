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