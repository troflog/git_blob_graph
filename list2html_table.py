def list_to_html_table(data, header_string):
    if not data or not all(isinstance(row, list) for row in data):
        raise ValueError("Input must be a non-empty 2D list.")

    html_table = "<table>\n"
    
    # Add the header row
    html_table += "  <tr>\n"
    html_table += f"    <th colspan='{len(data[0])}'>{header_string}</th>\n"
    html_table += "  </tr>\n"

    # Add the data rows
    for row in data:
        html_table += "  <tr>\n"
        for cell in row:
            html_table += f"    <td>{cell}</td>\n"
        html_table += "  </tr>\n"

    html_table += "</table>"
    return html_table

# Example usage:
data = [
    ["Name", "Age"],
    ["John", 25 ],
    ["Jane", 30],
    ["Bob", 22]
]

header_string = "Employee Information"
html_table = list_to_html_table(data, header_string)
print(html_table)
