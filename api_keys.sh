#!/bin/bash

read -p "Google API key: " google_api_key
read -p "Imgur API key: " imgur_api_key

echo {\"GOOGLE_API_KEY\": \"$google_api_key\", \"IMGUR_API_KEY\": \"$imgur_api_key\"} > earthpronapp/config.json

printf "config.json created\n"

read -p "Alchemy API key: " alchemy_api_key

python earthpronapp/alchemyapi.py $alchemy_api_key
mv api_key.txt earthpronapp/api_key.txt
