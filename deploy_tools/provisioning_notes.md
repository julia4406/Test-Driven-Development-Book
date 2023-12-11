Provision work of a new site
============================
## Requirements
* nginx
* Python 3.10
* gunicorn
* virtualenv + pip
* Git

    For ex.in Ubuntu:
    sudo add-apt-repository ppa:fkrull/deadsnakes
    sudo apt-get install nginx git python310 python3.10-venv

##Configuration virtual knot Nginx:

* look nginx.template.conf
* replace SITENAME (for ex. superlists.my-domain.com)

##Systemd service:

* look gunicorn-systemd.template.service
* replace SITENAME (for ex. superlists.my-domain.com)

##Folders structure:
Users account should exist in /home/username

/home/username
|___ sites
    |___ SITENAME
        |--- database
        |--- source
        |--- static
        |___ virtualenv

