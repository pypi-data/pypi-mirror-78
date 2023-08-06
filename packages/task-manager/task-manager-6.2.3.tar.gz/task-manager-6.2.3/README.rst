The TaskListManager keeps track of lists of tasks that users should support. It
has a REST interface to access tasks and update them.

Documentation
=============

The Task Manager is documented at https://idsp-task-manager.readthedocs.io/


Installation on a Debian or Ubuntu Server
=========================================

Prerequisites
-------------

::

   # apt-get install -y build-essential python-dev python-pip mercurial mysql-server libmysqlclient-dev nginx
   # pip install virtualenv
   # adduser taskman
   # su taskman
   (taskman)$ mkdir ~/taskmanager && cd ~/taskmanager
   (taskman)$ virtualenv --prompt="(taskman)" venv
   (taskman)$ ln -s venv/bin/activate
   (taskman)$ source activate
   (taskman)$ hg clone https://bitbucket.org/bigr_erasmusmc/taskmanager
   (taskman)$ cd taskmanager
   (taskman)$ pip install -e .


Mysql database initialization
-----------------------------

::

    # mysql -p  [use -p if you have set a root password, which you should done anyway]
    mysql> CREATE USER 'taskmanager'@'localhost' IDENTIFIED BY 'blaat123';
    mysql> CREATE DATABASE taskmanager;
    mysql> GRANT ALL ON taskmanager.* TO 'taskmanager'@'localhost';
    (taskman)$ python ./create_config.py -d taskmanager -u taskmanager -p blaat123
    (taskman)$ taskmanager-db-init [migrations should be implemented]




Mysql dummy data (optional)
---------------------------

::

    (taskman)$ taskmanager-data-init


Running a test instance of the taskmanger
-----------------------------------------

::

    (taskman)$ taskmanager-run



Deploy on a production server
-----------------------------

::

    (taskman)$ pip install -r requirements_production.txt

    # service nginx start
    # rm /etc/nginx/sites-enabled/default
    # cp resources/nginx/taskmanager /etc/nginx/sites-available/taskmanager
    # ln -s /etc/nginx/sites-available/taskmanager /etc/nginx/sites-enabled/taskmanager


Startup scripts
~~~~~~~~~~~~~~~

Find out which process management system you are using: ``# stat /proc/1/exe``. If this outputs something along the lines of '/lib/systemd/systemd' skip to the systemd version otherwise you probably are running on an upstart system. See [this StackExchange post](http://unix.stackexchange.com/questions/196166/how-to-find-out-if-a-system-uses-sysv-upstart-or-systemd-initsystem) for more details.
Below are configurations for the upstart and systemd provided. (Make sure you should only follow 1 of those).

systemd
*******

There is script that is called from the systemd unit in ``resources/systemd/taskmanager-run``. If you have changed the install location in the first steps please make sure to update this file accordingly.

::

    # cp resources/systemd/taskmanager.service /etc/systemd/system/taskmanager.service
    # systemctl enable taskmanager.service
    # systemctl start taskmanager
    # systemctl restart nginx
    
    
upstart
*******

If you have changed the install location in the first steps please make sure to update the upstart file accordingly.

::

    # cp resources/upstart/taskmanager.conf /etc/systemd/system/taskmanager.conf
    # initctl reload-configuration
    # service taskmanager start
    # service nginx restart


You can now reach the taskmanager on port 80 from your network.

Add authentication to the taskmanager (optional)
------------------------------------------------

You can add Basic Authentication to the taskmanager by creating credentials and uncommenting 2 lines from the provided nginx config

::

    # apt install apache2-utils
    # htpasswd -c /etc/nginx/.htpasswd username

Uncomment ``auth_basic ...`` and ``auth_basic_user_file ...`` in the nginx config (``/etc/nginx/sites-available/taskmanager``).

::

    # systemctl restart nginx


Add sentry.io to the taskmanager
--------------------------------

Install the dependencies in the taskmanager virtualenv:

::

    (taskman)$ pip install raven[flask]

Create a drop-in configuration for the systemd unit:

::

    # mkdir /etc/systemd/system/taskmanager.service.d
    # touch /etc/systemd/system/taskmanager.service.d/environment.conf
    # vim /etc/systemd/system/taskmanager.service.d/environment.conf

Add the following to the file and close it:

::

    [service]
    Environment="SENTRY_DSN=YOUR_SENTRY_DSN"

::

    # systemctl daemon-reload
    # systemctl restart taskmanager
