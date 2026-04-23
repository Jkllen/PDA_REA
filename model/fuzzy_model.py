import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from skfuzzy import interp_membership

from mappings.categorical_map import (
    safe_get,
    alcohol_map,
    driving_experience_map,
    time_of_day_map,
    trip_duration_map,
    weather_map,
    visible_road_issues_map,
    road_type_map,
    traffic_level_map,
    road_condition_map,
    intersection_map,
    vehicle_type_map,
    mechanical_issues_map,
    vehicle_age_map,
    brake_condition_map,
    maintenance_map,
)

# =========================================================
# ANTECEDENTS
# =========================================================
driver_age = ctrl.Antecedent(np.arange(18, 71, 1), "driver_age")

alcohol_risk = ctrl.Antecedent(np.arange(0.0, 1.01, 0.01), "alcohol_risk")
experience_risk = ctrl.Antecedent(np.arange(0.0, 1.01, 0.01), "experience_risk")
time_risk = ctrl.Antecedent(np.arange(0.0, 1.01, 0.01), "time_risk")
trip_duration_risk = ctrl.Antecedent(np.arange(0.0, 1.01, 0.01), "trip_duration_risk")

weather_risk = ctrl.Antecedent(np.arange(0.0, 1.01, 0.01), "weather_risk")
road_issue_risk = ctrl.Antecedent(np.arange(0.0, 1.01, 0.01), "road_issue_risk")
road_type_risk = ctrl.Antecedent(np.arange(0.0, 1.01, 0.01), "road_type_risk")
traffic_risk = ctrl.Antecedent(np.arange(0.0, 1.01, 0.01), "traffic_risk")
road_condition_risk = ctrl.Antecedent(np.arange(0.0, 1.01, 0.01), "road_condition_risk")
intersection_risk = ctrl.Antecedent(np.arange(0.0, 1.01, 0.01), "intersection_risk")

vehicle_type_risk = ctrl.Antecedent(np.arange(0.0, 1.01, 0.01), "vehicle_type_risk")
mechanical_risk = ctrl.Antecedent(np.arange(0.0, 1.01, 0.01), "mechanical_risk")
vehicle_age_risk = ctrl.Antecedent(np.arange(0.0, 1.01, 0.01), "vehicle_age_risk")
brake_risk = ctrl.Antecedent(np.arange(0.0, 1.01, 0.01), "brake_risk")
maintenance_risk = ctrl.Antecedent(np.arange(0.0, 1.01, 0.01), "maintenance_risk")

risk = ctrl.Consequent(np.arange(0.0, 1.01, 0.01), "risk")


# =========================================================
# MEMBERSHIP FUNCTIONS
# =========================================================
def add_low_medium_high(variable):
    variable["low"] = fuzz.trapmf(variable.universe, [0.0, 0.0, 0.20, 0.40])
    variable["medium"] = fuzz.trimf(variable.universe, [0.30, 0.50, 0.80])
    variable["high"] = fuzz.trapmf(variable.universe, [0.75, 0.90, 1.0, 1.0])


driver_age["young"] = fuzz.trapmf(driver_age.universe, [18, 18, 25, 35])
driver_age["middle"] = fuzz.trapmf(driver_age.universe, [28, 35, 55, 62])
driver_age["senior"] = fuzz.trapmf(driver_age.universe, [55, 62, 70, 70])

for variable in (
    alcohol_risk,
    experience_risk,
    time_risk,
    trip_duration_risk,
    weather_risk,
    road_issue_risk,
    road_type_risk,
    traffic_risk,
    road_condition_risk,
    intersection_risk,
    vehicle_type_risk,
    mechanical_risk,
    vehicle_age_risk,
    brake_risk,
    maintenance_risk,
):
    add_low_medium_high(variable)

