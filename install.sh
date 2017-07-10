#! /bin/bash
#####################################################################
#
# to install or update:
# curl --silent https://raw.githubusercontent.com/DexterInd/DI_Sensors/master/install.sh | bash
#
#####################################################################

PIHOME=/home/pi
DEXTER=Dexter
DI_SENSORS=DI_Sensors

pushd $PIHOME > /dev/null
result=${PWD##*/} 
# check if ~/Dexter exists, if not create it
if [ ! -d $DEXTER ] ; then
    mkdir $DEXTER
fi
# go into $DEXTER
cd $DEXTER


# check if /home/pi/Dexter/DI_SENSORS exists
# if not, clone the folder
# if yes, refresh the folder
if [ ! -d $DI_SENSORS ] ; then
    # clone the folder
    sudo git clone --quiet https://github.com/DexterInd/DI_Sensors.git
    cd $DI_SENSORS
else
    cd $DI_SENSORS
    sudo git pull --quiet
fi


# install the python driver modules
cd Python
sudo python setup.py install
sudo python3 setup.py install

# python install cleanup
sudo rm -rf build
sudo rm -rf DI_Sensors.egg-info
sudo rm -rf dist

popd > /dev/null
