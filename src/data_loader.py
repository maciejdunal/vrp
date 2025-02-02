import csv


def load_clients(file_path: str, num_clients: int) -> list:
    """Wczytuje klientów z pliku CSV bez losowego doboru."""
    clients = []
    with open(file_path, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for i, client in enumerate(reader):
            if i >= num_clients:
                break
            clients.append({
                "Name": client["Name"],
                "Address": client["Address"],
                "Latitude": float(client["Latitude"]),
                "Longitude": float(client["Longitude"]),
                "Demand": int(client["Demand"])
            })
    return clients