risk["low"] = fuzz.trapmf(risk.universe, [0.0, 0.0, 0.28, 0.48])
risk["medium"] = fuzz.trimf(risk.universe, [0.35, 0.55, 0.75])
risk["high"] = fuzz.trapmf(risk.universe, [0.62, 0.78, 1.0, 1.0])


# =========================================================
# RULES
# =========================================================
rules = [
    # Safer baseline
    # Rule 0 
    ctrl.Rule(
        alcohol_risk["low"]
        & experience_risk["low"]
        & weather_risk["low"]
        & road_condition_risk["low"]
        & traffic_risk["low"]
        & brake_risk["low"]
        & mechanical_risk["low"]
        & maintenance_risk["low"],
        risk["low"],
    ), # DEAD RULE

    # Alcohol-related rules
    # Rule 1-4
    # Alcohol dominates everything
    ctrl.Rule(alcohol_risk["high"], risk["high"]),
    ctrl.Rule(alcohol_risk["medium"] & (time_risk["high"] | trip_duration_risk["high"]), risk["high"]),
    ctrl.Rule(alcohol_risk["medium"], risk["medium"]),

    # Experience and age
    # Rule 5-10
    ctrl.Rule(experience_risk["high"] & (traffic_risk["high"] | time_risk["high"]), risk["high"]),
    ctrl.Rule(driver_age["young"] & experience_risk["high"], risk["high"]),
    ctrl.Rule(driver_age["senior"] & (weather_risk["high"] | traffic_risk["high"]), risk["high"]),

    # Time and trip exposure
    # Rule 11-14
    ctrl.Rule(time_risk["high"] & trip_duration_risk["high"], risk["high"]),
    ctrl.Rule(trip_duration_risk["high"] & traffic_risk["high"], risk["high"]),
    ctrl.Rule(trip_duration_risk["high"] & experience_risk["medium"], risk["medium"]),

    # Weather / environment
    # Rule 15-28
    ctrl.Rule(weather_risk["high"] & (road_condition_risk["high"] | road_issue_risk["high"]), risk["high"]),
    ctrl.Rule(traffic_risk["high"] & intersection_risk["high"], risk["high"]),
    ctrl.Rule(road_condition_risk["high"] & traffic_risk["high"], risk["high"]),
    ctrl.Rule(weather_risk["medium"] & traffic_risk["medium"], risk["medium"]),

    # Vehicle-related rules
    # Rule 29-37
    ctrl.Rule(brake_risk["high"], risk["high"]),
    ctrl.Rule(mechanical_risk["high"] & maintenance_risk["high"], risk["high"]),
    ctrl.Rule(vehicle_age_risk["high"] & maintenance_risk["high"], risk["high"]),
    ctrl.Rule(vehicle_type_risk["high"] & (weather_risk["high"] | road_condition_risk["high"]), risk["high"]),

    # Mixed moderate-risk combinations
    # Rule 38-42
    ctrl.Rule(
        experience_risk["medium"]
        & weather_risk["medium"]
        & traffic_risk["medium"],
        risk["medium"],
    ),

    ctrl.Rule(
        brake_risk["medium"]
        & road_condition_risk["medium"]
        & weather_risk["medium"],
        risk["medium"],
    ),

    # Strong low-risk combinations
    # Rule43
    ctrl.Rule(
        weather_risk["low"]
        & road_condition_risk["low"]
        & road_issue_risk["low"]
        & traffic_risk["low"]
        & brake_risk["low"]
        & mechanical_risk["low"]
        & maintenance_risk["low"]
        & alcohol_risk["low"]
        & experience_risk["low"],
        risk["low"],
    ), # DEAD RULE
]

system = ctrl.ControlSystem(rules)


# =========================================================
# HELPERS
# =========================================================
def classify_risk(score: float) -> str:
    if score < 0.40:
        return "Low Risk"
    if score < 0.68:
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
        "low": round((low / total) * 100, 2),
        "medium": round((medium / total) * 100, 2),
        "high": round((high / total) * 100, 2),
    }


