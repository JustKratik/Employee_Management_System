import os
from flask import Flask, jsonify, request, send_file
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

app = Flask(__name__, static_folder="static")

# --- CONFIG ---
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
DEFAULT_SHEET_ID = "1lemebG36uQ9MlbKZC_O2H_ltJZZI8aXFlnWlMbD4MXA"
RANGE_NAME = "Admin_Sheet!A1:Z2000"


def get_google_creds():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            return None
    return creds


@app.route("/")
def index():
    return send_file("index.html")


@app.route("/api/employees")
def get_employees():
    print("\n--- NEW REQUEST RECEIVED ---")
    creds = get_google_creds()
    if not creds:
        return jsonify({"error": "Authentication failed"}), 500

    sheet_id = request.args.get('sheet', DEFAULT_SHEET_ID)

    service = build('sheets', 'v4', credentials=creds)
    result = service.spreadsheets().values().get(
        spreadsheetId=sheet_id,
        range=RANGE_NAME
    ).execute()

    values = result.get('values', [])
    if not values:
        return jsonify([])

    headers = values[0]
    print(f"✅ Found {len(values)} rows")
    print(f"👀 Headers: {headers}")

    data = []
    for row in values[1:]:
        row += [''] * (len(headers) - len(row))
        data.append(dict(zip(headers, row)))

    return jsonify(data)


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(debug=True, port=5000)
