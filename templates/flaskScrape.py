from flask import Flask, jsonify, render_template
from flask_cors import CORS
from webscraper import scrape_and_store

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

@app.route('/')
def home():
    return "CORS is enabled for all origins!"

@app.route('/scrape', methods=['POST'])
def scrape_data():
    try:
        # Call the scrape_and_store function to get the DataFrame
        df = scrape_and_store()
        
        # Convert the DataFrame to JSON (records format for a list of dictionaries)
        result = df.to_json(orient="records")
        
        # Return a successful response with the data
        return jsonify({"message": "Data scraped successfully.", "data": result}), 200
    except Exception as e:
        # Handle errors and return error details
        return jsonify({"error": str(e)}), 500
    
@app.route('/research')
def research_page():
    return render_template('research.html')

if __name__ == "__main__":
    app.run(debug=True)