def build_reasons(inputs: dict) -> list[str]:
    reasons = []

    alcohol_value = safe_get(alcohol_map, inputs["alcohol_consumption"], 0.0)
    exp_value = safe_get(driving_experience_map, inputs["driving_experience"], 0.5)
    time_value = safe_get(time_of_day_map, inputs["time_of_day"], 0.5)
    duration_value = safe_get(trip_duration_map, inputs["expected_trip_duration"], 0.5)
    weather_value = safe_get(weather_map, inputs["weather_condition"], 0.5)
    road_issue_value = safe_get(visible_road_issues_map, inputs["visible_road_issues"], 0.5)
    road_type_value = safe_get(road_type_map, inputs["road_type"], 0.5)
    traffic_value = safe_get(traffic_level_map, inputs["traffic_level"], 0.5)
    road_condition_value = safe_get(road_condition_map, inputs["road_condition"], 0.5)
    intersection_value = safe_get(intersection_map, inputs["intersections_busy_crossings"], 0.5)
    vehicle_type_value = safe_get(vehicle_type_map, inputs["vehicle_type"], 0.5)
    mechanical_value = safe_get(mechanical_issues_map, inputs["recent_mechanical_issues"], 0.5)
    vehicle_age_value = safe_get(vehicle_age_map, inputs["vehicle_age"], 0.5)
    brake_value = safe_get(brake_condition_map, inputs["brake_condition"], 0.5)
    maintenance_value = safe_get(maintenance_map, inputs["last_vehicle_maintenance"], 0.5)

    if alcohol_value >= 0.70:
        reasons.append("Alcohol consumption before driving significantly increased the accident risk.")
    elif alcohol_value >= 0.35:
        reasons.append("Recent alcohol consumption increased the accident risk.")

    if exp_value >= 0.75:
        reasons.append("Limited driving experience increased the accident risk.")
    elif exp_value >= 0.50:
        reasons.append("Moderate driving experience still contributed to the accident risk.")

    if time_value >= 0.85:
        reasons.append("Driving during late-night or early-morning hours increased the accident risk.")
    elif time_value >= 0.60:
        reasons.append("Time of travel increased the accident risk.")

    if duration_value >= 0.70:
        reasons.append("Longer trip duration increased exposure and fatigue-related risk.")

    if weather_value >= 0.80:
        reasons.append("Severe weather condition increased the accident risk.")
    elif weather_value >= 0.55:
        reasons.append("Weather condition increased the accident risk.")

    if road_issue_value >= 0.80:
        reasons.append("Serious visible road issues increased the accident risk.")
    elif road_issue_value >= 0.55:
        reasons.append("Road issues along the route increased the accident risk.")
    elif str(inputs["visible_road_issues"]).strip().lower() == "not sure":
        reasons.append("Uncertainty about visible road issues contributed to the accident risk.")

    if road_type_value >= 0.90:
        reasons.append("Mountain or curved road conditions increased the accident risk.")
    elif road_type_value >= 0.65:
        reasons.append("Road type increased the accident risk.")

    if traffic_value >= 0.90:
        reasons.append("Severe traffic congestion increased the accident risk.")
    elif traffic_value >= 0.70:
        reasons.append("Heavy traffic increased the accident risk.")

    if road_condition_value >= 1.00:
        reasons.append("Flooded road condition greatly increased the accident risk.")
    elif road_condition_value >= 0.70:
        reasons.append("Unsafe road condition increased the accident risk.")
    elif road_condition_value >= 0.65:
        reasons.append("Wet or slippery road condition increased the accident risk.")

    if intersection_value >= 0.75:
        reasons.append("Frequent intersections or busy crossings increased the accident risk.")
    elif intersection_value >= 0.45:
        reasons.append("Intersections along the trip contributed to the accident risk.")

    if vehicle_type_value >= 0.95:
        reasons.append("Motorcycle use increased the accident risk due to greater exposure.")
    elif vehicle_type_value >= 0.45:
        reasons.append("Vehicle type contributed to the accident risk.")

    if mechanical_value >= 1.00:
        reasons.append("Major mechanical issues greatly increased the accident risk.")
    elif mechanical_value >= 0.70:
        reasons.append("Mechanical issues needing attention increased the accident risk.")
    elif mechanical_value >= 0.40:
        reasons.append("Existing mechanical issues contributed to the accident risk.")
    elif str(inputs["recent_mechanical_issues"]).strip().lower() == "not sure":
        reasons.append("Uncertainty about recent mechanical issues contributed to the accident risk.")

    if vehicle_age_value >= 0.85:
        reasons.append("Older vehicle age increased the accident risk.")
    elif vehicle_age_value >= 0.65:
        reasons.append("Vehicle age contributed to the accident risk.")

    if brake_value >= 1.00:
        reasons.append("Weak or unreliable brake condition greatly increased the accident risk.")
    elif brake_value >= 0.75:
        reasons.append("Brake condition increased the accident risk.")
    elif brake_value >= 0.40:
        reasons.append("Brake responsiveness should be checked before travel.")
    elif str(inputs["brake_condition"]).strip().lower() == "not sure":
        reasons.append("Uncertainty about brake condition contributed to the accident risk.")

    if maintenance_value >= 0.90:
        reasons.append("Overdue vehicle maintenance increased the accident risk.")
    elif maintenance_value >= 0.60:
        reasons.append("Vehicle maintenance history increased the accident risk.")
    elif maintenance_value >= 0.30:
        reasons.append("Maintenance timing should be monitored before travel.")
    elif str(inputs["last_vehicle_maintenance"]).strip().lower() == "cannot remember":
        reasons.append("Uncertainty about last vehicle maintenance contributed to the accident risk.")

    if not reasons:
        reasons.append("Input conditions stayed within safer operating ranges.")

    return reasons


