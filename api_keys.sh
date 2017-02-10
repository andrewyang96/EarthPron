#!/bin/bash

read -p "Google API key: " google_api_key
read -p "Imgur client ID: " imgur_client_id
read -p "Imgur client secret: " imgur_client_secret
read -p "Reddit client ID: " reddit_client_id
read -p "Reddit client secret: " reddit_client_secret

printf "{
    \"GOOGLE_API_KEY\": \"$google_api_key\",
    \"IMGUR_CLIENT_ID\": \"$imgur_client_id\",
    \"IMGUR_CLIENT_SECRET\": \"$imgur_client_secret\",
    \"REDDIT_CLIENT_ID\": \"$reddit_client_id\",
    \"REDDIT_CLIENT_SECRET\": \"$reddit_client_secret\"
}\n" > earthpronupdater/config.json

printf "config.json created\n"

read -p "Alchemy API key: " alchemy_api_key

python earthpronupdater/alchemyapi.py $alchemy_api_key
mv api_key.txt earthpronupdater/api_key.txt
