from datetime import datetime

def generate_html_report(scan_results, file_name="network_scan_report.html"):
    with open(file_name, "w", encoding='utf-8') as report:
        report.write(f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Network Scan Report</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    padding: 20px;
                }}
                h1 {{
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
                tr:nth-child(even) {{
                    background-color: #f9f9f9;
                }}
                tr:hover {{
                    background-color: #f1f1f1;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Network Scan Report</h1>
                <p>Generated on {datetime.now()}</p>
                <table>
                    <tr>
                        <th>IP Address</th>
                        <th>Open Ports</th>
                        <th>Services</th>
                        <th>MAC Address</th>
                        <th>Vendor</th>
                    </tr>""")

        for result in scan_results.values():
            ip = result["ip"]
            open_ports = result["open_ports"]
            services = result["services"]
            mac_address = result["mac_address"]
            vendor = result["vendor"]

            report.write(f"""
                    <tr>
                        <td>{ip}</td>
                        <td>{', '.join(map(str, open_ports))}</td>
                        <td>{', '.join(services)}</td>
                        <td>{mac_address}</td>
                        <td>{vendor}</td>
                    </tr>""")

        report.write("""
                </table>
            </div>
        </body>
        </html>
        """)
    print(f"Report saved to {file_name}")
