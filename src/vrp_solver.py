from ortools.constraint_solver import pywrapcp, routing_enums_pb2


def solve_vrp(distance_matrix: list, strategy: str, num_vehicles: int, demands: list, vehicle_capacity: int):
    """Rozwiązuje problem VRP przy użyciu OR-Tools."""
    manager = pywrapcp.RoutingIndexManager(len(distance_matrix), num_vehicles, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        return distance_matrix[manager.IndexToNode(from_index)][manager.IndexToNode(to_index)]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    def demand_callback(from_index):
        return demands[manager.IndexToNode(from_index)]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index, 0, [vehicle_capacity] * num_vehicles, True, "Capacity"
    )

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = getattr(
        routing_enums_pb2.FirstSolutionStrategy, strategy
    )

    solution = routing.SolveWithParameters(search_parameters)
    return solution, manager, routing
