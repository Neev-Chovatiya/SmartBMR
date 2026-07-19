# Copyright (c) 2026, Neev Chovatiya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BatchManufacturingRecord(Document):
    def validate(self):
        has_anomaly = any(str(row.step_number).strip() in ["ANOMALY", "0"] for row in self.process_log)
        if has_anomaly and self.workflow_state == "Completed" and not self.supervisor_investigation_remarks:
            frappe.throw("Supervisor Investigation Remarks are mandatory for anomalous batches.")
            
        self.calculate_quality_metrics()

    def calculate_quality_metrics(self):
        min_limit = 36.0
        max_limit = 39.0
        
        highest_temp = 0.0
        if self.process_log:
            for row in self.process_log:
                temp = float(row.actual_temp_reading or 0.0)
                if temp > highest_temp:
                    highest_temp = temp
        self.peak_temperature = round(highest_temp, 3)

        total_raw_pings = frappe.db.count("IoT Temperature Log", filters={"batch_record_id": self.name})
        
        raw_anomalies = frappe.db.sql("""
            SELECT COUNT(*) 
            FROM `tabIoT Temperature Log` 
            WHERE batch_record_id = %s 
              AND (temperature < %s OR temperature > %s)
        """, (self.name, min_limit, max_limit))[0][0] or 0

        self.excursion_duration = int(raw_anomalies)

        if total_raw_pings > 0:
            stability = (float(total_raw_pings - raw_anomalies) / float(total_raw_pings)) * 100.0
            self.batch_stability_score = round(stability, 3)
        else:
            self.batch_stability_score = 100.0

def send_anomaly_alert(bmr_id, temperature):
    """Sends an automated email alert safely without breaking the main execution pipeline."""
    qa_email = "admin@example.com" 
    subject = f"CRITICAL: Temperature Anomaly Detected on BMR {bmr_id}"
    
    message = f"""
    <h3>Production Threshold Breach Alert</h3>
    <p>An automated IoT telemetry sensor has flagged a critical process deviation.</p>
    <ul>
        <li><strong>Batch Record ID:</strong> {bmr_id}</li>
        <li><strong>Logged Temperature:</strong> <span style="color: red; font-weight: bold;">{temperature}°C</span></li>
        <li><strong>Status:</strong> Defect logged to the database ledger automatically.</li>
    </ul>
    <p>Please check the administrative dashboard immediately to verify batch integrity.</p>
    """
    
    try:
        frappe.sendmail(
            recipients=[qa_email],
            subject=subject,
            message=message
        )
    except frappe.OutgoingEmailError:
        frappe.log_error(
            title="SmartBMR Mail System Alert Skipped",
            message=f"Email alert triggered for BMR {bmr_id} ({temperature}°C), but default outgoing email account is not set up in the desk."
        )


@frappe.whitelist(allow_guest=True)
def log_machine_temperature(bmr_id, temp_reading):
    doc = frappe.get_doc("Batch Manufacturing Record", bmr_id)
    
    if doc.workflow_state != "In Production":
        frappe.throw("Machine rejected: BMR is not In Production.")
        
    current_temp = float(temp_reading)
    MIN_SAFE_TEMP = 36.0
    MAX_SAFE_TEMP = 39.0
    
    log_tank = frappe.get_doc({
        "doctype": "IoT Temperature Log",
        "batch_record_id": bmr_id,
        "temperature": current_temp,
        "timestamp": frappe.utils.now_datetime()
    })
    log_tank.insert(ignore_permissions=True)
    frappe.db.commit() 
    
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
        
        if not was_last_anomaly:
            send_anomaly_alert(bmr_id, current_temp)
        
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
        
        doc.calculate_quality_metrics()
        
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        return {"status": "logged", "message": f"Raw log captured & State tracked: {log_step} at {current_temp}°C"}
        
    return {"status": "ignored", "message": f"Raw log captured & Stable condition continues. Process log suppressed."}