import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template, jsonify
from werkzeug.utils import secure_filename
from textextractor import Extractor
from bot import Chatbot
import pandas as pd
from bs4 import BeautifulSoup
import json
import requests
from concurrent.futures import ThreadPoolExecutor
import sys


BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
DATA_PATH = os.path.join(BASE_DIR, 'data', 'research_opportunities.csv')  

python_files_dir = os.path.join(BASE_DIR, 'python')
sys.path.append(python_files_dir)
import webscraper
import recommendation
 
global research_opps
UPLOAD_FOLDER = ''

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'

@app.route("/index.html")
def goto_index():
    return render_template("index.html")

@app.route("/")
def home():
    return redirect("/index.html")

@app.route('/recommendation.html') 
def go_to_recommendation(): 
    return render_template("recommendation.html") 

@app.route('/filter.html') 
def go_to_filter(): 
    return render_template("filter.html") 

@app.route("/resume_review_cold_email.html")
def goto_RRCE():
    return render_template("resume_review_cold_email.html")
    
@app.route('/search', methods = ['GET', 'POST'])
def search():
    query = request.args.get('query')

    # Perform search logic here (e.g., database query, filtering)
    results = []  # Placeholder for search results

    return render_template('search_results.html', query=query, results=results)


@app.route('/filter', methods=['GET'])
def filter_opportunities():
    global research_opps
    webscrape()
    research_area = request.args.get('research_area')
    opportunity_timing = request.args.get('opportunity_timing')
    deadline_before = request.args.get('deadline_before')

    filtered_df = research_opps.copy()
    if research_area:
        filtered_df = filtered_df[filtered_df['Research Area'].str.contains(research_area, case=False, na=False)]
    if opportunity_timing:
        filtered_df = filtered_df[filtered_df['Opportunity Timing'].str.contains(opportunity_timing, case=False, na=False)]
    if deadline_before:
        filtered_df['Before Date'] = pd.to_datetime(filtered_df['Deadline Date'], errors='coerce')
        filtered_df = filtered_df[filtered_df['Before Date'] <= pd.to_datetime(deadline_before)]
    return filtered_df.to_json(orient='records')

@app.route('/recommend_filter', methods=['GET'])
def recommend_opportunities_filter():
    global research_opps
    webscrape()
    researchInterest1 = request.args.get('researchInterest1')
    researchInterest2 = request.args.get('researchInterest2')
    researchInterest3 = request.args.get('researchInterest3')
    
    research_interests = [researchInterest1, researchInterest2, researchInterest3]
    columns = ["Title", "Description", "DetailURL", "Research Area", "Opportunity Timing", "Deadline Date"]
    recommended_df1 = pd.DataFrame(columns=columns)
    recommended_df2 = pd.DataFrame(columns=columns)
    recommended_df3 = pd.DataFrame(columns=columns)
    recommended_df = research_opps.copy()

    recommended_by_model = recommendation.recommend_RO(research_opps, research_interests)

    if researchInterest1:
        recommended_df1 = recommended_df[recommended_df['Description'].str.contains(researchInterest1, case=False, na=False)]
    if researchInterest2:
        recommended_df2 = recommended_df[recommended_df['Description'].str.contains(researchInterest2, case=False, na=False)]
    if researchInterest3:
        recommended_df3 = recommended_df[recommended_df['Description'].str.contains(researchInterest3, case=False, na=False)]
    if researchInterest1 or researchInterest2 or researchInterest3:
        recommended_df = pd.concat([recommended_df1, recommended_df2, recommended_df3, recommended_by_model])
    return recommended_df.to_json(orient='records')

@app.route('/recommend_ML', methods=['GET'])
def recommend_opportunities_ML():
    global research_opps
    webscrape()
    researchInterest1 = request.args.get('researchInterest1')
    researchInterest2 = request.args.get('researchInterest2')
    researchInterest3 = request.args.get('researchInterest3')
    
    columns = ["Title", "Description", "DetailURL", "Research Area", "Opportunity Timing", "Deadline Date"]
    recommended_df = research_opps.copy()
    recommended_by_model = recommendation.recommend_RO(research_opps, re)

    if researchInterest1 or researchInterest2 or researchInterest3:
        recommended_df = pd.merge(recommended_df, pd.merge(recommended_df2, recommended_df3, how = "outer", on=columns), how='outer', on=columns)
    
    return recommended_df.to_json(orient='records')

@app.route('/webscrape', methods=['GET'])
def webscrape():
    global research_opps
    research_opps_list = []
    for i in range(0, 9):  
        research_opps_list += webscraper.scrape_main_page(i)
    columns = ["Title", "Description", "DetailURL", "Research Area", "Opportunity Timing", "Deadline Date"]
    research_opps = pd.DataFrame(research_opps_list, columns=columns)

    for row in range(len(research_opps.index)):
        if (len(research_opps.at[row, "Deadline Date"].split(" ")) >= 2):
            research_opps.at[row, "Deadline Date"] = research_opps.at[row, "Deadline Date"].split(" ")[1]
    research_opps.insert(0, "Id", research_opps.index, False)



  
@app.route('/upload', methods=['POST']) 
def upload(): 
    if request.method == 'POST': 
  
        # Get the list of files from webpage 
        files = request.files.getlist("file") 
        job_desc = request.files.getlist("job_desc")
    
        files[0].save(os.path.join(app.config['UPLOAD_FOLDER'], files[0].filename))
        job_desc[0].save(os.path.join(app.config['UPLOAD_FOLDER'], job_desc[0].filename))

        # Iterate for each file in the files List, and Save them 
       
        return redirect(url_for('uploads', resumeName=files[0].filename, jobDesc=job_desc[0].filename))

    return render_template("index.html")

@app.route('/uploads/<resumeName>/<jobDesc>') 
def uploads(resumeName, jobDesc):
    resumePath = (str(UPLOAD_FOLDER) + "/" + resumeName)
    jobPath = (str(UPLOAD_FOLDER) + "/" + jobDesc)
    tester = Extractor(resumePath, jobPath)
    nlpBot = Chatbot()
    similarityReview = nlpBot.resumeReview(resumePath, jobPath, tester.calculate_similarity())

    return render_template("uploads.html", variable=similarityReview)

@app.route('/emails', methods=['POST'])
def email():
    
    if request.method == 'POST':

        type = request.form['type']
        
        lname = request.form['lname']
        collegeName = request.form['collegeName']
        major = request.form['major']
        profName = request.form['profName']

        return redirect(url_for('emails', type=type, lname=lname, collegeName=collegeName, major=major, profName=profName))

    return render_template("index.html")

@app.route('/emails/<type>/<lname>/<collegeName>/<major>/<profName>') 
def emails(type, lname, collegeName, major, profName):
    
    emailGen = Chatbot()
    responses = emailGen.emailGenerator(type, lname, collegeName, major, profName)

    return render_template("emails.html", variable=responses)

if __name__ == "__main__":

    app.debug = True
    app.run()