import json
import csv
import math
import xml.etree.ElementTree as ET

with open('Police.csv', 'r') as police:
    lines_police = police.readlines()
    
police_table = list()

for line in lines_police:
    element = line.strip().split(",")
    police_table.append(element)

police_table[0][10] = "date_id" #date_fk  = date_id

for i in range(10):
    print(police_table[i])

#ASSIGNEMENT 1

#PARTECIPANT_ID
#GUN_ID
#GEO_ID

dict_part_id = {}
dict_gun_id = {}
dict_geo_id = {}
for i in range(len(police_table[0])):
    if "participant" in police_table[0][i]:
        dict_part_id[police_table[0][i]] = i
    if "gun" in police_table[0][i]:
        dict_gun_id[police_table[0][i]] = i
    if "latitude" in police_table[0][i] or "longitude" in police_table[0][i]:
        dict_geo_id[police_table[0][i]] = i

#Let's create the lists that will contain the various combinations for participant, gun, and
#geo, and let's insert the metadata we have collected in dictionaries into the first list
def table_creation (dict_id):
    id_table = list()
    metadata_id = list()
    for i in dict_id.keys():
        metadata_id.append(i)
    id_table.append(metadata_id)
    return id_table

part_id_table = table_creation(dict_part_id)
gun_id_table = table_creation(dict_gun_id)
geo_id_table = table_creation(dict_geo_id)

#"Let's manually add the metadata provided in the assignment
police_table[0].append("participant_id")
police_table[0].append("gun_id")
police_table[0].append("geo_id")


for i in range(1, len(police_table)):
    current_combo_part_id = []
    current_combo_gun_id = []
    current_combo_geo_id = []
    for j in range(len(police_table[i])):
        if j in dict_part_id.values():
            current_combo_part_id.append(police_table[i][j])
        elif j in dict_gun_id.values():
            current_combo_gun_id.append(police_table[i][j])
        elif j in dict_geo_id.values():
            current_combo_geo_id.append(police_table[i][j])


    if current_combo_part_id in part_id_table:
        police_table[i].append(part_id_table.index(current_combo_part_id)-1) #In the 'police_table' list that we are analyzing, let's add the geo_id as the last element.
    else:
        part_id_table.append(current_combo_part_id)
        police_table[i].append(part_id_table.index(current_combo_part_id)-1)

    if current_combo_gun_id in gun_id_table:
        police_table[i].append(gun_id_table.index(current_combo_gun_id)-1)
    else:
        gun_id_table.append(current_combo_gun_id)
        police_table[i].append(gun_id_table.index(current_combo_gun_id)-1)

    if current_combo_geo_id in geo_id_table:
        police_table[i].append(geo_id_table.index(current_combo_geo_id)-1)
    else:
        geo_id_table.append(current_combo_geo_id)
        police_table[i].append(geo_id_table.index(current_combo_geo_id)-1)

# RESULT FOR PARTICIPANT: A list of lists, where each inner list represents a different combination of participant
# values (a row from the table). Since it's a set built without repetitions, their position in the comprehensive
# list indicates their participant_id (the first inner list contains the metadata). In the 'gun_id_list', some values
# are 'unknown', but we will assign an ID to combinations that have 'unknown' values within their attributes.
# For example, if a combination only specifies the gun_type, then that's a combination we want to recognize among the others.

#Just to keep track of progress.
    if i % 5000 == 0:
        print(round((i / 170929) * 100, 2), "%")
    elif i == len(police_table)-1:
        print("100%")


#Added indices within the tables.
def add_idx(primary_key, id_table):
    for i in range(len(id_table)):
        if i == 0:
            id_table[i].insert(0,primary_key)
        else:
            id_table[i].insert(0,i-1)


add_idx("participant_id", part_id_table)
add_idx("gun_id", gun_id_table)
add_idx("geo_id", geo_id_table)

#ASSIGNEMENT 1 PUNTO 2

with open("dict_partecipant_age.json", "r") as part_age, open("dict_partecipant_status.json", 'r') as part_status, open("dict_partecipant_type.json", 'r') as part_type:
    age_dict = json.load(part_age)
    status_dict = json.load(part_status)
    type_dict = json.load(part_type)


# Check
print("Type: ", type(age_dict), "\nContent AGE (F1): ", age_dict, "\n")           #F1
print("Type: ", type(type_dict), "\nContent TYPE (F2): ", type_dict, "\n")        #F2
print("Type: ", type(status_dict), "\nContent STATUS (F3): ", status_dict, "\n")  #F3

#Let's calculate the crime gravity for each instance in the dataset and insert it at the end of each element in 'police_table'
police_table[0].append("crime_gravity")
for i in range(1, len(police_table)):
    crime_gravity = age_dict[str(police_table[i][1])] * type_dict[str(police_table[i][4])] * status_dict[str(police_table[i][3])] #Formula fornita dalla consegna
    police_table[i].append(crime_gravity)

# split the police data into the tables required by the assignment and create the corresponding CSV files

#CUSTODY.CSV

