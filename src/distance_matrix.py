import requests


def get_distance_matrix(locations: list) -> list:
    """Pobiera macierz odległości między punktami za pomocą OSRM."""
    base_url = "http://router.project-osrm.org/table/v1/driving/"
    coords = ";".join([f"{loc['Longitude']},{loc['Latitude']}" for loc in locations])
    url = f"{base_url}{coords}?annotations=distance"

    response = requests.get(url, timeout=10)
    data = response.json()
    matrix = data.get("distances", [])

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] is None:
                matrix[i][j] = 10**6  # Duża wartość oznaczająca brak połączenia

    return matrix
