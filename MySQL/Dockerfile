#Pull the official mysql image
FROM mysql:8.0

#Set the environment variables
ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=testdb


# Copy the init script into the magic directory of mysql image to run the script automatically
COPY ./MySQL/init-db.sql /docker-entrypoint-initdb.d/


#Expose the port
EXPOSE 3306