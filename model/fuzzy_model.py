import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from mappings.categorical_map import (
    brake_map,
    weather_map,
    light_map,
    road_map,
    time_map,
    road_type_map,
    safe_get,
)

driver_age = ctrl.Antecedent(np.arange(18, 71, 1), "driver_age")
driver_experience = ctrl.Antecedent(np.arange(0, 51, 1), "driver_experience")
driver_alcohol = ctrl.Antecedent(np.arange(0, 1.01, 0.01), "driver_alcohol")
traffic_density = ctrl.Antecedent(np.arange(0, 3, 1), "traffic_density")
vehicle_age = ctrl.Antecedent(np.arange(0, 22, 1), "vehicle_age")
failure_history = ctrl.Antecedent(np.arange(0, 1.01, 0.01), "failure_history")
maintenance_required = ctrl.Antecedent(np.arange(0, 1.01, 0.01), "maintenance_required")
brake_condition = ctrl.Antecedent(np.arange(0, 1.01, 0.01), "brake_condition")

weather_risk = ctrl.Antecedent(np.arange(0, 1.01, 0.01), "weather_risk")
lighting_risk = ctrl.Antecedent(np.arange(0, 1.01, 0.01), "lighting_risk")
road_risk = ctrl.Antecedent(np.arange(0, 1.01, 0.01), "road_risk")
time_risk = ctrl.Antecedent(np.arange(0, 1.01, 0.01), "time_risk")
road_type_risk = ctrl.Antecedent(np.arange(0, 1.01, 0.01), "road_type_risk")

risk = ctrl.Consequent(np.arange(0, 1.01, 0.01), "risk")


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

vehicle_age["new"] = fuzz.trapmf(vehicle_age.universe, [0, 0, 5, 8])
vehicle_age["moderate"] = fuzz.trapmf(vehicle_age.universe, [6, 9, 14, 17])
vehicle_age["old"] = fuzz.trapmf(vehicle_age.universe, [15, 18, 21, 21])

failure_history["no"] = fuzz.trapmf(failure_history.universe, [0.0, 0.0, 0.2, 0.3])
failure_history["yes"] = fuzz.trapmf(failure_history.universe, [0.5, 0.7, 1.0, 1.0])

maintenance_required["low"] = fuzz.trapmf(maintenance_required.universe, [0.0, 0.0, 0.3, 0.5])
maintenance_required["high"] = fuzz.trapmf(maintenance_required.universe, [0.4, 0.6, 1.0, 1.0])

brake_condition["good"] = fuzz.trapmf(brake_condition.universe, [0.0, 0.0, 0.2, 0.3])
brake_condition["fair"] = fuzz.trimf(brake_condition.universe, [0.2, 0.5, 0.7])
brake_condition["poor"] = fuzz.trapmf(brake_condition.universe, [0.6, 0.8, 1.0, 1.0])

add_low_medium_high(weather_risk)
add_low_medium_high(lighting_risk)
add_low_medium_high(road_risk)
add_low_medium_high(time_risk)
add_low_medium_high(road_type_risk)

risk["low"] = fuzz.trapmf(risk.universe, [0.0, 0.0, 0.25, 0.45])
risk["medium"] = fuzz.trimf(risk.universe, [0.35, 0.55, 0.75])
risk["high"] = fuzz.trapmf(risk.universe, [0.65, 0.8, 1.0, 1.0])

rules = [
    ctrl.Rule(driver_alcohol["high"], risk["high"]),
    ctrl.Rule(traffic_density["high"] & brake_condition["poor"], risk["high"]),
    ctrl.Rule(vehicle_age["old"] & maintenance_required["high"], risk["high"]),
    ctrl.Rule(failure_history["yes"] & brake_condition["poor"], risk["high"]),
    ctrl.Rule(driver_experience["low"] & traffic_density["high"], risk["high"]),
    ctrl.Rule(driver_experience["high"] & traffic_density["low"], risk["low"]),
    ctrl.Rule(driver_age["senior"] & traffic_density["high"], risk["high"]),
    ctrl.Rule(driver_alcohol["none"] & brake_condition["good"], risk["low"]),
    ctrl.Rule(weather_risk["high"], risk["high"]),
    ctrl.Rule(lighting_risk["high"] & time_risk["high"], risk["high"]),
    ctrl.Rule(road_risk["high"], risk["high"]),
    ctrl.Rule(road_type_risk["high"] & traffic_density["high"], risk["high"]),
    ctrl.Rule(weather_risk["low"] & road_risk["low"] & brake_condition["good"], risk["low"]),
]

system = ctrl.ControlSystem(rules)


def classify_risk(score: float) -> str:
    if score < 0.4:
        return "Low Risk"
    if score < 0.7:
        return "Medium Risk"
    return "High Risk"


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

    sim.input["driver_age"] = inputs["driver_age"]
    sim.input["driver_experience"] = inputs["driver_experience"]
    sim.input["driver_alcohol"] = float(inputs["driver_alcohol"])
    sim.input["traffic_density"] = inputs["traffic_density"]
    sim.input["vehicle_age"] = inputs["vehicle_age"]
    sim.input["failure_history"] = float(inputs["failure_history"])
    sim.input["maintenance_required"] = float(inputs["maintenance_required"])
    sim.input["brake_condition"] = brake_value
    sim.input["weather_risk"] = weather_value
    sim.input["lighting_risk"] = lighting_value
    sim.input["road_risk"] = road_value
    sim.input["time_risk"] = time_value
    sim.input["road_type_risk"] = road_type_value

    sim.compute()
    score = float(sim.output.get("risk", 0.5))
    risk_level = classify_risk(score)

    reasons = []

    if float(inputs["driver_alcohol"]) >= 0.3:
        reasons.append("Alcohol level increased the risk.")
    if inputs["traffic_density"] == 2:
        reasons.append("High traffic density increased the risk.")
    if str(inputs["brake_condition"]).lower() == "poor":
        reasons.append("Poor brake condition increased the risk.")
    if float(inputs["maintenance_required"]) >= 0.5:
        reasons.append("Vehicle maintenance requirement increased the risk.")
    if float(inputs["failure_history"]) >= 0.5:
        reasons.append("Vehicle failure history increased the risk.")
    if inputs["vehicle_age"] >= 15:
        reasons.append("Old vehicle age increased the risk.")
    if inputs["driver_experience"] <= 5:
        reasons.append("Low driving experience increased the risk.")
    if str(inputs["weather"]).lower() in {"rain", "heavy rain", "storm", "fog", "foggy"}:
        reasons.append("Weather condition increased the risk.")
    if str(inputs["lighting"]).lower() in {"darkness-lights unlit", "unlit", "no lighting"}:
        reasons.append("Poor lighting condition increased the risk.")
    if str(inputs["road_condition"]).lower() in {"slippery", "muddy", "flood"}:
        reasons.append("Road condition increased the risk.")
    if str(inputs["time_of_day"]).lower() in {"evening", "night"}:
        reasons.append("Time of travel increased the risk.")
    if str(inputs["road_type"]).lower() == "mountain road":
        reasons.append("Road type increased the risk.")

    if not reasons:
        reasons.append("Input conditions stayed within safer ranges.")

    recommendations = generate_recommendations(risk_level, reasons)

    return score, risk_level, reasons, recommendations