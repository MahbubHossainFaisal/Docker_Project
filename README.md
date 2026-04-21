# Docker Project

# 1. Initial MySQL image build attempts (Troubleshooting paths/commands)
docker build -t project_mysql_image .
docker build ./MySQL -t project_mysql_container .
docker build ./MySQL -t project_mysql_container .
docker build -f ./MySQL/Dockerfile -t project_mysql_container .

# 2. Initial MySQL container run attempt (Failed due to PostgreSQL syntax)
docker run -p 3306:3306 --name project_mysql_container project_mysql_image

# 3. Initial Flask image build attempts
docker build -t project_flask_image .
cd Flask_App
docker build -t project_flask_image .

# 4. Creating the network (after db_connection_failed error)
docker network create my_project_network

# 5. Cleaning up existing/failed containers
docker rm -f project_mysql_container
docker rm -f project_flask_container

# 6. Running both containers properly on the new network
docker run -d -p 3306:3306 --name project_mysql_container --network my_project_network project_mysql_image
docker run -d -p 8000:8000 --name project_flask_cont ainer --network my_project_network project_flask_image

# 7. Testing the API endpoint (Troubleshooting PowerShell syntax)
curl.exe -X POST http://127.0.0.1:8000/api/data -H "Content-Type: application/json" -d "{\"user_id\": 2, \"value\": 29.5}"
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/data" -Method Post -Headers @{"Content-Type"="application/json"} -Body '{"user_id": 2, "value": 29.5}'

# 8. Pushing Phase 2 to GitHub
git add .
git commit -m "phase 2 of the assignment completed"
git push origin main

# 9. Interacting with the database via Compose
docker compose exec mysql mysql -u root -proot testdb -e "INSERT INTO ingestion_data(id,user_id,value,source) VALUES (100,100,'xyz','dummy');"
docker compose exec mysql mysql -u root -proot testdb -e "INSERT INTO ingested_data(id,user_id,value,source) VALUES (100,100,'xyz','dummy');"
docker compose exec mysql mysql -u root -proot testdb -e "INSERT INTO ingested_data(id,user_id,value,source) VALUES (100,100,2.32,'dummy');"
docker compose exec mysql mysql -u root -proot testdb -e "SELECT * FROM ingested_data;"
docker compose down
