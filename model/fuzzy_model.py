import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from skfuzzy import interp_membership
from mappings.categorical_map import (
    brake_map,
    weather_map,
    light_map,
    road_map,
    time_map,
    road_type_map,
    vehicle_type_map,
    road_defect_map,
    intersection_map,
    safe_get,
)

# Antecedent
driver_age = ctrl.Antecedent(np.arange(18, 71, 1), "driver_age")
driver_experience = ctrl.Antecedent(np.arange(0, 51, 1), "driver_experience")
driver_alcohol = ctrl.Antecedent(np.arange(0, 1.01, 0.01), "driver_alcohol")
traffic_density = ctrl.Antecedent(np.arange(0, 3, 1), "traffic_density")


vehicle_age = ctrl.Antecedent(np.arange(0, 51, 1), "vehicle_age")
speed_limit = ctrl.Antecedent(np.arange(30, 214, 1), "speed_limit")
vehicle_type_risk = ctrl.Antecedent(np.arange(0, 1.01, 0.01), "vehicle_type_risk")
road_defect_risk = ctrl.Antecedent(np.arange(0, 1.01, 0.01), "road_defect_risk")
intersection_risk = ctrl.Antecedent(np.arange(0, 1.01, 0.01), "intersection_risk")

failure_history = ctrl.Antecedent(np.arange(0, 1.01, 0.01), "failure_history")
brake_condition = ctrl.Antecedent(np.arange(0, 1.01, 0.01), "brake_condition")

weather_risk = ctrl.Antecedent(np.arange(0, 1.01, 0.01), "weather_risk")
lighting_risk = ctrl.Antecedent(np.arange(0, 1.01, 0.01), "lighting_risk")
road_risk = ctrl.Antecedent(np.arange(0, 1.01, 0.01), "road_risk")
time_risk = ctrl.Antecedent(np.arange(0, 1.01, 0.01), "time_risk")
road_type_risk = ctrl.Antecedent(np.arange(0, 1.01, 0.01), "road_type_risk")

risk = ctrl.Consequent(np.arange(0, 1.01, 0.01), "risk")

# Membership Functions 
def add_low_medium_high(variable):
    variable["low"] = fuzz.trapmf(variable.universe, [0.0, 0.0, 0.2, 0.4])
    variable["medium"] = fuzz.trimf(variable.universe, [0.3, 0.5, 0.7])
    variable["high"] = fuzz.trapmf(variable.universe, [0.6, 0.8, 1.0, 1.0])


driver_age["young"] = fuzz.trapmf(driver_age.universe, [18, 18, 25, 35])
driver_age["middle"] = fuzz.trapmf(driver_age.universe, [28, 35, 55, 62])
driver_age["senior"] = fuzz.trapmf(driver_age.universe, [55, 62, 70, 70])

driver_experience["low"] = fuzz.trapmf(driver_experience.universe, [0, 0, 3, 7])
driver_experience["medium"] = fuzz.trapmf(driver_experience.universe, [5, 10, 20, 30])
driver_experience["high"] = fuzz.trapmf(driver_experience.universe, [25, 35, 50, 50])

driver_alcohol["none"] = fuzz.trapmf(driver_alcohol.universe, [0.0, 0.0, 0.05, 0.1])
driver_alcohol["low"] = fuzz.trimf(driver_alcohol.universe, [0.05, 0.25, 0.5])
driver_alcohol["high"] = fuzz.trapmf(driver_alcohol.universe, [0.4, 0.6, 1.0, 1.0])

traffic_density["low"] = fuzz.trimf(traffic_density.universe, [0, 0, 1])
traffic_density["medium"] = fuzz.trimf(traffic_density.universe, [0, 1, 2])
traffic_density["high"] = fuzz.trimf(traffic_density.universe, [1, 2, 2])

vehicle_age["new"] = fuzz.trapmf(vehicle_age.universe, [0, 0, 5, 10])
vehicle_age["moderate"] = fuzz.trapmf(vehicle_age.universe, [7, 10, 25, 35])
vehicle_age["old"] = fuzz.trapmf(vehicle_age.universe, [30, 35, 50, 50])

speed_limit["low"] = fuzz.trapmf(speed_limit.universe, [30,30,60,80])
speed_limit["medium"] = fuzz.trapmf(speed_limit.universe, [60,80,120,150])
speed_limit["high"] = fuzz.trapmf(speed_limit.universe, [130,150,213,213])


