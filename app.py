from flask import Flask, render_template, request
import pynuodb
import logging
import re

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def init_db():
    connection = pynuodb.connect(database='test', host='nuoadmin1', user='dba', password='goalie')
    return connection

@app.route('/')
def display_tables():
    pattern = r'\b[A-Z_]+\b'
    db_connection = init_db()
   
    cursor = db_connection.cursor()
    cursor.execute("use hockey")
    cursor.execute("show tables")
       
    tables = cursor.fetchall()
    matches = re.findall(pattern, str(tables))
    tables = list(set(matches))
    db_connection.close() 

    return render_template('tables.html', tables=tables)

@app.route('/view_table', methods=['GET', 'POST'])
def view_table():
    db_connection = init_db()

    cursor = db_connection.cursor()
    cursor.execute(f"SELECT * from hockey.{request.args['table_name']}")

    rows = cursor.fetchall()

    columns = [column[0] for column in cursor.description]

    db_connection.close() 

    return render_template('view_table.html', data=rows, columns=columns)

if __name__ == '__main__':
    app.run(debug=True)