def generate_recommendations(risk_level: str, reasons: list[str]) -> list[str]:
    recommendations = []

    if risk_level == "High Risk":
        recommendations.extend([
            "Delay or cancel the trip until the major risk factors are resolved.",
            "Do not proceed unless the vehicle is safe and the driver is fit to travel.",
            "Consider alternate transportation or another qualified driver.",
        ])
    elif risk_level == "Medium Risk":
        recommendations.extend([
            "Proceed only with extra caution.",
            "Inspect the vehicle and reassess conditions before departure.",
            "Reduce travel exposure by choosing a safer route or time of departure.",
        ])
    else:
        recommendations.extend([
            "Proceed with normal caution.",
            "Continue following standard road safety practices.",
        ])

    joined = " ".join(reasons).lower()

    if "alcohol" in joined:
        recommendations.append("Do not drive after alcohol consumption.")
    if "experience" in joined:
        recommendations.append("Drive conservatively and avoid unnecessary high-risk routes.")
    if "late-night" in joined or "early-morning" in joined or "time of travel" in joined:
        recommendations.append("Avoid driving during high-risk hours if possible.")
    if "trip duration" in joined or "fatigue" in joined:
        recommendations.append("Plan rest breaks and avoid fatigue during longer trips.")
    if "weather" in joined:
        recommendations.append("Monitor weather updates before departure.")
    if "road issues" in joined or "road condition" in joined:
        recommendations.append("Choose a safer route if current road conditions are poor.")
    if "traffic" in joined:
        recommendations.append("Travel at a less congested time if possible.")
    if "intersection" in joined:
        recommendations.append("Slow down and stay alert near intersections and crossings.")
    if "motorcycle" in joined or "vehicle type" in joined:
        recommendations.append("Use extra caution based on the vehicle’s operating risks.")
    if "mechanical" in joined:
        recommendations.append("Have mechanical issues checked before continuing the trip.")
    if "brake" in joined:
        recommendations.append("Inspect or repair the braking system before travel.")
    if "maintenance" in joined:
        recommendations.append("Schedule or complete vehicle maintenance as soon as possible.")

    return list(dict.fromkeys(recommendations))


