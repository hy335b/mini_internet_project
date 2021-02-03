from threading import Thread
import time
import subprocess
import psycopg2
import psycopg2.extras
measurements_dict={}


def connect_and_collect(router_group, router_name):

    print(router_group)
    print(router_name)

    dest=str(router_group)+"_"+str(router_name)+"router"
    command = "sudo docker exec "+dest+" vtysh -c \"show ip bgp\""

    ip_bgp_routes = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

    measurements_dict[str(router_group)+'-'+router_name] = str(ip_bgp_routes.stdout.read()).replace("\\n", "\n").replace("\\r", "\r")
    print(ip_bgp_routes)
    return ip_bgp_routes



def all_routers():

    all_groups=list(range(1, 41, 1))

    all_locations=['HOUS','NEWY','LOND','BARC','ABID','ATH','ROMA','TOKY']


    thread_list=[]

    id_to_key={}


    p=0

    for group_id in all_groups:
        for loc in all_locations:
            p=p+1
            t=Thread(target=connect_and_collect,args=(group_id,loc))
            measure_key=str(group_id)+'-'+loc
            id_to_key[p]=measure_key
            thread_list.append(t)


    for t in thread_list:
         cur_thread=t
         cur_thread.start()
         cur_thread.join()


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
    all_routers()
    connection, cursor = connection_create()
    # Print PostgreSQL Connection properties
    print ( connection.get_dsn_parameters(),"\n")

    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    query = ("INSERT INTO routes (router_id, data) VALUES (%s, %s) ON CONFLICT(router_id) DO UPDATE SET data=%s ")
    values = list()
    for key in measurements_dict:
        entry = (key, measurements_dict[key], measurements_dict[key],)
        values.append(entry)

    psycopg2.extras.execute_batch(cursor, query, values)
    print("Data Inserted")
    connection.commit()
    cursor.close()
    connection.close()


while(True):
    main()
    time.sleep(60)
