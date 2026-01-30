import re
import requests
from flask import Flask, request, jsonify
# python
import re
import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

API_KEY = "AIzaSyABdKbscWXikb6aO5iHDwNw1y_1L7yFs0A"
RANGE = "Admin_Sheet!A1:Z1000"

def get_sheet_id(sheet_input: str) -> str:
    """
    Accepts full Google Sheet URL OR raw Sheet ID
    """
    if "docs.google.com" in sheet_input:
        match = re.search(r"/d/([a-zA-Z0-9-_]+)", sheet_input)
        if not match:
            raise ValueError("Invalid Google Sheet URL")
        return match.group(1)
    return sheet_input

# serve the HTML file at the root URL
@app.route("/")
def index():
    # ensure `employee_system.html` is in the same directory as `main.py`
    return send_from_directory(".", "Employee_management_System.html")

@app.route("/api/employees")
def get_employees():
    sheet_input = request.args.get("sheet")  # URL or ID

    if not sheet_input:
        return jsonify({"error": "sheet parameter required"}), 400

    sheet_id = get_sheet_id(sheet_input)

    url = (
        f"https://sheets.googleapis.com/v4/spreadsheets/"
        f"{sheet_id}/values/{RANGE}?key={API_KEY}"
    )

    response = requests.get(url)
    response.raise_for_status()

    values = response.json().get("values", [])
    if not values:
        return jsonify([])

    headers = values[0]
    rows = values[1:]

    data = [dict(zip(headers, row)) for row in rows]
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
app = Flask(__name__)
API_KEY = "AIzaSyABdKbscWXikb6aO5iHDwNw1y_1L7yFs0A"
RANGE = "Admin_Sheet!A1:Z1000"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1lemebG36uQ9MlbKZC_O2H_ltJZZI8aXFlnWlMbD4MXA/edit?gid=0#gid=0"
def get_sheet_id(sheet_input: str) -> str:
    """
    Accepts full Google Sheet URL OR raw Sheet ID
    """
    if "docs.google.com" in sheet_input:
        match = re.search(r"/d/([a-zA-Z0-9-_]+)", sheet_input)
        if not match:
            raise ValueError("Invalid Google Sheet URL")
        return match.group(1)
    return sheet_input
@app.route("/api/employees")
def get_employees():
    sheet_input = request.args.get("sheet")  # URL or ID

    if not sheet_input:
        return jsonify({"error": "sheet parameter required"}), 400

    sheet_id = get_sheet_id(sheet_input)

    url = (
        f"https://sheets.googleapis.com/v4/spreadsheets/"
        f"{sheet_id}/values/{RANGE}?key={API_KEY}"
    )

    response = requests.get(url)
    response.raise_for_status()

    values = response.json()["values"]
    headers = values[0]
    rows = values[1:]

    data = [dict(zip(headers, row)) for row in rows]
    return jsonify(data)
if __name__ == "__main__":
    app.run(debug=True)
