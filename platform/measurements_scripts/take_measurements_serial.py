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

    tier1_stubs = list(range(1, 102, 20)) + list(range(2, 103, 20)) + [13, 14, 33, 34, 53, 54, 71, 72, 91, 92, 111, 112]
    tier2 = list(range(3, 13, 1)) + list(range(23, 33, 1)) + list(range(43, 53, 1)) + list(range(63, 71, 1)) + list(range(83, 91, 1)) + list(range(103, 111, 1))

    routers_tier1_stubs=['LOND', 'ZURI']
    routers_tier2=['LOND','ZURI','PARI','GENE','NEWY','BOST','ATLA','MIAM']

    for group_id in tier1_stubs:
        for loc in routers_tier1_stubs:
            connect_and_collect(group_id,loc)

    for group_id in tier2:
        for loc in routers_tier2:
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
