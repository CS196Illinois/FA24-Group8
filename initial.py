import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
from textextractor import Extractor
from bot import Chatbot

UPLOAD_FOLDER = '/Users/sriramnatarajan/Documents/FA24-Group8/uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'

@app.route('/') 
def main(): 
    return render_template("index.html") 


  
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