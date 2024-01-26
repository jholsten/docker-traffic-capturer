#!/bin/bash

# Usage: ./collect_to_file.sh -f $filename
while getopts ":f:" opt; do
  case $opt in
    f) filename="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    exit 1
    ;;
  esac

  case $OPTARG in
    -*) echo "Option $opt needs a valid argument"
    exit 1
    ;;
  esac
done

export API_PORT=$(cat API_PORT)
echo "Sending request to store data in file '$filename' to API on port $API_PORT..."
echo "Response: " $(curl -X POST http://localhost:$API_PORT/collect/file/$filename)