# =========================================================
# MAIN EVALUATION
# =========================================================
def evaluate_fuzzy(inputs: dict):
    global sim
    sim = ctrl.ControlSystemSimulation(system)

    sim.input["driver_age"] = int(inputs["driver_age"])

    sim.input["alcohol_risk"] = safe_get(alcohol_map, inputs["alcohol_consumption"], 0.0)
    sim.input["experience_risk"] = safe_get(driving_experience_map, inputs["driving_experience"])
    sim.input["time_risk"] = safe_get(time_of_day_map, inputs["time_of_day"])
    sim.input["trip_duration_risk"] = safe_get(trip_duration_map, inputs["expected_trip_duration"])

    sim.input["weather_risk"] = safe_get(weather_map, inputs["weather_condition"])
    sim.input["road_issue_risk"] = safe_get(visible_road_issues_map, inputs["visible_road_issues"])
    sim.input["road_type_risk"] = safe_get(road_type_map, inputs["road_type"])
    sim.input["traffic_risk"] = safe_get(traffic_level_map, inputs["traffic_level"])
    sim.input["road_condition_risk"] = safe_get(road_condition_map, inputs["road_condition"])
    sim.input["intersection_risk"] = safe_get(intersection_map, inputs["intersections_busy_crossings"])

    sim.input["vehicle_type_risk"] = safe_get(vehicle_type_map, inputs["vehicle_type"])
    sim.input["mechanical_risk"] = safe_get(mechanical_issues_map, inputs["recent_mechanical_issues"])
    sim.input["vehicle_age_risk"] = safe_get(vehicle_age_map, inputs["vehicle_age"])
    sim.input["brake_risk"] = safe_get(brake_condition_map, inputs["brake_condition"])
    sim.input["maintenance_risk"] = safe_get(maintenance_map, inputs["last_vehicle_maintenance"])

    sim.compute()

    score = float(sim.output.get("risk", 0.5))
    risk_level = classify_risk(score)
    risk_distribution = get_risk_distribution(score)
    reasons = build_reasons(inputs)
    recommendations = generate_recommendations(risk_level, reasons)

    return score, risk_level, risk_distribution, reasons, recommendations


# =====================================================================


### TESTING ONLY


# =====================================================================
import numpy as np

def sample_inputs(n=1000):
    rng = np.random.default_rng(42)
    samples = []

    for _ in range(n):
        samples.append({
            "driver_age": rng.uniform(18, 70),
            "alcohol_risk": rng.uniform(0, 1),
            "experience_risk": rng.uniform(0, 1),
            "time_risk": rng.uniform(0, 1),
            "trip_duration_risk": rng.uniform(0, 1),
            "weather_risk": rng.uniform(0, 1),
            "road_issue_risk": rng.uniform(0, 1),
            "road_type_risk": rng.uniform(0, 1),
            "traffic_risk": rng.uniform(0, 1),
            "road_condition_risk": rng.uniform(0, 1),
            "intersection_risk": rng.uniform(0, 1),
            "vehicle_type_risk": rng.uniform(0, 1),
            "mechanical_risk": rng.uniform(0, 1),
            "vehicle_age_risk": rng.uniform(0, 1),
            "brake_risk": rng.uniform(0, 1),
            "maintenance_risk": rng.uniform(0, 1),
        })
    return samples

def analyze_rule_activation(samples):
    rules_list = list(system.rules)
    n_rules = len(rules_list)

    total_activation = np.zeros(n_rules)
    fire_count = np.zeros(n_rules)

    for s in samples:
        sim = ctrl.ControlSystemSimulation(system)

        for k, v in s.items():
            sim.input[k] = v

        sim.compute()

        for i, rule in enumerate(rules_list):
            strength = rule.aggregate_firing[sim]

            total_activation[i] += strength
            if strength > 0.01:
                fire_count[i] += 1

    avg_activation = total_activation / len(samples)
    fire_rate = fire_count / len(samples)

    return avg_activation, fire_rate

