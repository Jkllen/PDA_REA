def get_login_input():
    client = input("Client Number: ").strip()
    password = input("Password: ").strip()
    return client, password


def get_int(prompt, min_value, max_value):
    while True:
        try:
            value = int(input(prompt).strip())
            if min_value <= value <= max_value:
                return value
            print(f"Enter a value between {min_value} and {max_value}.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def get_float(prompt, min_value, max_value):
    while True:
        try:
            value = float(input(prompt).strip())
            if min_value <= value <= max_value:
                return value
            print(f"Enter a value between {min_value} and {max_value}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def get_choice(prompt, valid_choices):
    valid_lower = [choice.lower() for choice in valid_choices]

    while True:
        value = input(prompt).strip().lower()
        if value in valid_lower:
            return value
        print(f"Invalid input. Choose from: {', '.join(valid_choices)}")


def get_user_input():
    print("\n=== ENTER PRE-DRIVING INPUTS ===")

    age = get_int("Driver Age (18-70): ", 18, 70)
    experience = get_int("Driver Experience (0-50 years): ", 0, 50)
    alcohol = get_float("Alcohol level (0-1): ", 0.0, 1.0)
    traffic = get_int("Traffic (0=low, 1=medium, 2=high): ", 0, 2)
    vehicle_age = get_float("Vehicle Age (0-21 years): ", 0.0, 21.0)
    failure = get_float("Failure history (0-1): ", 0.0, 1.0)
    maintenance = get_float("Maintenance required (0-1): ", 0.0, 1.0)

    brake = get_choice("Brake condition (good/fair/poor): ", ["good", "fair", "poor"])
    weather = get_choice(
        "Weather (clear/sunny/windy/fog/foggy/rain/heavy rain/storm): ",
        ["clear", "sunny", "windy", "fog", "foggy", "rain", "heavy rain", "storm"],
    )
    lighting = get_choice(
        "Lighting (daylight/bright/darkness-light lit/light lit/darkness-lights unlit/unlit/no lighting): ",
        [
            "daylight",
            "bright",
            "darkness-light lit",
            "light lit",
            "darkness-lights unlit",
            "unlit",
            "no lighting",
        ],
    )
    road_condition = get_choice(
        "Road condition (dry/normal/wet/slippery/muddy/sand/flood): ",
        ["dry", "normal", "wet", "slippery", "muddy", "sand", "flood"],
    )
    time_of_day = get_choice(
        "Time of day (morning/afternoon/evening/night): ",
        ["morning", "afternoon", "evening", "night"],
    )
    road_type = get_choice(
        "Road type (city road/one way/roundabout/slip road/highway/rural road/mountain road): ",
        ["city road", "one way", "roundabout", "slip road", "highway", "rural road", "mountain road"],
    )

    return {
        "driver_age": age,
        "driver_experience": experience,
        "driver_alcohol": alcohol,
        "traffic_density": traffic,
        "vehicle_age": vehicle_age,
        "failure_history": failure,
        "maintenance_required": maintenance,
        "brake_condition": brake,
        "weather": weather,
        "lighting": lighting,
        "road_condition": road_condition,
        "time_of_day": time_of_day,
        "road_type": road_type,
    }