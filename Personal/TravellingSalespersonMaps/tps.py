import argparse
import math
import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple, Union

import requests

try:
    import folium
except ImportError:  # pragma: no cover - optional dependency
    folium = None

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional dependency
    load_dotenv = None


ORS_GEOCODE_URL = "https://api.openrouteservice.org/geocode/search"
ORS_MATRIX_URL = "https://api.openrouteservice.org/v2/matrix/driving-car"
ORS_DIRECTIONS_URL = "https://api.openrouteservice.org/v2/directions/driving-car"


@dataclass(frozen=True)
class City:
    name: str
    lon: float
    lat: float


def load_cities(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as handle:
        names = [line.strip() for line in handle if line.strip()]
    seen = set()
    ordered = []
    for name in names:
        if name not in seen:
            ordered.append(name)
            seen.add(name)
    return ordered


def normalize_cities(cities: List[str], start_city: str) -> List[str]:
    if start_city in cities:
        return [start_city] + [city for city in cities if city != start_city]
    return [start_city] + cities


def get_api_key(cli_key: Optional[str]) -> str:
    if cli_key:
        return cli_key
    env_key = os.getenv("ORS_API_KEY")
    if env_key:
        return env_key
    raise SystemExit(
        "Missing OpenRouteService API key. Provide --api-key or set ORS_API_KEY."
    )


def geocode_city(session: requests.Session, api_key: str, name: str) -> City:
    params = {
        "api_key": api_key,
        "text": f"{name}, Bulgaria",
        "size": 1,
        "boundary.country": "BG",
    }
    response = session.get(ORS_GEOCODE_URL, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    features = data.get("features") or []
    if not features:
        raise RuntimeError(f"Geocoding failed for {name!r}.")
    lon, lat = features[0]["geometry"]["coordinates"]
    return City(name=name, lon=lon, lat=lat)


def build_city_list(names: List[str], api_key: str) -> List[City]:
    session = requests.Session()
    cache: Dict[str, City] = {}
    cities: List[City] = []
    for name in names:
        if name in cache:
            cities.append(cache[name])
            continue
        city = geocode_city(session, api_key, name)
        cache[name] = city
        cities.append(city)
    return cities


def fetch_duration_matrix(cities: List[City], api_key: str) -> List[List[float]]:
    locations = [[city.lon, city.lat] for city in cities]
    headers = {"Authorization": api_key, "Content-Type": "application/json"}
    payload = {"locations": locations, "metrics": ["duration"]}
    response = requests.post(
        ORS_MATRIX_URL, json=payload, headers=headers, timeout=60)
    response.raise_for_status()
    data = response.json()
    durations = data.get("durations")
    if not durations:
        raise RuntimeError("Matrix API did not return durations.")
    return durations


def fetch_route_geometry(
    session: requests.Session,
    api_key: str,
    origin: City,
    destination: City,
) -> List[Tuple[float, float]]:
    headers = {"Authorization": api_key}
    params = {
        "start": f"{origin.lon},{origin.lat}",
        "end": f"{destination.lon},{destination.lat}",
        "format": "geojson",
    }
    response = session.get(
        ORS_DIRECTIONS_URL, params=params, headers=headers, timeout=60
    )
    response.raise_for_status()
    data = response.json()
    features = data.get("features") or []
    if not features:
        raise RuntimeError(
            f"Directions failed for {origin.name} -> {destination.name}."
        )
    coords = features[0]["geometry"]["coordinates"]
    return [(lat, lon) for lon, lat in coords]


def solve_tsp(duration: List[List[float]]) -> Tuple[List[int], float]:
    n = len(duration)
    if n <= 1:
        return [0], 0.0

    size = 1 << (n - 1)
    dp = [[math.inf] * n for _ in range(size)]
    parent = [[-1] * n for _ in range(size)]

    for i in range(1, n):
        mask = 1 << (i - 1)
        dp[mask][i] = duration[0][i]
        parent[mask][i] = 0

    for mask in range(size):
        for i in range(1, n):
            if not (mask & (1 << (i - 1))):
                continue
            prev_mask = mask ^ (1 << (i - 1))
            if prev_mask == 0:
                continue
            best = dp[mask][i]
            best_parent = parent[mask][i]
            for j in range(1, n):
                if not (prev_mask & (1 << (j - 1))):
                    continue
                cand = dp[prev_mask][j] + duration[j][i]
                if cand < best:
                    best = cand
                    best_parent = j
            dp[mask][i] = best
            parent[mask][i] = best_parent

    full_mask = size - 1
    best_total = math.inf
    best_end = -1
    for i in range(1, n):
        cand = dp[full_mask][i] + duration[i][0]
        if cand < best_total:
            best_total = cand
            best_end = i

    if best_end == -1:
        return [0], 0.0

    order: List[int] = []
    mask = full_mask
    current = best_end
    while mask:
        order.append(current)
        prev = parent[mask][current]
        mask ^= 1 << (current - 1)
        current = prev

    order.reverse()
    route = [0] + order + [0]
    return route, best_total


def format_minutes(minutes: int) -> str:
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02d}:{mins:02d}"


def build_schedule(
    route: List[int],
    duration: List[List[float]],
    city_names: List[str],
    work_minutes: int,
    day_start: int,
    day_end: int,
) -> List[Dict[str, Union[str, int]]]:
    schedule: List[Dict[str, Union[str, int]]] = []
    day = 1
    current_time = day_start
    worked: Set[int] = set()

    start_city = route[0]
    if start_city not in worked and work_minutes > 0:
        if current_time + work_minutes > day_end:
            day += 1
            current_time = day_start
        schedule.append(
            {
                "day": day,
                "start": current_time,
                "end": current_time + work_minutes,
                "type": "work",
                "city": city_names[start_city],
            }
        )
        current_time += work_minutes
        worked.add(start_city)

    for step in range(len(route) - 1):
        origin = route[step]
        dest = route[step + 1]
        drive_minutes = int(math.ceil(duration[origin][dest] / 60.0))

        while drive_minutes > 0:
            if current_time >= day_end:
                day += 1
                current_time = day_start
                continue
            remaining = day_end - current_time
            chunk = min(remaining, drive_minutes)
            schedule.append(
                {
                    "day": day,
                    "start": current_time,
                    "end": current_time + chunk,
                    "type": "drive",
                    "from": city_names[origin],
                    "to": city_names[dest],
                }
            )
            current_time += chunk
            drive_minutes -= chunk

        if dest not in worked and work_minutes > 0:
            if current_time + work_minutes > day_end:
                day += 1
                current_time = day_start
            schedule.append(
                {
                    "day": day,
                    "start": current_time,
                    "end": current_time + work_minutes,
                    "type": "work",
                    "city": city_names[dest],
                }
            )
            current_time += work_minutes
            worked.add(dest)

    return schedule


def summarize_schedule(schedule: List[Dict[str, Union[str, int]]]) -> Tuple[int, int]:
    if not schedule:
        return 1, 0
    last_day = max(item["day"] for item in schedule)
    total_minutes = 0
    for item in schedule:
        total_minutes += int(item["end"]) - int(item["start"])
    return last_day, total_minutes


def print_schedule(schedule: List[Dict[str, Union[str, int]]]) -> None:
    if not schedule:
        print("No travel needed.")
        return
    current_day = None
    for item in schedule:
        if item["day"] != current_day:
            current_day = item["day"]
            print(f"\nDay {current_day}")
        start = format_minutes(int(item["start"]))
        end = format_minutes(int(item["end"]))
        if item["type"] == "drive":
            print(f"{start}-{end} drive {item['from']} -> {item['to']}")
        else:
            print(f"{start}-{end} work {item['city']}")


def build_route_map(
    route: List[int],
    cities: List[City],
    api_key: str,
    output_path: str,
) -> None:
    if folium is None:
        raise SystemExit(
            "Map visualization requires 'folium'. Install it with: pip install folium"
        )

    route_points = [(cities[idx].lat, cities[idx].lon) for idx in route]
    if not route_points:
        raise RuntimeError("No route points to visualize.")

    avg_lat = sum(point[0] for point in route_points) / len(route_points)
    avg_lon = sum(point[1] for point in route_points) / len(route_points)

    route_map = folium.Map(location=[avg_lat, avg_lon], zoom_start=7)

    def compute_marker_location(
        base_lat: float,
        base_lon: float,
        existing: List[Tuple[float, float]],
        threshold: float = 0.01,
        step_degrees: float = 60.0,
        step_radius: float = 0.006,
    ) -> Tuple[float, float]:
        close_count = sum(
            1
            for lat, lon in existing
            if abs(lat - base_lat) <= threshold and abs(lon - base_lon) <= threshold
        )
        if close_count == 0:
            return base_lat, base_lon
        ring = close_count // 6 + 1
        angle = math.radians(close_count * step_degrees)
        radius = step_radius * ring
        return base_lat + radius * math.sin(angle), base_lon + radius * math.cos(angle)

    marker_locations: List[Tuple[float, float]] = []
    for step, idx in enumerate(route):
        city = cities[idx]
        popup = f"{step + 1}. {city.name}"
        marker_lat, marker_lon = compute_marker_location(
            city.lat, city.lon, marker_locations
        )
        marker_locations.append((marker_lat, marker_lon))
        folium.Marker(
            location=[marker_lat, marker_lon],
            popup=popup,
            tooltip=popup,
            icon=folium.DivIcon(
                html=(
                    f"<div style='background:#1f77b4;color:white;"
                    f"border-radius:50%;width:28px;height:28px;"
                    f"line-height:28px;text-align:center;font-weight:600;'>"
                    f"{step + 1}"
                    "</div>"
                )
            ),
        ).add_to(route_map)

    session = requests.Session()
    for step in range(len(route) - 1):
        origin = cities[route[step]]
        dest = cities[route[step + 1]]
        leg_points = fetch_route_geometry(session, api_key, origin, dest)
        folium.PolyLine(
            leg_points,
            color="#1f77b4",
            weight=4,
            opacity=0.9,
        ).add_to(route_map)

    route_map.save(output_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute fastest route with work stops using OpenRouteService."
    )
    parser.add_argument(
        "--cities-file",
        default="cities.txt",
        help="Path to file with city names, one per line.",
    )
    parser.add_argument(
        "--start-city",
        default="Sofia",
        help="Starting and ending city.",
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="OpenRouteService API key (or set ORS_API_KEY).",
    )
    parser.add_argument(
        "--work-minutes",
        type=int,
        default=60,
        help="Work time in minutes per city.",
    )
    parser.add_argument(
        "--day-start",
        type=str,
        default="07:00",
        help="Daily driving start time (HH:MM).",
    )
    parser.add_argument(
        "--day-end",
        type=str,
        default="23:00",
        help="Daily driving end time (HH:MM).",
    )
    parser.add_argument(
        "--map-file",
        type=str,
        default="route_map.html",
        help="Output HTML map file with the full route.",
    )
    return parser.parse_args()


def parse_time_hhmm(value: str) -> int:
    parts = value.split(":")
    if len(parts) != 2:
        raise ValueError(f"Invalid time {value!r}; expected HH:MM.")
    hours = int(parts[0])
    minutes = int(parts[1])
    return hours * 60 + minutes


def main() -> None:
    if load_dotenv:
        load_dotenv()

    args = parse_args()
    api_key = get_api_key(args.api_key)

    cities = load_cities(args.cities_file)
    cities = normalize_cities(cities, args.start_city)
    city_objs = build_city_list(cities, api_key)

    duration = fetch_duration_matrix(city_objs, api_key)
    route, drive_seconds = solve_tsp(duration)

    route_names = [cities[idx] for idx in route]
    print("Route:")
    print(" -> ".join(route_names))

    drive_hours = drive_seconds / 3600.0
    print(f"Total driving time (no work): {drive_hours:.2f} hours")

    day_start = parse_time_hhmm(args.day_start)
    day_end = parse_time_hhmm(args.day_end)
    schedule = build_schedule(
        route=route,
        duration=duration,
        city_names=cities,
        work_minutes=args.work_minutes,
        day_start=day_start,
        day_end=day_end,
    )
    total_days, total_minutes = summarize_schedule(schedule)
    print(
        f"Total scheduled time (drive + work): {total_minutes / 60.0:.2f} hours")
    print(f"Days needed (07:00-23:00): {total_days}")
    print_schedule(schedule)

    try:
        build_route_map(
            route=route,
            cities=city_objs,
            api_key=api_key,
            output_path=args.map_file,
        )
        print(f"Map saved to {args.map_file}")
    except SystemExit as exc:
        print(str(exc))


if __name__ == "__main__":
    main()
