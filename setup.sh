#Test git pull Sep 12,2016
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
# 
# 

echo "\n"
echo "Updating all existing packages...\n"
sudo apt-get -y update
sudo apt-get -y upgrade


#sudo apt-get -t jessie-backports install gunicorn

echo "\n"

#sudo apt-get install vim




#echo "You'll be asked to enter a password for the database, don't forget it! \n"
#sudo apt-get install -y --force-yes mysql-server 
#sudo apt-get install -y --force-yes mysql-client
#sudo apt-get install -y --force-yes apache2
#sudo apt-get install -y --force-yes libapache2-mod-python
# Restart apache to make sure things work
#sudo apache2 -k restart

echo "\n"
echo "Installing some essential stuff...\n"
echo "Installing python essentials\n"
sudo apt-get install -y build-essential python-dev

sudo apt-get install -y git
sudo apt-get install -y lynx
sudo apt-get install -y supervisor


#sudo apt-get install -y python-pip
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
sudo rm -rf get-pip.py
sudo apt-get install -y openssh-server
#sudo apt-get install -y --force-yes python-mysqldb libmysqlclient-dev 

echo "Install Virtual Environment"
sudo pip install virtualenv
echo "\n"

#Create user/group
#homeauto_django
echo "Create User/Group for Locker project"
sudo mkdir /webapps
sudo mkdir /webapps/homelocker
sudo groupadd --system webapps
sudo useradd --system --gid webapps --shell /bin/bash --home /webapps/homelocker locker
sudo chown -R locker:users /webapps/homelocker
sudo chmod -R g+w /webapps/homelocker

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

echo "Now we're going to install django and any other packages\n"
#sudo pip install django
sudo pip install -r requirements.txt

echo "\n"
echo "Finally, lets make sure Django is installed properly - this will print the version number\n"
python djangotest.py

echo "\n"
echo "Done! Locker project is ready\n"
exit 0