failure_history["no"] = fuzz.trapmf(failure_history.universe, [0.0, 0.0, 0.2, 0.3])
failure_history["yes"] = fuzz.trapmf(failure_history.universe, [0.5, 0.7, 1.0, 1.0])

brake_condition["good"] = fuzz.trapmf(brake_condition.universe, [0.0, 0.0, 0.2, 0.3])
brake_condition["fair"] = fuzz.trimf(brake_condition.universe, [0.2, 0.5, 0.7])
brake_condition["poor"] = fuzz.trapmf(brake_condition.universe, [0.6, 0.8, 1.0, 1.0])

add_low_medium_high(weather_risk)
add_low_medium_high(lighting_risk)
add_low_medium_high(road_risk)
add_low_medium_high(time_risk)
add_low_medium_high(road_type_risk)
add_low_medium_high(vehicle_type_risk)
add_low_medium_high(road_defect_risk)
add_low_medium_high(intersection_risk)

risk["low"] = fuzz.trapmf(risk.universe, [0.0, 0.0, 0.25, 0.45])
risk["medium"] = fuzz.trimf(risk.universe, [0.35, 0.55, 0.75])
risk["high"] = fuzz.trapmf(risk.universe, [0.65, 0.8, 1.0, 1.0])

rules = [
    ctrl.Rule(weather_risk["high"] & road_risk["medium"] & lighting_risk["medium"] & road_defect_risk["medium"], risk["medium"]),
    ctrl.Rule(weather_risk["high"] & road_risk["high"] & lighting_risk["high"], risk["high"]),
    ctrl.Rule(weather_risk["low"] & road_risk["low"] & lighting_risk["low"], risk["low"]),
    ctrl.Rule(weather_risk["medium"] & road_risk["high"] & lighting_risk["high"], risk["high"]),
    ctrl.Rule(road_defect_risk["high"] & road_risk["medium"] & weather_risk["high"], risk["high"]),
    ctrl.Rule(road_defect_risk["low"] & road_risk["low"] & weather_risk["low"] & lighting_risk["low"], risk["low"]),

    ctrl.Rule(driver_age["young"] & vehicle_type_risk["high"] & time_risk["high"] & driver_experience["low"], risk["high"]),
    ctrl.Rule(driver_age["senior"] & traffic_density["high"] & intersection_risk["high"], risk["medium"]),
    ctrl.Rule(driver_age["middle"] & vehicle_type_risk["low"] & weather_risk["low"] & road_risk["low"] & driver_experience["high"], risk["low"]),
    ctrl.Rule(driver_alcohol["high"] & time_risk["high"] & lighting_risk["high"], risk["high"]),
    ctrl.Rule(driver_alcohol["high"] & vehicle_type_risk["high"] & road_risk["high"], risk["high"]),
    ctrl.Rule(driver_alcohol["none"] & driver_experience["high"] & weather_risk["low"] & road_risk["low"], risk["low"]),
    ctrl.Rule(driver_experience["low"] & speed_limit["high"] & road_type_risk["high"], risk["high"]),
    ctrl.Rule(driver_experience["medium"] & driver_alcohol["none"] & traffic_density["medium"] & weather_risk["medium"], risk["medium"]),

    ctrl.Rule(time_risk["high"] & lighting_risk["high"] & road_type_risk["high"], risk["high"]),
    ctrl.Rule(time_risk["high"] & traffic_density["high"], risk["medium"]),
    ctrl.Rule(intersection_risk["high"] & traffic_density["high"] & weather_risk["high"], risk["high"]),
    ctrl.Rule(road_type_risk["low"] & traffic_density["low"] & time_risk["medium"] & intersection_risk["low"], risk["low"]),
    ctrl.Rule(speed_limit["high"] & road_type_risk["high"] & weather_risk["high"], risk["high"]),
    ctrl.Rule(speed_limit["low"] & traffic_density["low"] & lighting_risk["low"], risk["low"]),
    ctrl.Rule(speed_limit["medium"] & intersection_risk["high"] & lighting_risk["medium"], risk["medium"]),
    ctrl.Rule(road_defect_risk["high"] & speed_limit["high"] & lighting_risk["high"], risk["high"]),

    ctrl.Rule(brake_condition["poor"] & road_risk["high"] & vehicle_type_risk["high"], risk["high"]),
    ctrl.Rule(vehicle_age["old"] & road_type_risk["high"] & weather_risk["high"], risk["high"]),
    ctrl.Rule(vehicle_age["new"] & brake_condition["good"] & weather_risk["low"], risk["low"]),
    ctrl.Rule(failure_history["yes"] & brake_condition["poor"] & driver_age["young"] & time_risk["high"], risk["high"]),
]

