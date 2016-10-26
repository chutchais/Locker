echo "\n"
echo "Updating all existing packages...\n"
sudo apt-get -y update
sudo apt-get -y upgrade
echo "\n"

echo "Installing some essential stuff...\n"
echo "Installing python essentials\n"
sudo apt-get install -y build-essential python-dev
sudo apt-get install -y git
sudo apt-get install -y lynx
sudo apt-get install -y supervisor
sudo apt-get install vim


echo "Installing Django Library\n"
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
sudo rm -rf get-pip.py
sudo apt-get install -y openssh-server


echo "Install Virtual Environment"
sudo pip install virtualenv
echo "\n"

#Create user/group
#homeauto_django
echo "Create User/Group for Locker project"
sudo mkdir /webapps
sudo mkdir /webapps/homelocker
sudo mkdir /webapps/homelocker/logs
sudo groupadd --system webapps
sudo useradd --system --gid webapps --shell /bin/bash --home /webapps/homelocker locker
sudo chown -R locker:users /webapps/homelocker
sudo chmod -R g+w /webapps/homelocker
#change passwd
sudo passwd locker
#put new passwd.


echo "Create Virtual Host"
sudo su - locker
cd /webapps/homelocker
virtualenv .
source bin/activate
git clone https://github.com/chutchais/Locker.git
pip install -r Locker/requirements.txt

rm -rf Locker/locker/migration
cd Locker
python manage.py makemigrations locker
python manage.py migrate
python manage.py createsuperuser
#Put password

#Back to Root user.
su pi
sudo pip install setproctitle
sudo aptitude install supervisor
sudo aptitude install nginx

#Test nginx
sudo service nginx start
sudo service nginx stop
sudo service nginx restart

######Config Supervisor########
#chmod 777
chmod 777 /webapps/homelocker/Locker/gunicorn_start
#Copy lockerauto.conf to /etc/supervisor/conf.d/lockerauto.conf
cp /webapps/homelocker/Locker/lockerauto.conf /etc/supervisor/conf.d/lockerauto.conf
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl status



#Make media folder
sudo mkdir /var/www /var/www/static /var/www/media
sudo chown -R locker:users /var/www

#############Setup Web Static files
#move to  virtual locker
su - locker
source bin/activate
cd Locker
python manage.py collectstatic


#############Setup nginx
cd /etc/nginx/sites-available/
#sudo nano lockerauto
#copy from GitHub
cp /webapps/homelocker/Locker/lockerauto lockerauto
cd /etc/nginx/sites-enabled
sudo ln -s ../sites-available/lockerauto
sudo rm default
sudo service nginx restart


echo "Finish !!!!!!!! you can access to 127.0.0.1:8008"
exit 0
