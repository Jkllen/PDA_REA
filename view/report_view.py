def generate_report(
    client,
    inputs,
    score,
    risk_level,
    risk_distribution,
    predicted_crash_type,
    predicted_maintenance,
    reasons,
    recommendations,
):
    reasons_text = "\n".join(f"- {reason}" for reason in reasons)
    recommendations_text = "\n".join(f"- {item}" for item in recommendations)

    failure_text = "Yes" if float(inputs["failure_history"]) >= 0.5 else "No"

    report = f"""
=== PRE-DRIVING ACCIDENT RISK REPORT ===

Client: {client}

--- INPUT SUMMARY ---
Driver Age: {inputs['driver_age']}
Driver Experience: {inputs['driver_experience']}
Alcohol Level: {inputs['driver_alcohol']}
Traffic Density: {inputs['traffic_density']}
Vehicle Age: {inputs['vehicle_age']}
Vehicle Type: {inputs['vehicle_type']}
Failure History: {failure_text}
Brake Condition: {inputs['brake_condition']}
Weather: {inputs['weather']}
Lighting: {inputs['lighting']}
Road Condition: {inputs['road_condition']}
Time of Day: {inputs['time_of_day']}
Road Type: {inputs['road_type']}
Road Defect: {inputs['road_defect']}
Intersection: {inputs['intersection']}
Speed Limit: {inputs['speed_limit']}

--- RESULT ---
Accident Risk Level: {risk_level}
Severity Score: {score:.2f}
Predicted Crash Type: {predicted_crash_type}
Predicted Maintenance Required: {predicted_maintenance}

--- RISK DISTRIBUTION ---
Low Risk: {risk_distribution['low']:.2f}%
Medium Risk: {risk_distribution['medium']:.2f}%
High Risk: {risk_distribution['high']:.2f}%

--- WHY THIS RESULT WAS GENERATED ---
{reasons_text}

--- ADVISORY RECOMMENDATIONS ---
{recommendations_text}

======================================
""".strip()

    return report