system = ctrl.ControlSystem(rules)


def classify_risk(score: float) -> str:
    if score < 0.4:
        return "Low Risk"
    if score < 0.7:
        return "Medium Risk"
    return "High Risk"

def get_risk_distribution(score: float) -> dict:
    low = interp_membership(risk.universe, risk["low"].mf, score)
    medium = interp_membership(risk.universe, risk["medium"].mf, score)
    high = interp_membership(risk.universe, risk["high"].mf, score)
    
    total = low + medium + high
    if total == 0:
        return {"low": 0.0, "medium": 0.0, "high": 0.0}
    
    return {
        "low": round((low/total) * 100, 2),
        "medium": round((medium/total) * 100, 2),
        "high": round((high/total)* 100, 2),
    }

def predict_crash_type(risk_level: str, inputs: dict) -> str:
    brake = str(inputs["brake_condition"]).lower()
    road = str(inputs["road_condition"]).lower()
    vehicle_type = str(inputs["vehicle_type"]).lower()
    alcohol = float(inputs["driver_alcohol"])
    speed_limit = int(inputs["speed_limit"])
    vehicle_age_value = int(inputs["vehicle_age"])
    failure = float(inputs["failure_history"])

    if risk_level == "High Risk":
        if vehicle_age_value >= 30 and brake == "poor":
            return "Tow due to crash"
        if alcohol >= 0.5 and speed_limit >= 130:
            return "Tow due to crash"
        if brake == "poor" and road in {"flood", "wet", "damp"}:
            return "Injury"
        return "Injury"

    if risk_level == "Medium Risk":
        if vehicle_age_value >= 7 and brake == "fair":
            return "Drive away"
        if failure < 0.5 and road in {"wet", "damp"}:
            return "Drive away"
        return "Drive away"

    if risk_level == "Low Risk":
        if vehicle_age_value <= 10 and brake == "good":
            return "No injury"
        return "Drive away"

    return "Drive away"


def predict_maintenance_required(risk_level: str, inputs: dict) -> str:
    brake = str(inputs["brake_condition"]).lower()
    vehicle_type = str(inputs["vehicle_type"]).lower()
    alcohol = float(inputs["driver_alcohol"])
    speed_limit = int(inputs["speed_limit"])
    vehicle_age_value = int(inputs["vehicle_age"])
    failure = float(inputs["failure_history"])

    if risk_level == "High Risk":
        if vehicle_age_value >= 30 and brake == "poor":
            return "Yes"
        if brake == "poor":
            return "Yes"
        if failure >= 0.5 and brake == "poor" and vehicle_type == "motorcycle":
            return "Yes"
        if alcohol >= 0.5 and speed_limit >= 130:
            return "No"
        return "Yes"

    if risk_level == "Medium Risk":
        if brake == "fair":
            return "No"
        if failure < 0.5:
            return "No"
        return "No"

    if risk_level == "Low Risk":
        if brake == "good":
            return "No"
        return "No"

    return "No"

def generate_recommendations(risk_level: str, reasons: list[str]) -> list[str]:
    recommendations = []

    if risk_level == "High Risk":
        recommendations.append("Delay travel if possible until conditions improve.")
        recommendations.append("Inspect the vehicle before departure, especially brakes and maintenance status.")
        recommendations.append("Avoid driving under alcohol influence.")
    elif risk_level == "Medium Risk":
        recommendations.append("Drive with caution and reduce speed in risky conditions.")
        recommendations.append("Double-check vehicle condition before departure.")
    else:
        recommendations.append("Proceed with normal caution and follow safe driving practices.")

    joined = " ".join(reasons).lower()

    if "alcohol" in joined:
        recommendations.append("Do not drive after drinking alcohol.")
    if "brake" in joined:
        recommendations.append("Have the braking system checked before travel.")
    if "maintenance" in joined or "vehicle" in joined:
        recommendations.append("Perform preventive maintenance before long trips.")
    if "weather" in joined or "road" in joined or "lighting" in joined:
        recommendations.append("Monitor weather and road visibility before departure.")
    if "traffic" in joined:
        recommendations.append("Choose a less congested route or travel at a safer time.")

    return list(dict.fromkeys(recommendations))


