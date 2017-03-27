# Log Online Query

Query the online service log

* Function realization:

Through the page fill in the query server's IP address and query file path, you can check the online server file content

* Implement prerequisites

1. The query server has the authority to log in to the server without password
2. The query server has permission to view the server file being queried

* Configuration instructions

1. The data related to the query server is defined in the configuration file
2. If the login server is not related to the information can be unified definition, you can call each pass to achieve their own, Query the main.py file 38, line 39.