indx_custody = list()
for i in range(len(police_table[0])):
    if police_table[0][i] == "custody_id" or police_table[0][i] == "participant_id" or police_table[0][i] == "gun_id" or police_table[0][i] == "geo_id" or police_table[0][i] == "date_id" or police_table[0][i] == "crime_gravity" or police_table[0][i] == "incident_id":
        indx_custody.append(i)

print("indici_custody: ", indx_custody)

custody_id_table = list()
for i in range(len(police_table)):
    current_custody = []

    for j in range(len(police_table[i])):
        if j in indx_custody:
            current_custody.append(police_table[i][j])
    custody_id_table.append(current_custody)


def writer_on_csv (nome_file, table_to_write):
    with open(nome_file, mode='w', newline='') as current_file:
        writer = csv.writer(current_file, delimiter=',')
        writer.writerows(table_to_write)

writer_on_csv("Custody.csv", custody_id_table)

#PARTICIPANT.CSV

writer_on_csv("Participant.csv", part_id_table)

#GUN.CSV

writer_on_csv("Gun.csv", gun_id_table)

#GEOGRAPHY.CSV

# uscities.csv is a file containing the coordinates of approximately 30,000 American cities along with their related
# information, including latitude, longitude, and state affiliation.
# The file is located within the project folder, and further details about the file are provided in the report.
with open('uscities.csv', 'r') as uscities:
    lines_uscities = uscities.readlines()

uscities_list = list()
for line in lines_uscities:
    element = line.strip().split(",")
    uscities_list.append(element)


for i in range(len(uscities_list)):
    for j in range(len(uscities_list[i])):
        uscities_list[i][j] = uscities_list[i][j].strip('"')


dict_uscities = {}
for i in range(len(uscities_list[0])):
    if uscities_list[0][i] == "lat" or uscities_list[0][i] == "lng" or uscities_list[0][i] == "city" or uscities_list[0][i] == "state_name":
        dict_uscities[uscities_list[0][i]] = i
print("dict_uscities: ", dict_uscities)


geo_id_table[0].append("city")
geo_id_table[0].append("state_name")
for i in range(1, len(geo_id_table)):
    dist_min = float("inf")
    indice_dist_min = float("inf")
    for j in range(1, len(uscities_list)):
        try:
            attuale_dist = math.sqrt((float(geo_id_table[i][1]) - float(uscities_list[j][int(dict_uscities["lat"])]))**2 + (float(geo_id_table[i][2]) - float(uscities_list[j][int(dict_uscities["lng"])]))**2)
            if attuale_dist < dist_min:
                indice_dist_min = j
                dist_min = attuale_dist
        except:
            print("Something went wrong:    \nindice = ", j, "\nvalore: ", uscities_list[j][int(dict_uscities["lng"])])

    geo_id_table[i].append(uscities_list[indice_dist_min][dict_uscities["city"]])
    geo_id_table[i].append(uscities_list[indice_dist_min][dict_uscities["state_name"]])

    # check
    if i % 500 == 0:
        print("Current completion status geo_id:", round((i / len(geo_id_table)) * 100, 2), "%")
    elif i == len(police_table)-1:
        print("100%")

# Creation of geo.csv file
with open("Geography.csv", mode='w', newline='') as geo_file:
    writer = csv.writer(geo_file, delimiter=',')
    writer.writerows(geo_id_table)


#DATE.CSV

tree = ET.parse('dates.xml')
root = tree.getroot()

for row in root.findall('row'):
    for element in row:
        print(f"Tag: {element.tag}, Testo: {element.text}")
        for attributo, valore in element.attrib.items():
            print(f"Attributo: {attributo}, Valore: {valore}")


date_id_table = []
date_id_table.append(["date_id", "day", "month", "year"])

for row in root.findall('row'):
    date_pk = row.find('date_pk').text

    data = row.find('date').text
    anno, mese, giorno = data.split(' ')[0].split('-')

    lista_interna = [int(date_pk), int(giorno), int(mese), int(anno)]
    date_id_table.append(lista_interna)


for i in range(10):
    print(date_id_table[i])

with open("Date.csv", mode='w', newline='') as date_file:
    writer = csv.writer(date_file, delimiter=',')
    writer.writerows(date_id_table)


import pyodbc
import csv

#Connection parameters
server = 'N.A.'
database = 'Group_ID_4_DB'
username = 'Group_ID_4'
password = 'N.A.'

# Connection
connectionString = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password

#Loading the tables into the database
def data_upload(csv_file,table_name):
    cnxn = pyodbc.connect(connectionString)
    cursor = cnxn.cursor()
    with open (csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        insert_query = f"INSERT INTO (table_name) ({', '.join(header)}) VALUES ({', '.join(['?'] * len(header))})"
        for row in csv_reader:
            cursor.execute(insert_query, row)
        cnxn.commit()
        cnxn.close()

data_upload('Gun.csv', 'Gun')
data_upload('Date.csv', 'Date')
data_upload('Participant.csv', 'Participant')
data_upload('Geography.csv', 'Geography')
data_upload('Custody.csv', 'Custody')
