// Compile with:
// g++ -o check_title_binary -I/usr/include/mysqlcppconn -L/usr/lib/mysqlcppconn check_title.cpp -lmysqlcppconn

/* Standard C++ includes */
#include <stdlib.h>
#include <iostream>
#include <string.h>
#include "mysql_connection.h"

#include <cppconn/driver.h>
#include <cppconn/exception.h>
#include <cppconn/resultset.h>
#include <cppconn/statement.h>

using namespace std;

bool valid_post_title(sql::Connection *con, char * title){
    sql::Statement *stmt;
    sql::ResultSet *res;
    bool isValid = true;
    char query[60];

    strcpy(query, "SELECT * FROM post WHERE title='");
    strcat(query, title);
    strcat(query, "'");

    stmt = con->createStatement();
    res = stmt->executeQuery(query);
    while (res->next()) {
        /* Access column data by alias or column name */
        // string title = res->getString("title");
        // int id = res->getInt("id");
        // string id_as_string = res->getString("id");
        isValid = false;
        break;
    }
    delete res;
    delete stmt;
    return isValid;
}

int main(int argc, char *argv[]){

    if (argc < 2) {
		cout << "# ERR: Empty query" << endl;
		return EXIT_FAILURE;
	}

    try {
        sql::Driver *driver;
        sql::Connection *con;
        
        /* Create a connection */
        sql::ConnectOptionsMap connection_properties;
        connection_properties["hostName"]=sql::SQLString("tcp://db:3306");
        connection_properties["userName"]=sql::SQLString("root");
        connection_properties["password"]=sql::SQLString("myrootpass");
        connection_properties["CLIENT_MULTI_STATEMENTS"]=(true);
        driver = get_driver_instance();
        con = driver->connect(connection_properties);

        /* Connect to the MySQL database */
        con->setSchema("mydb");

        char *title = argv[1];
        bool isValid = valid_post_title(con, title);
        if(isValid){
            cout << "true" << endl;
        } else {
            cout << "false" << endl;
        }

        delete con;

    } catch (sql::SQLException &e) {
        cout << "# ERR: SQLException in " << __FILE__;
        cout << "(" << __FUNCTION__ << ") on line " << __LINE__ << endl;
        cout << "# ERR: " << e.what();
        cout << " (MySQL error code: " << e.getErrorCode();
        cout << ", SQLState: " << e.getSQLState() << " )" << endl;
    }

    return EXIT_SUCCESS;
}