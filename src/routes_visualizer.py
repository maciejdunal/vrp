import folium


def visualize_vrp_route(locations: list, solution, manager, routing, num_vehicles: int):
    """Generuje mapę trasy VRP z podziałem na pojazdy."""
    m = folium.Map(location=[locations[0]['Latitude'], locations[0]['Longitude']], zoom_start=13)
    folium.Marker([locations[0]['Latitude'], locations[0]['Longitude']],
                  popup="Piekarnia", icon=folium.Icon(color="red", icon="info-sign")).add_to(m)

    colors = ["#FF0000", "#0000FF", "#008000", "#FFA500", "#800080"][:num_vehicles]

    for v in range(num_vehicles):
        route = []
        index = routing.Start(v)
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))
        route.append(manager.IndexToNode(index))

        pts = [(locations[i]['Latitude'], locations[i]['Longitude']) for i in route]
        folium.PolyLine(pts, color=colors[v], weight=2, opacity=0.5).add_to(m)

        for count, node in enumerate(route):
            if node == 0:
                continue
            folium.Marker(
                [locations[node]['Latitude'], locations[node]['Longitude']],
                icon=folium.DivIcon(html=f"""<div style="font-size:10px;color:white;background-color:{colors[v]};border:1px solid black;border-radius:50%;width:15px;height:15px;display:flex;align-items:center;justify-content:center;">{count}</div>""")
            ).add_to(m)

    m.save("vrp_route_map.html")
