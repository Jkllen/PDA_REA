def safe_get(mapping, key, default=0.5):
    key = str(key).strip().lower()
    return mapping.get(key, default)


alcohol_map = {
    "none": 0.0,
    "1 drink (light)": 0.35,
    "2-3 drinks (moderate)": 0.70,
    "more than 3 drinks (high)": 1.00,
    "prefer not to say": 0.75,
}

driving_experience_map = {
    "less than 1 year": 0.65,
    "1-3 years": 0.55,
    "4-6 years": 0.30,
    "7-10 years": 0.25,
    "more than 10 years": 0.10,
}

time_of_day_map = {
    "early morning (12 am - 5 am)": 0.95,
    "morning (6 am - 11 am)": 0.25,
    "afternoon (12 pm - 5 pm)": 0.20,
    "evening (6 pm - 9 pm)": 0.60,
    "late night (10 pm - 11 pm)": 0.85,
}

trip_duration_map = {
    "less than 15 minutes": 0.15,
    "15-30 minutes": 0.30,
    "30-60 minutes": 0.50,
    "1-2 hours": 0.70,
    "more than 2 hours": 0.90,
}

weather_map = {
    "clear / sunny": 0.10,
    "cloudy / overcast": 0.25,
    "light rain": 0.55,
    "heavy rain": 0.80,
    "storm / typhoon": 1.00,
    "fog / low visibility": 0.85,
}

visible_road_issues_map = {
    "none": 0.10,
    "potholes / uneven road": 0.55,
    "flooding": 0.90,
    "road construction": 0.65,
    "accidents / obstructions": 0.80,
    "poor lighting": 0.60,
    "not sure": 0.50,
}

road_type_map = {
    "highway / expressway": 0.65,
    "main road / city road": 0.35,
    "residential area": 0.20,
    "rural / provincial road": 0.50,
    "mountain / curved road": 0.90,
}

traffic_level_map = {
    "light (free-flowing)": 0.15,
    "moderate": 0.45,
    "heavy (slow-moving)": 0.70,
    "severe congestion / standstill": 0.90,
}

road_condition_map = {
    "dry and clear": 0.10,
    "wet / slippery": 0.65,
    "muddy": 0.75,
    "flooded": 1.00,
    "damaged / uneven": 0.70,
}

intersection_map = {
    "no": 0.15,
    "yes - few": 0.45,
    "yes - many": 0.75,
    "not sure": 0.50,
}

vehicle_type_map = {
    "motorcycle": 0.95,
    "sedan / car": 0.20,
    "suv / van": 0.35,
    "pickup truck": 0.45,
}

mechanical_issues_map = {
    "none": 0.10,
    "minor issues (not affecting driving)": 0.40,
    "moderate issues (needs attention)": 0.70,
    "major issues (affects safety)": 1.00,
    "not sure": 0.65,
}

vehicle_age_map = {
    "less than 1 year": 0.10,
    "1-3 years": 0.20,
    "4-6 years": 0.40,
    "7-10 years": 0.65,
    "more than 10 years": 0.85,
}

brake_condition_map = {
    "very responsive": 0.10,
    "slight delay": 0.40,
    "noticeable delay": 0.75,
    "weak / unreliable": 1.00,
    "not sure": 0.70,
}

maintenance_map = {
    "within last month": 0.10,
    "1-3 months ago": 0.30,
    "4-6 months ago": 0.60,
    "more than 6 months ago": 0.90,
    "cannot remember": 0.65,
}