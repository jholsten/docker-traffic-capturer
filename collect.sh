#!/bin/bash

curl -X GET --silent http://localhost:$(cat API_PORT)/collect
