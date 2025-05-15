def build_html_report(student):
    student_id = student.get("student_id")
    events = student.get("events", [])

    if not student_id or not events:
        raise ValueError("Missing student_id or events")

    # Get sorted list of unique units
    sorted_units = sorted({event["unit"] for event in events})

    # Map unit numbers to Q1, Q2, ...
    unit_alias = {unit: f"Q{i+1}" for i, unit in enumerate(sorted_units)}

    # Build the event order string using the aliases
    event_order = ' -> '.join(unit_alias[event["unit"]] for event in events)

    # Format HTML output
    html = f"<h2>Student ID: {student_id}</h2>\n<p>Event Order: {event_order}</p>"

    return html, student_id
