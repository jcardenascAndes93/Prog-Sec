# Flask Template with MySQL, PyTest and Docker


This project consist of two containers:
* `sc_blog_g0`: a flask blog app built from a python docker image.
* `mysql_sc_g0`: a mysql server instance.

`sc_blog_g0` allows hot reloading from the host repository folder.

## Prerequisites
* Install Docker CE and `docker-compose`.
* (Optional) [Manage Docker as a non-root user](https://docs.docker.com/engine/install/linux-postinstall/).

## Running the app
1. Create the two containers from the root directory (builds a docker image by performing every step in the Dockerfile):
    ~~~~
    > docker-compose up 
    ~~~~

2. Initialize the database in a different terminal:
    ~~~~
    > docker exec sc_blog_g0 flask init-db
    ~~~~
   
3. Compile C++ file to validate unique blog titles
    ~~~~
    > docker exec sc_blog_g0 g++ -o sc_blog/check_title_binary -I/usr/include/mysqlcppconn -L/usr/lib/mysqlcppconn sc_blog/check_title.cpp -lmysqlcppconn
    ~~~~

4. Go to web page:

    [http://localhost:5000](http://localhost:5000)

5. When done with the web app, remove the docker containers without losing the db data (which is saved in mysql_data 
   directory).
   ~~~~
    > docker-compose down
    ~~~~


## Testing the app
1. Get an interactive console inside the `sc_blog_g0` container:
    ~~~~
    > docker exec -it sc_blog_g0 bash
    ~~~~
2. Install the app as a python package inside the container:
    ~~~~
    > pip install -e .
    ~~~~
3. Run the tests:
    ~~~~
    > pytest -v --timeout=5
    ~~~~
4. Run tests to generate coverage report:
    ~~~~
    > coverage run -m pytest
    ~~~~
5. Check coverage report:
    ~~~~
    > coverage report
    ~~~~
   Or get a full html report and open it from the host in app/htmlcov/index.html:
    ~~~~
    > coverage html
    ~~~~
 

### Docker Compose:
https://docs.docker.com/compose/

### Docker Cheat Sheet:
http://dockerlabs.collabnix.com/docker/cheatsheet/
