from flask import Flask, request, jsonify
import mysql.connector

# --- Configuration ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root', # Your MySQL Username
    'password': 'your_mysql_password', # Your MySQL Password
    'database': 'drone_pilot_db'
}

app = Flask(__name__)

# --- Database Connection and Query Logic ---

def create_db_connection():
    """Establishes and returns a MySQL database connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

@app.route('/submit', methods=['POST'])
def submit_application():
    """Receives form data, checks for unique email, and inserts into DB."""
    
    # 1. Connect to Database
    conn = create_db_connection()
    if conn is None:
        return jsonify({'success': False, 'message': 'Database connection failed.'}), 500

    cursor = conn.cursor()
    
    # Files are ignored here, focus on text fields
    data = request.form

    # 2. Extract and Validate Email (Case-insensitive unique check)
    email = data.get('email', '').strip().lower()
    if not email:
        conn.close()
        return jsonify({'success': False, 'message': 'Email is required.'}), 400

    try:
        # 3. Check for Unique Email (Primary Key Logic)
        check_sql = "SELECT email FROM applications WHERE email = %s"
        cursor.execute(check_sql, (email,))
        
        if cursor.fetchone():
            conn.close()
            return jsonify({'success': False, 'message': 'The email address provided is already registered.'}), 409 # 409 Conflict

        # 4. Prepare Data for Insertion
        insert_sql = """
        INSERT INTO applications (full_name, email, country_code, phone_number, living_eu_uk, hold_license, prior_experience, own_drone_radio, own_drone, willing_to_travel, self_sponsor_invest) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        insert_data = (
            data.get('full_name'), 
            email, 
            data.get('country_code'), 
            data.get('phone_number'), 
            data.get('living_eu_uk'), 
            data.get('hold_license'), 
            data.get('prior_experience', 'N/A'),
            data.get('own_drone_radio'),
            data.get('own_drone', 'N/A'),
            data.get('willing_to_travel'),
            data.get('self_sponsor_invest')
        )

        # 5. Execute Insertion
        cursor.execute(insert_sql, insert_data)
        conn.commit()

        return jsonify({'success': True, 'message': 'Application submitted successfully.'}), 200

    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Database error during insertion: {err}")
        return jsonify({'success': False, 'message': f'Database error: {err}'}), 500
        
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    # Run the application (you may need to specify host/port based on your setup)
    app.run(debug=True, port=5000)  