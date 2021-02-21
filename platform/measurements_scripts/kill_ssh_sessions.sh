#!/bin/bash

sudo kill -9 $(ps aux | grep '.*groups/id_rsa.*' | awk '{print $2}')
