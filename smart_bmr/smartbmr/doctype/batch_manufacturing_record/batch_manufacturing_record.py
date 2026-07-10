import frappe
from frappe.model.document import Document

class BatchManufacturingRecord(Document):
    pass

@frappe.whitelist(allow_guest=True)
def log_machine_temperature(bmr_id, temp_reading):
    doc = frappe.get_doc("Batch Manufacturing Record", bmr_id)
    
    if doc.workflow_state != "In Production":
        frappe.throw("Machine rejected: BMR is not In Production.")
        
    current_temp = float(temp_reading)
    MIN_SAFE_TEMP = 36.0
    MAX_SAFE_TEMP = 39.0
    
    is_current_anomaly = (current_temp < MIN_SAFE_TEMP or current_temp > MAX_SAFE_TEMP)
    
    last_row = doc.process_log[-1] if doc.process_log else None
    
    was_last_anomaly = False
    if last_row and last_row.actual_temp_reading:
        last_temp = float(last_row.actual_temp_reading)
        was_last_anomaly = (last_temp < MIN_SAFE_TEMP or last_temp > MAX_SAFE_TEMP)

    should_log = False
    log_step = "NORMAL"
    log_instruction = ""

    if is_current_anomaly:
        should_log = True
        log_step = "ANOMALY"
        log_instruction = "CRITICAL OUT-OF-SPEC TEMPERATURE DETECTED"
    else:
        if not last_row:
            should_log = True
            log_instruction = "Initial state check: Production started safely."
        elif was_last_anomaly:
            should_log = True
            log_instruction = "Recovery marker: First normal temperature after anomaly phase."

    if should_log:
        doc.append("process_log", {
            "step_number": log_step, 
            "instructions": log_instruction,
            "minimum_temp": MIN_SAFE_TEMP,
            "maximum_temp": MAX_SAFE_TEMP,
            "actual_temp_reading": current_temp
        })
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        return {"status": "logged", "message": f"State captured: {log_step} at {current_temp}°C"}
        
    return {"status": "ignored", "message": "Stable condition continues. Log suppressed."}