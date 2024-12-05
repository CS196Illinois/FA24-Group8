from flask import Flask, jsonify
from webscraper import scrape_and_store

# Initialize Flask app
app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)
