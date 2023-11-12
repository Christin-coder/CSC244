from flask import Flask, jsonify, render_template, request, redirect, url_for
import pynuodb
import logging
import re

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def init_db():
    connection = pynuodb.connect(database='test', host='nuoadmin1', user='dba', password='goalie')
    return connection

def get_column_data_types(table_name):
    db_connection = init_db()
    column_data_types = []
    cursor = db_connection.cursor()
    cursor.execute(f"SELECT * FROM imdb.{table_name} FETCH FIRST 1 ROWS ONLY")
    columns = [column[0] for column in cursor.description]
    cursor.execute(f"SELECT * FROM imdb.{table_name} WHERE {' AND '.join(f'{column} IS NOT NULL' for column in columns)} LIMIT 1")
    rowValues = cursor.fetchall()
    for i in rowValues:
        column_data_types.append(type(i))

    db_connection.close()
    return column_data_types


def convert_to_data_types(column_values, column_data_types):
    converted_values = []
    for value, data_type in zip(column_values, column_data_types):
        if data_type in ('VARCHAR', 'CHAR'):
            converted_values.append(str(value))
        elif data_type in ('INTEGER', 'SMALLINT', 'BIGINT', 'DECIMAL', 'FLOAT', 'DOUBLE'):
            converted_values.append(int(value))
        elif data_type == 'BOOLEAN':
            converted_values.append(bool(value))

    return converted_values

@app.route('/')
def display_tables():
    pattern = r'\b[A-Z_]+\b'
    db_connection = init_db()
   
    cursor = db_connection.cursor()
    cursor.execute("use imdb")
    cursor.execute("show tables")
       
    tables = cursor.fetchall()
    matches = re.findall(pattern, str(tables))
    tables = list(set(matches))
    tables.remove("IMDB")
    db_connection.close() 

    return render_template('tables.html', tables=tables)

@app.route('/view_table', methods=['GET', 'POST'])
def view_table():
    page_number = int(request.args.get('page', 1))
    page_size = 15

    db_connection = init_db()

    cursor = db_connection.cursor()
    offset = (page_number - 1) * page_size

    table_name = request.args["table_name"]
    cursor.execute(f"SELECT * FROM imdb.{table_name} OFFSET {offset} FETCH FIRST {page_size} ROWS ONLY")
    all_rows = cursor.fetchall()

    columns = [column[0] for column in cursor.description]
    db_connection.close() 

    return render_template('view_table.html', table_name = table_name, data=all_rows, columns=columns, page=page_number)

@app.route('/submit_rows', methods=['POST'])
def submit_rows():
    if request.method == 'POST':
        table_name = request.args["table_name"]
        column_values = request.form.getlist('column_values')

        '''column_data_types = get_column_data_types(table_name)
        converted_values = convert_to_data_types(column_values, column_data_types)'''
        
        db_connection = init_db()
        cursor = db_connection.cursor()
        cursor.execute(f"INSERT INTO imdb.{table_name} VALUES ({', '.join(['?']*len(column_values))})", column_values)
        db_connection.commit()
        db_connection.close()
        
    return redirect(url_for('view_table', table_name=table_name))
    
    
if __name__ == '__main__':
    app.run(debug=True)