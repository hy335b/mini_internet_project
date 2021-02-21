#!/bin/bash

for (( counter=2001; counter<2015; counter++ ))
do
sudo firewall-cmd --add-port=$counter/tcp
done

for (( counter=2021; counter<2035; counter++ ))
do
sudo firewall-cmd --add-port=$counter/tcp
done

for (( counter=2041; counter<2055; counter++ ))
do
sudo firewall-cmd --add-port=$counter/tcp
done

for (( counter=2061; counter<2073; counter++ ))
do
sudo firewall-cmd --add-port=$counter/tcp
done

for (( counter=2081; counter<2093; counter++ ))
do
sudo firewall-cmd --add-port=$counter/tcp
done

for (( counter=2101; counter<2113; counter++ ))
do
sudo firewall-cmd --add-port=$counter/tcp
done

sudo firewall-cmd --add-port=2099/tcp

sudo firewall-cmd --add-port=5001/tcp
