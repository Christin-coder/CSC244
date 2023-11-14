import ast
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
    logger.debug(f"Columns are : {columns}")
    cursor.execute(f"SELECT * FROM imdb.{table_name} WHERE {' AND '.join(f'{column} IS NOT NULL' for column in columns)} LIMIT 1")
    rowValues = cursor.fetchall()
    for i in rowValues[0]:
        if i != '':
            column_data_types.append(type(i))
            logger.debug(f"Data type is {type(i)}")
        else:
            column_data_types.append('')
            
    db_connection.close()
    return column_data_types

def convert_to_data_types(column_values, column_data_types):
    converted_values = []
    logger.debug(f"Values are {column_values}")
    for value, data_type in zip(column_values, column_data_types):
        logger.debug(f"Values is {value} and data type is {data_type}")
        if data_type is str and value != '' and value != None:
            converted_values.append(str(value))
        elif data_type is int and value != '' and value != None:
            converted_values.append(int(value))
        elif data_type is float and value != '' and value != None:
            converted_values.append(float(value))
        elif data_type is bool and value != '' and value != None:
            converted_values.append(bool(value))
        elif value is '' and value != None:
            converted_values.append('')

    return converted_values

def check_emptyInput(column, value):
    if value == '':
        return False
    else:
        return True
    
def build_search_query(table_name, columns, search_values, column_data_types):
    conditions = []

    for column, value, data_type in zip(columns, search_values, column_data_types):
        flag = check_emptyInput(column, value)
        if flag:
            if data_type is str:
                conditions.append(f"{column} = '{value}'")
            elif data_type is int:
                conditions.append(f"{column} = {value}")
            elif data_type is float:
                conditions.append(f"{column} = {value}")
            elif data_type is bool:
                conditions.append(f"{column} = {value}")

    where_clause = " AND ".join(conditions)
    return where_clause


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
    if(request.args.get('update_values')):
        logger.debug("update section entered")
        table_name = request.args["table_name"]
        logger.debug(f"Table name is {table_name}")
        updateValue = request.args.get('update_values')
        logger.debug(f"Update Where clause values = {updateValue}")
        updateValue = ast.literal_eval(updateValue)
        column_data_types = get_column_data_types(table_name)
        converted_values = convert_to_data_types(updateValue, column_data_types)
        logger.debug(f"Search query values = {converted_values}")
        
        db_connection = init_db()
        cursor = db_connection.cursor()
        cursor.execute(f"SELECT * FROM imdb.{table_name} FETCH FIRST 1 ROWS ONLY")
        columns = [column[0] for column in cursor.description]
        logger.debug(f"Column names {columns}")
        if table_name in ("DIRECTORS", "ACTORS", "MOVIES"):
            query = f"SELECT * FROM imdb.{table_name} WHERE ID = {converted_values[0]}"
            logger.debug(query)
        else:
            where_clause = build_search_query(table_name, columns, converted_values, column_data_types)
            query = f"SELECT * FROM imdb.{table_name} WHERE {where_clause}"
        cursor.execute(query)
        search_results = cursor.fetchall()
        logger.debug(f"Search results are {search_results}")
        db_connection.close()
        
        return render_template('updateTable.html', table_name=table_name, data=search_results, columns=columns)
    
    db_connection = init_db()
    cursor = db_connection.cursor()
    offset = (page_number - 1) * page_size

    table_name = request.args["table_name"]
    cursor.execute(f"SELECT * FROM imdb.{table_name} OFFSET {offset} FETCH FIRST {page_size} ROWS ONLY")
    all_rows = cursor.fetchall()

    columns = [column[0] for column in cursor.description]
    db_connection.close() 

    return render_template('view_table.html', table_name = table_name, data=all_rows, columns=columns, page=page_number)

