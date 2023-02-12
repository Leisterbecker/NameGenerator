#!/bin/bash
trap "kill 0" EXIT
cd ./server
. venv/bin/activate
flask --app server run &
PID_SERVER=$!
echo "PID Server: "$PID_SERVER
cd ../client
npm run dev &
wait
echo "exit name generator"
exit 0