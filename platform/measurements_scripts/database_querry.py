import sys
import psycopg2
import datetime

def connection_create():
    try:
        connection = psycopg2.connect(user = "bgproutes_db_student",
                                  password = "hy335b_rocks",
                                  host = "147.52.203.13",
                                  port = "5001",
                                  database = "bgproutes_db")
        cursor = connection.cursor()
        return connection, cursor

    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)

def get_measurements(list_of_routers):
    for i in list_of_routers:
        connection, cursor = connection_create()
        query = "SELECT * FROM routes WHERE router_id = %s"
        cursor.execute(query,(i,))
        records = cursor.fetchall()

        for entry in records:
            print(entry[0])
            print(entry[1])


def fetch_results():
    print("\nDatabase query script, trigger timestamp --> ****" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "****\n")
    assert(len(sys.argv) == 2)
    if "," in sys.argv[1]:
        router_list=(sys.argv[1].rstrip()).split(",") # list of routers is denoted as Router1,Router2,Router3 .....
    else:
        router_list= [sys.argv[1].rstrip()]

    get_measurements(router_list)


fetch_results()

