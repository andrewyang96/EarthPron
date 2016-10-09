#!/bin/bash

read -p "Google API key: " google_api_key
read -p "Imgur API key: " imgur_api_key

echo {\"GOOGLE_API_KEY\": \"$google_api_key\", \"IMGUR_API_KEY\": \"$imgur_api_key\"} > epapp/config.json

printf "config.json created\n"

read -p "Alchemy API key: " alchemy_api_key

python epapp/alchemyapi.py $alchemy_api_key
mv api_key.txt epapp/api_key.txt