def evaluate_fuzzy(inputs: dict):
    sim = ctrl.ControlSystemSimulation(system)

    brake_value = safe_get(brake_map, inputs["brake_condition"])
    weather_value = safe_get(weather_map, inputs["weather"])
    lighting_value = safe_get(light_map, inputs["lighting"])
    road_value = safe_get(road_map, inputs["road_condition"])
    time_value = safe_get(time_map, inputs["time_of_day"])
    road_type_value = safe_get(road_type_map, inputs["road_type"])
    vehicle_type_value = safe_get(vehicle_type_map, inputs["vehicle_type"])
    road_defect_value = safe_get(road_defect_map, inputs["road_defect"])
    intersection_value = safe_get(intersection_map, inputs["intersection"])
    
    
    sim.input["driver_age"] = inputs["driver_age"]
    sim.input["driver_experience"] = inputs["driver_experience"]
    sim.input["driver_alcohol"] = float(inputs["driver_alcohol"])
    sim.input["traffic_density"] = inputs["traffic_density"]
    sim.input["vehicle_age"] = inputs["vehicle_age"]
    sim.input["failure_history"] = float(inputs["failure_history"])
    sim.input["brake_condition"] = brake_value
    sim.input["weather_risk"] = weather_value
    sim.input["lighting_risk"] = lighting_value
    sim.input["road_risk"] = road_value
    sim.input["time_risk"] = time_value
    sim.input["road_type_risk"] = road_type_value
    sim.input["speed_limit"] = inputs["speed_limit"]
    sim.input["vehicle_type_risk"] = vehicle_type_value
    sim.input["road_defect_risk"] = road_defect_value
    sim.input["intersection_risk"] = intersection_value

    sim.compute()
    score = float(sim.output.get("risk", 0.5))
    risk_level = classify_risk(score)
    risk_distribution = get_risk_distribution(score)
    predicted_crash_type = predict_crash_type(risk_level, inputs)
    predicted_maintenance = predict_maintenance_required(risk_level, inputs)
    
    reasons = []

    if float(inputs["driver_alcohol"]) >= 0.5:
        reasons.append("Driver alcohol level increased the accident risk.")

    if inputs["traffic_density"] == 2:
        reasons.append("High traffic density increased the accident risk.")

    if str(inputs["brake_condition"]).lower() == "poor":
        reasons.append("Poor brake condition increased the accident risk.")

    if float(inputs["failure_history"]) >= 0.5:
        reasons.append("Vehicle failure history increased the accident risk.")

    if inputs["vehicle_age"] >= 30:
        reasons.append("Old vehicle age increased the accident risk.")

    if inputs["driver_experience"] <= 8:
        reasons.append("Low driving experience increased the accident risk.")

    if str(inputs["weather"]).lower() in {"rain", "fog"}:
        reasons.append("Weather condition increased the accident risk.")

    if str(inputs["lighting"]).lower() in {"darkness"}:
        reasons.append("Poor lighting condition increased the accident risk.")

    if str(inputs["road_condition"]).lower() in {"wet", "damp", "flood"}:
        reasons.append("Road surface condition increased the accident risk.")

    if str(inputs["time_of_day"]).lower() == "evening":
        reasons.append("Time of travel increased the accident risk.")

    if str(inputs["road_type"]).lower() == "mountain road":
        reasons.append("Road type increased the accident risk.")

    if str(inputs["road_defect"]).lower() in {"worn surface", "ruts/holes"}:
        reasons.append("Road defects increased the accident risk.")

    if str(inputs["intersection"]).lower() == "at intersection":
        reasons.append("Intersection-related conditions increased the accident risk.")

    if inputs["speed_limit"] >= 130:
        reasons.append("High speed limit zone increased the accident risk.")

    if str(inputs["vehicle_type"]).lower() == "motorcycle":
        reasons.append("High-risk vehicle type increased the accident risk.")

    if not reasons:
        reasons.append("Input conditions stayed within safer ranges.")
    recommendations = generate_recommendations(risk_level, reasons)

    return score, risk_level, risk_distribution, predicted_crash_type, predicted_maintenance, reasons, recommendations