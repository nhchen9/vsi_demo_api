#!/bin/bash

for i in {1..100}
do
    curl -X GET "http://127.0.0.1:8000/decrypt?command=AQICAHhOmVIiapsKsJ3v8MJ8YOJecymAtttFPxQnthhvMsfe3AGn%2Fhhsdh1%2BVaL5zhPLKoPnAAAAZjBkBgkqhkiG9w0BBwagVzBVAgEAMFAGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMic6HYHf3qDGi%2BGsvAgEQgCNUZxipcUxo%2Fc5tSS7LKydF5QG3QSw7NrlkmhV%2FbOLJbjZPoQ%3D%3D" -H  "accept: application/json"
done