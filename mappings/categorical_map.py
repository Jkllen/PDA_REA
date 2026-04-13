def safe_get(mapping, key):
    key = str(key).strip().lower()
    return mapping.get(key, 0.5)


weather_map = {
    "clear": 0.1,
    "windy": 0.5,
    "fog": 0.5,
    "rain": 0.9,
}

light_map = {
    "daylight": 0.1,
    "dusk": 0.5,
    "darkness-light lit": 0.5,
    "darkness": 0.9,
}

road_map = {
    "dry": 0.1,
    "damp": 0.5,
    "wet": 0.5,
    "flood": 0.9,
}

vehicle_type_map = {
    "car": 0.2,
    "van": 0.2,
    "bus": 0.5,
    "truck": 0.5,
    "motorcycle": 0.9,
}

road_defect_map = {
    "no defects": 0.1,
    "worn surface": 0.5,
    "ruts/holes": 0.9,
}

brake_map = {
    "good": 0.1,
    "fair": 0.5,
    "poor": 0.9,
}

time_map = {
    "morning": 0.6,
    "afternoon": 0.3,
    "evening": 0.8,
}

road_type_map = {
    "city road": 0.3,
    "rural road": 0.5,
    "highway": 0.9, # Made it higher apt to the interview
    "mountain road": 0.9,
}

intersection_map = {
    "no intersection": 0.2,
    "at intersection": 0.8,
}


def alcohol_map(value):
    try:
        value = float(value)
    except Exception:
        value = 0.0

    if value == 0:
        return 0.0
    if value < 0.3:
        return 0.5
    return 1.0


def normalize_inputs(data):
    return {
        "weather": safe_get(weather_map, data["weather_conditions"]),
        "lighting": safe_get(light_map, data["road_light_condition"]),
        "road": safe_get(road_map, data["road_conditions"]),
        "vehicle_type": safe_get(vehicle_type_map, data["vehicle_type"]),
        "brake": safe_get(brake_map, data["brake_condition"]),
        "time": safe_get(time_map, data["time_of_day"]),
        "road_type": safe_get(road_type_map, data["road_type"]),
        "road_defect": safe_get(road_defect_map, data["road_defect"]),
        "intersection": safe_get(intersection_map, data["intersection_related"]),
        "alcohol": alcohol_map(data["driver_alcohol"]),
    }