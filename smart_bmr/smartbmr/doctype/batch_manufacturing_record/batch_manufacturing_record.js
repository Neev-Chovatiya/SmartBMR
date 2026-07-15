// Copyright (c) 2026, Neev Chovatiya and contributors
// For license information, please see license.txt

frappe.ui.form.on('Batch Manufacturing Record', {
    refresh: function(frm) {
        let wrapper = frm.get_field('telemetry_dashboard').$wrapper;
        wrapper.empty();
        
        wrapper.append('<div id="chart-container" style="margin-bottom: 20px; padding: 10px; background: #fff; border-radius: 4px;"></div>');

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

            new frappe.Chart("#chart-container", {
                title: "Live Temperature Telemetry Profile (°C)",
                data: {
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
                },
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
        });
    }
});