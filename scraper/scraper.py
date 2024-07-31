import requests
from bs4 import BeautifulSoup
import csv

# Definir la URL de la página web
url = 'https://www.soccerstats.com/homeaway.asp?league=ecuador'

# Realizar una solicitud GET a la URL
response = requests.get(url)
response.raise_for_status()

# Procesar el contenido HTML usando BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Encontrar todas las tablas relevantes
tables = soup.find_all('table', {'id': 'btable'})

# Función para extraer datos de una tabla y eliminar la primera columna si es necesario
def extract_table_data(table, expected_headers, remove_first_column=False):
    rows = table.find_all('tr')[1:]  # Omitir la primera fila que contiene los encabezados originales
    data = []

    for row in rows:
        cells = row.find_all('td')
        if remove_first_column:
            cells = cells[1:]  # Omitir la primera columna que es el ID
        if len(cells) == len(expected_headers):
            row_data = {expected_headers[i]: cells[i].text.strip() for i in range(len(cells))}
            data.append(row_data)
    
    return data

# Función específica para extraer datos de tablas adicionales
def extract_additional_table_data(table, expected_headers, skip_rows=2, remove_first_column=False):
    rows = table.find_all('tr')[skip_rows:]  # Omitir las primeras filas que contienen los encabezados originales
    data = []

    for row in rows:
        cells = row.find_all('td')
        if remove_first_column:
            cells = cells[1:]  # Omitir la primera columna que es el ID
        if len(cells) > 1:
            row_data = {}
            cell_index = 0
            for header in expected_headers:
                # Saltar celdas con &nbsp;
                while cell_index < len(cells) and cells[cell_index].text.strip() in {'\xa0', ''}:
                    cell_index += 1
                if cell_index < len(cells):
                    row_data[header] = cells[cell_index].text.strip()
                    cell_index += 1
                else:
                    row_data[header] = ''
            data.append(row_data)

    return data

# Encabezados esperados para cada tabla
home_headers = ['Team', 'GP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']
away_headers = ['Team', 'GP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']
relative_performance_headers = ['Team', 'GPh', 'GPa', 'Pts', 'PPG Home', 'PPG Away', 'PPG Difference']
points_goal_distribution_headers = ['Team', 'GP', 'PHome', 'PAway', 'GHome', 'GAway', 'GCHome', 'GCAway']

# Extraer datos de las tablas Home y Away
home_data = extract_table_data(tables[0], home_headers, remove_first_column=True)
away_data = extract_table_data(tables[1], away_headers, remove_first_column=True)

# Identificar las tablas adicionales
relative_performance_table = tables[1].find_next('table', {'id': 'btable'})
points_goal_distribution_table = relative_performance_table.find_next('table', {'id': 'btable'})

# Extraer datos de las tablas adicionales
relative_performance_data = extract_additional_table_data(relative_performance_table, relative_performance_headers, skip_rows=2, remove_first_column=True)
points_goal_distribution_data = extract_additional_table_data(points_goal_distribution_table, points_goal_distribution_headers, skip_rows=2, remove_first_column=True)

# Función para guardar datos en archivos CSV
def save_to_csv(data, filename):
    if data:
        with open(filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

# Guardar los datos en archivos CSV
save_to_csv(home_data, 'home_table_data.csv')
save_to_csv(away_data, 'away_table_data.csv')
save_to_csv(relative_performance_data, 'relative_performance_data.csv')
save_to_csv(points_goal_distribution_data, 'points_goal_distribution_data.csv')