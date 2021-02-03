import datetime
import time
import subprocess
import psycopg2
import psycopg2.extras
measurements_dict={}


def connect_and_collect(router_group, router_name):

    dest=str(router_group)+"_"+str(router_name)+"router"
    command = "sudo docker exec "+dest+" vtysh -c \"show ip bgp\""

    ip_bgp_routes = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    measurement_timestamp = "\nMeasurement Timestamp --> ****" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "****"
    measurements_dict[str(router_group)+'-'+router_name] = str(ip_bgp_routes.stdout.read()).replace("\\n", "\n").replace("\\r", "\r") + measurement_timestamp



def all_routers():

    all_groups=list(range(1, 41, 1))

    all_locations=['HOUS','NEWY','LOND','BARC','ABID','ATH','ROMA','TOKY']


    for group_id in all_groups:
        for loc in all_locations:
            connect_and_collect(group_id,loc)


def connection_create():
    try:
        connection = psycopg2.connect(user = "bgproutes_db_root",
                                  password = "pG@Sksn",
                                  host = "127.0.0.1",
                                  port = "5001",
                                  database = "bgproutes_db")
        cursor = connection.cursor()
        return connection, cursor

    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)




def main():
    print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    all_routers()
    connection, cursor = connection_create()
    # Print PostgreSQL Connection properties
    print ( connection.get_dsn_parameters(),"\n")

    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    query = ("INSERT INTO routes (router_id, data) VALUES (%s, %s) ON CONFLICT(router_id) DO UPDATE SET data=%s ")
    values = list()
    db_insertion_time = "\nDatabase Insertion Timestamp (Last Update) --> ****" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "****\n"
    for key in measurements_dict:
        entry = (key, measurements_dict[key] + db_insertion_time, measurements_dict[key] + db_insertion_time,)
        values.append(entry)

    psycopg2.extras.execute_batch(cursor, query, values)
    print("Data Inserted")
    connection.commit()
    cursor.close()
    connection.close()
    print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


main()
