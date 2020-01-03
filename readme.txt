MSU PMIIS

Requirements

-- python 3
   postgre sql
   gtk-runtime environment (for windows)

python pakages

--- django
    psycopg2
    waesyprint

=============   !!!!!!!!!!!!!!! ======================

the application may run on both 32 and 64 bit machines
for easier installation process, it is recommened to use ubuntu as the server's operating system

======================================================

for windows installation
    > download and install python 3
    > downlaod and install postgre sql

    > install gtk-runtime environment

        Note: installation of gtk-runtime environment many differ depending on the archetecture of the server computer, 32-bit computer has an available executeble installer while
        for 64-bit computers, installation is though MSYS

for ubuntu installation
    > install python3 ("apt install python3") and pip3 ( "apt install python3-pip3" )
    > install postgresql ("apt install postgresql postgresql-contrib")

for installation of python packages
    : to install package use "pip" for windows and "pip3" for python

    open the terminal or command promt and type the following command to install packages

    for Django:
        pip install django

    for PostgreSQL python connector

        pip install psycopg2

    for Weasyprint

        pip install weasyprint

        Note: before installing weasyprint, there are some things that must be done. please refer to
        --- ( weasyprint.readthedocs.io/en/stable/install.html ) ----
        for complete instructions regarding on installation of weasyprint

Setup the Database:
  using the command prompt/termeinal, run the setupdb.py
  use "python" on Windows and "python3" on Linux


After all this requirements were installed, you can now comfigure the app to start

first step in configuring the app is thought the following files
these files are responsible for datebase connection of the application
locate
      App_directory/Project_SMO_Inventory/Project_SMO_Inventory/src/connectdb.py
      on the values indicated set or change :

                uname = 'your postgres access username'
                password = 'your postgres access password'
                host = 'your db server ip address'
                dbname = 'your db name'

                for the database name, the database will be created if it doesnt curently exist

      App_directory/Project_SMO_Inventory/Project_SMO_Inventory/settings.py
      find the commented line "Configure database connection here"
      on the values indicated set or change :
               'NAME': 'your db name', ---- name indicated here must be the same with the indicated db name on connectdb.py file
               'USER': 'your postgres access username',
               'PASSWORD': 'your postgres access password',
               'HOST': 'your db server ip addres',



After configuring the db connectios

    you may now start the django server
    to start the server
        "python3" for ubuntu "python" for windows

        open the terminal or command prompt on this file's directory
        run the following commands:

        python manage.py makemigrations
        python manage.py migrate
        python manage.py runserver 0.0.0.0:8000 (the port number may differ depending on your desired port number)

You may access the app on address 127.0.0.1:8000 (or what port number you have set)





