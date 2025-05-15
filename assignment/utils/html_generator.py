def build_html_report(student):
    student_id = student.get("student_id")
    events = student.get("events", [])

    if not student_id or not isinstance(events, list) or not events:
        raise ValueError("Invalid student record: missing student_id or events")

    unique_units = sorted(set(event["unit"] for event in events))
    unit_to_q = {unit: f"Q{i+1}" for i, unit in enumerate(unique_units)}
    event_order = [unit_to_q[event["unit"]] for event in events]

    html = f"""<h2>Student ID: {student_id}</h2>
        <p>Event Order: {' -> '.join(event_order)}</p>
    """
    return html, student_id
