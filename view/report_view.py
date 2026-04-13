def generate_report(client, inputs, score, risk_level, reasons, recommendations):
    reasons_text = "\n".join(f"- {reason}" for reason in reasons)
    recommendations_text = "\n".join(f"- {item}" for item in recommendations)

    report = f"""
=== PRE-DRIVING RISK REPORT ===

Client: {client}

--- INPUT SUMMARY ---
Driver Age: {inputs['driver_age']}
Driver Experience: {inputs['driver_experience']}
Alcohol Level: {inputs['driver_alcohol']}
Traffic Density: {inputs['traffic_density']}
Vehicle Age: {inputs['vehicle_age']}
Failure History: {inputs['failure_history']}
Maintenance Required: {inputs['maintenance_required']}
Brake Condition: {inputs['brake_condition']}
Weather: {inputs['weather']}
Lighting: {inputs['lighting']}
Road Condition: {inputs['road_condition']}
Time of Day: {inputs['time_of_day']}
Road Type: {inputs['road_type']}

--- RESULT ---
Risk Score: {score:.2f}
Risk Level: {risk_level}

--- WHY THIS RISK WAS GENERATED ---
{reasons_text}

--- ADVISORY RECOMMENDATIONS ---
{recommendations_text}

===============================
""".strip()

    return report


def display_report(report):
    print("\n=== RISK REPORT ===")
    print(report)