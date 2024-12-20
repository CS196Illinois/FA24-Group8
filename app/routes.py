from flask import render_template, request, jsonify
from app import app
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
DATA_PATH = os.path.join(BASE_DIR, 'data', 'research_opportunities_full.csv')  
try:
    df = pd.read_csv(DATA_PATH)
    print("Data loaded successfully!")
except FileNotFoundError:
    print("Error: Data file not found at", DATA_PATH)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/filter', methods=['GET'])
def filter_opportunities():
    research_area = request.args.get('research_area')
    opportunity_timing = request.args.get('opportunity_timing')
    location = request.args.get('location')
    deadline_before = request.args.get('deadline_before')

    filtered_df = df.copy()
    if research_area:
        filtered_df = filtered_df[
            filtered_df['Research Area'].str.contains(research_area, case=False, na=False)
        ]
    if opportunity_timing:
        filtered_df = filtered_df[filtered_df['Opportunity Timing'].str.contains(opportunity_timing, case=False, na=False)]
    if location:
        filtered_df = filtered_df[filtered_df['Location'].str.contains(location, case=False, na=False)]
    if deadline_before:
        filtered_df['Deadline Date'] = pd.to_datetime(filtered_df['Deadline Date'], errors='coerce')
        filtered_df = filtered_df[filtered_df['Deadline Date'] <= pd.to_datetime(deadline_before)]

    filtered_df = filtered_df.fillna("")
    return jsonify(filtered_df.to_dict(orient='records'))

@app.route('/get-options', methods=['GET'])
def get_options():
    research_areas = df['Research Area'].dropna().str.split(", ").explode().str.strip().drop_duplicates().sort_values().tolist()
    opportunity_timings = df['Opportunity Timing'].dropna().str.split(", ").explode().str.strip().drop_duplicates().sort_values().tolist()

    return jsonify({
        'research_areas': research_areas,
        'opportunity_timings': opportunity_timings
    })