@app.route('/update_rows', methods=['GET', 'POST'])
def update_rows():
    logger.debug("Entered update_rows section")
    table_name = request.args["table_name"]
    if table_name in ("DIRECTORS", "MOVIES", "ACTORS"):
        logger.debug(f"Table = {table_name}")
        previousValues = ast.literal_eval(request.args.get('data'))
        previousValues = previousValues[0]
        logger.debug(f"Previous Values = {previousValues}")
        update_values = request.form.getlist('newValueOfRow')
        logger.debug(f"New Row values = {update_values}")
        column_data_types = get_column_data_types(table_name)
        logger.debug(f"Data types are {column_data_types}")
        converted_values_prev = convert_to_data_types(previousValues, column_data_types)
        converted_values_new = convert_to_data_types(update_values, column_data_types)
        logger.debug(f"Converted previous values are {converted_values_prev}")
        logger.debug(f"Converted values are {converted_values_new}")
    
        db_connection = init_db()
        cursor = db_connection.cursor()
        cursor.execute(f"SELECT * FROM imdb.{table_name} FETCH FIRST 1 ROWS ONLY")
        columns = [column[0] for column in cursor.description]
        set_clause = build_search_query(table_name, columns, converted_values_new, column_data_types)
        logger.debug(f"UPDATE imdb.{table_name} SET {set_clause} WHERE ID = {converted_values_prev[0]}")
        query = f"UPDATE imdb.{table_name} SET {set_clause} WHERE ID = {converted_values_prev[0]}"
        cursor.execute(query)
        db_connection.commit()
        db_connection.close
    
    return redirect(url_for('view_table', table_name=table_name))
    

@app.route('/submit_rows', methods=['POST'])
def submit_rows():
    if request.method == 'POST':
        table_name = request.args["table_name"]
        column_values = request.form.getlist('column_values')
        
        db_connection = init_db()
        cursor = db_connection.cursor()
        cursor.execute(f"INSERT INTO imdb.{table_name} VALUES ({', '.join(['?']*len(column_values))})", column_values)
        db_connection.commit()
        db_connection.close()
        
    return redirect(url_for('view_table', table_name=table_name))
    
@app.route('/search_rows', methods=['GET','POST'])
def search_rows():
    if request.method == 'POST':
        table_name = request.args["table_name"]
        search_values = request.form.getlist('search_values')
        column_data_types = get_column_data_types(table_name)
        converted_values = convert_to_data_types(search_values, column_data_types)
        
        db_connection = init_db()
        cursor = db_connection.cursor()
        cursor.execute(f"SELECT * FROM imdb.{table_name} FETCH FIRST 1 ROWS ONLY")
        columns = [column[0] for column in cursor.description]
        where_clause = build_search_query(table_name, columns, converted_values, column_data_types)
        query = f"SELECT * FROM imdb.{table_name} WHERE {where_clause}"
        cursor.execute(query)
        search_results = cursor.fetchall()
        logger.debug(f"Search row results are {search_results}")
        db_connection.close()
        
    return render_template('search.html', table_name = table_name, data=search_results, columns=columns)


    
@app.route('/delete_rows', methods=['GET','POST'])
def deleteRow():
    if (request.form.get("rowValue")):
        logger.debug("delete section entered")
        table_name = request.args["table_name"]
        delete_values = ast.literal_eval(request.form.get('rowValue'))
        column_data_types = get_column_data_types(table_name)
        converted_values = convert_to_data_types(delete_values, column_data_types)
    
        db_connection = init_db()
        cursor = db_connection.cursor()
        cursor.execute(f"SELECT * FROM imdb.{table_name} FETCH FIRST 1 ROWS ONLY")
        columns = [column[0] for column in cursor.description]
        where_clause = build_search_query(table_name, columns, converted_values, column_data_types)
        logger.debug(f"Delete from {table_name} where {where_clause}")
        query = f"DELETE FROM imdb.{table_name} WHERE {where_clause}"
        cursor.execute(query)
        db_connection.commit()
        db_connection.close()
    
    return redirect(url_for('view_table', table_name=table_name))
    
if __name__ == '__main__':
    app.run(debug=True)