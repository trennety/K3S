# Import Flask modules
from flask import Flask, request, render_template
from flask_mysqldb import MySQL
import os

# Create an object named app
app = Flask(__name__)

# Configure mysql database
app.config['MYSQL_HOST'] = os.getenv('MYSQL_DATABASE_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DATABASE')
# app.config['MYSQL_PORT'] = 3306 # Uncomment if a specific port is needed

# Initialize MySQL
mysql = MySQL(app)

# Write a function named `find_persons`
def find_persons(keyword):
    # Create a new cursor
    cursor = mysql.connection.cursor()
    query = f"""
    SELECT * FROM phonebook WHERE name LIKE %s;
    """
    cursor.execute(query, [f"%{keyword.strip().lower()}%"])
    result = cursor.fetchall()
    persons = [{'id': row[0], 'name':row[1].strip().title(), 'number':row[2]}
               for row in result]
    cursor.close()
    if len(persons) == 0:
        persons = [{'name': 'No Result', 'number': 'No Result'}]
    return persons


# Write a function named `find_records` which finds phone records by keyword using `GET` and `POST` methods,
# using template files named `index.html` given under `templates` folder
# and assign to the static route of ('/')
@app.route('/', methods=['GET', 'POST'])
def find_records():
    if request.method == 'POST':
        keyword = request.form['username']
        persons = find_persons(keyword)
        return render_template('index.html', persons=persons, keyword=keyword, show_result=True, developer_name='SwitzerChees')
    else:
        return render_template('index.html', show_result=False, developer_name='SwitzerChees')


# Add a statement to run the Flask application which can be reached from any host on port 80.
if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=80)
