// Copyright (c) 2026, Neev Chovatiya and contributors
// For license information, please see license.txt

frappe.ui.form.on('Batch Manufacturing Record', {
    refresh: function(frm) {
        let wrapper = frm.get_field('telemetry_dashboard').$wrapper;
        wrapper.empty();
        
        wrapper.append('<div id="chart-container" style="margin-bottom: 20px; padding: 10px; background: #fff; border-radius: 4px;"></div>');

        let chart = null;

        function render_live_telemetry() {
            if (!document.getElementById('chart-container')) {
                clearInterval(frm.telemetry_polling_interval);
                return;
            }

            frappe.db.get_list('IoT Temperature Log', {
                filters: { 'batch_record_id': frm.doc.name },
                fields: ['temperature', 'timestamp'],
                order_by: 'timestamp asc',
                limit: 50
            }).then(records => {
                let labels = [];
                let data_points = [];

                if (records && records.length > 0) {
                    records.forEach((row, idx) => {
                        labels.push(`Pt ${idx + 1}`);
                        data_points.push(row.temperature || 0);
                    });
                } else {
                    labels = ["No Data"];
                    data_points = [0];
                }

                let chart_data = {
                    labels: labels,
                    datasets: [
                        {
                            name: "Machine Temperature",
                            chartType: "line",
                            values: data_points
                        }
                    ],
                    yMarkers: [
                        { label: "Max Limit (39.0°C)", value: 39.0, options: { stroke: "#e74c3c", lineType: "dashed" } },
                        { label: "Min Limit (36.0°C)", value: 36.0, options: { stroke: "#e74c3c", lineType: "dashed" } }
                    ]
                };

                if (!chart) {
                    chart = new frappe.Chart("#chart-container", {
                        title: "Live Temperature Telemetry Profile (°C)",
                        data: chart_data,
                        type: 'line', 
                        height: 250,
                        colors: ['#3498db'], 
                        lineOptions: {
                            regionFill: 1,
                            splines: 0 
                        },
                        axisOptions: {
                            xIsSeries: 1
                        }
                    });
                } else {
                    chart.update(chart_data);
                }
            });
        }
        render_live_telemetry();

        if (frm.telemetry_polling_interval) {
            clearInterval(frm.telemetry_polling_interval);
        }
        
        if (frm.doc.workflow_state === "In Production") {
            frm.telemetry_polling_interval = setInterval(render_live_telemetry, 5000);
        }
    },
    
    before_unload: function(frm) {
        if (frm.telemetry_polling_interval) {
            clearInterval(frm.telemetry_polling_interval);
        }
    },

    before_workflow_action: function(frm) {
        if (frm.selected_workflow_action === "Approve & Close Batch") {
            
            let has_anomaly = false;
            
            if (frm.doc.process_log && frm.doc.process_log.length > 0) {
                frm.doc.process_log.forEach(row => {
                    if (row.step_number === "ANOMALY" || String(row.step_number) === "0" || row.step_number === 0) {
                        has_anomaly = true;
                    }
                });
            }

            if (has_anomaly && !frm.doc.supervisor_investigation_remarks) {
                frappe.validated = false; 
                
                frappe.msgprint({
                    title: __('Quality Assurance Block'),
                    indicator: 'red',
                    message: __('This batch contains temperature anomalies. You <b>must</b> fill out the <strong>Supervisor Investigation Remarks</strong> section at the bottom before this batch can be approved.')
                });
                
                return false;
            }
        }
    }
})