from flask import Flask, request, jsonify
import pymysql
from webscraper import scrape_and_store

# Initialize Flask app
app = Flask(__name__)

# Database connection setup
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='your_username',
        password='your_password',
        db='profileData',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# Route for saving user profile
@app.route('/save-profile', methods=['POST'])
def save_profile():
    data = request.get_json()

    username = data['username']
    password = data['password']  # Make sure to hash this before saving
    email = data['email']
    major = data.get('major', None)

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO users (username, password, email, major)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (username, password, email, major))
        connection.commit()
        return jsonify({'message': 'Profile saved successfully!'}), 200

    except pymysql.MySQLError as e:
        print(e)
        return jsonify({'error': 'Failed to save profile'}), 500

    finally:
        connection.close()

# Route for scraping data
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
