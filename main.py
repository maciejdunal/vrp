import argparse
from src.data_loader import load_clients
from src.distance_matrix import get_distance_matrix
from src.vrp_solver import solve_vrp
from src.routes_visualizer import visualize_vrp_route

VEHICLE_CAPACITY = 300

def format_vrp_output(solution, manager, routing, locations, num_vehicles, distance_matrix):
    output = "\nOptymalne trasy:\n"
    total_distance = 0

    for v in range(num_vehicles):
        output += f"\nPojazd {v+1}: Moja Piekarnia"
        index = routing.Start(v)
        step = 1
        route_distance = 0

        while not routing.IsEnd(index):
            prev_index = index
            index = solution.Value(routing.NextVar(index))
            if routing.IsEnd(index):
                break

            location_name = locations[manager.IndexToNode(index)]["Name"]
            output += f" -> {step}. {location_name}"
            step += 1

            route_distance += distance_matrix[manager.IndexToNode(prev_index)][manager.IndexToNode(index)]

        output += f"\nDługość trasy: {route_distance:.2f} m\n"
        total_distance += route_distance

    output += f"\nŁączna długość pokonanych tras: {total_distance:.2f} m\n"
    return output

def main(num_clients=60, strategy="PATH_CHEAPEST_ARC"):
    file_path = "data/clients.csv"
    depot = {"Name": "Moja Piekarnia", "Address": "Kraków, Piekarska 1", "Latitude": 50.048483, "Longitude": 19.941844, "Demand": 0}
    clients = load_clients(file_path, num_clients)
    locations = [depot] + clients
    demands = [loc["Demand"] for loc in locations]
    num_vehicles = 3
    distance_matrix = get_distance_matrix(locations)

    solution, manager, routing = solve_vrp(distance_matrix, strategy, num_vehicles, demands, VEHICLE_CAPACITY)

    vrp_output = format_vrp_output(solution, manager, routing, locations, num_vehicles, distance_matrix)
    print(vrp_output)

    visualize_vrp_route(locations, solution, manager, routing, num_vehicles)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_clients", type=int, default=60)
    parser.add_argument("--strategy", type=str, default="PATH_CHEAPEST_ARC")
    args = parser.parse_args()
    main(num_clients=args.num_clients, strategy=args.strategy)