import matplotlib.pyplot as plt

def plot_rule_stats(avg_activation, fire_rate):
    idx = np.arange(len(avg_activation))

    plt.figure()
    plt.scatter(avg_activation, fire_rate)

    for i in idx:
        plt.text(avg_activation[i], fire_rate[i], str(i), fontsize=8)

    plt.xlabel("Average Activation Strength")
    plt.ylabel("Firing Frequency")
    plt.title("Rule Activation Map")
    plt.grid()
    plt.show()

def get_rule_output_label(rule):
    try:
        return rule.consequent[0].term.label
    except Exception:
        return "unknown"

def detect_conflicts(samples, threshold=0.3):
    conflicts = []
    rules_list = list(system.rules)

    for s in samples:
        sim = ctrl.ControlSystemSimulation(system)

        for k, v in s.items():
            sim.input[k] = v

        sim.compute()

        active_rules = []

        for i, rule in enumerate(rules_list):
            strength = rule.aggregate_firing[sim]

            if strength > threshold:
                label = get_rule_output_label(rule)
                active_rules.append((i, label))

        for i in range(len(active_rules)):
            for j in range(i + 1, len(active_rules)):
                if active_rules[i][1] != active_rules[j][1]:
                    conflicts.append((active_rules[i], active_rules[j]))

    return conflicts

def group_rules_by_output():
    groups = {"low": [], "medium": [], "high": []}

    rules_list = list(system.rules)
    for i, rule in enumerate(rules_list):
        consequent = list(rule.consequent.keys())[0]
        label = list(rule.consequent[consequent].keys())[0]
        groups[label].append(i)

    return groups

def rule_coverage_report(avg_activation, fire_rate):
    avg_activation = np.asarray(avg_activation, dtype=float)
    fire_rate = np.asarray(fire_rate, dtype=float)

    for i, (a, f) in enumerate(zip(avg_activation, fire_rate)):

        if f < 0.05:
            print(f"[Rule {i}] ❌ Rarely fires | freq={f:.3f}")

        elif f > 0.8:
            print(f"[Rule {i}] ⚠️ Always active | freq={f:.3f}")

        elif a > 0.5:
            print(f"[Rule {i}] 🔥 Strong influence | activation={a:.3f}")

def inspect_rules(input_dict, top_n=10):
    sim = ctrl.ControlSystemSimulation(system)

    for k, v in input_dict.items():
        for k2, v2 in v.items():
            sim.input[k2] = float(v2)

    sim.compute()

    activations = []

    for i, rule in enumerate(system.rules):
        strength = rule.aggregate_firing[sim]
        activations.append((i, strength, str(rule)))

    activations.sort(key=lambda x: -x[1])

    with open('output.txt', 'a') as f:
        for i, strength, rule_text in activations[:top_n]:
            print(f"[{i}] strength={strength:.3f}", file=f)
            print(rule_text, file=f)
            print("-" * 50, file=f)

def plot_memberships(variable):
    plt.figure()

    for label in variable.terms:
        plt.plot(variable.universe, variable[label].mf, label=label)

    plt.title(variable.label)
    plt.legend()
    plt.grid()
    plt.show()

samples = sample_inputs(1000)

avg_activation, fire_rate = analyze_rule_activation(samples)

plot_memberships(alcohol_risk)
plot_memberships(risk)

rule_coverage_report(avg_activation, fire_rate)

conflicts = detect_conflicts(samples[:200])
print("Conflicts found:", len(conflicts))

inspect_rules(dict(enumerate(samples)))

plot_rule_stats(avg_activation, fire_rate)