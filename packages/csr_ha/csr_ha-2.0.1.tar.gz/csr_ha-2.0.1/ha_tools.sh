#!/usr/bin/env bash
# Install tools and programs to run the CSR in the cloud
#
# This script assumes the guestshell has been configured and enabled on
# the CSR.

# Set up a directory tree for HA
if [ ! -d $HOME/cloud ]; then
    sudo mkdir $HOME/cloud
    sudo chown guestshell $HOME/cloud
fi

if [ ! -d $HOME/cloud/HA ]; then
    sudo mkdir $HOME/cloud/HA
    sudo chown guestshell $HOME/cloud/HA
fi

if [ ! -d $HOME/cloud/HA/events ]; then
    sudo mkdir $HOME/cloud/HA/events
    sudo chown guestshell $HOME/cloud/HA/events
fi

ha_dir="$HOME/cloud/HA"

install_log="$ha_dir/install.log"

if [[ "$(python3 -V)" == *"Python 3"* ]]; then
    export PYTHON=$(which python3)
    export SITE=$($PYTHON -m site --user-site)
    if [[ ! -d "$SITE" ]]; then
        export PYTHON=$(which python)
        export SITE=$($PYTHON -m site --user-site)
    fi
else
    export PYTHON=$(which python)
    export SITE=$($PYTHON -m site --user-site)
fi

echo "Installing the CSR high availability package" >> $install_log

# Copy files from the package to guestshell

cp ha_tools.sh $ha_dir
cp debug_ha.sh $ha_dir
cp csr_ha.service $ha_dir
touch $ha_dir/csr_ha.log

#sudo mkdir $HOME/cloud/HA/client_api
#sudo chown guestshell $HOME/cloud/HA/client_api
cp csr_ha/client_api/revert_nodes.sh $ha_dir

#cd ../server
#sudo mkdir $HOME/cloud/HA/server
#sudo chown guestshell $HOME/cloud/HA/server
#cp * $HOME/cloud/HA/server

# Set up the path to python scripts
export HA_PY_PATH=$SITE/csr_ha/client_api:$SITE/csr_ha/server

echo 'alias create_node=create_node.py' >> $HOME/.bashrc
echo 'alias show_node=show_node.py' >> $HOME/.bashrc
echo 'alias node_event=node_event.py' >> $HOME/.bashrc
echo 'alias set_params=set_params.py' >> $HOME/.bashrc
echo 'alias clear_params=clear_params.py' >> $HOME/.bashrc
echo 'alias delete_node=delete_node.py' >> $HOME/.bashrc

#echo 'export PYTHONPATH='$PYTHONPATH':'$SITE'/csr_ha/client_api:'$SITE'/csr_ha/server' >> $HOME/.bashrc
echo 'export PATH='$HOME'/.local/bin:'$SITE'/csr_ha:'$SITE'/csr_cloud:$PATH' >> $HOME/.bashrc
source $HOME/.bashrc

echo "Show the current PATH" >> $install_log
echo $PATH >> $install_log
#echo "Show the current PYTHONPATH" >> $install_log
#echo $PYTHONPATH >> $install_log
echo "Show the python sites" >> $install_log
$PYTHON -m site >> $install_log

# Update csr_ha.service ExecStart script call
sudo sed -i "/ExecStart=.*/ c ExecStart=$PYTHON $SITE/csr_ha/server/ha_server.py start" $ha_dir/csr_ha.service

# Move the unit file for the csr_ha service
sudo mv $ha_dir/csr_ha.service /etc/systemd/user

# Start the high availability server
echo "Starting the high availability service" >> $install_log
sudo systemctl enable /etc/systemd/user/csr_ha.service
sudo systemctl start csr_ha.service
sudo systemctl status csr_ha >> $install_log
echo "NOTE: 'source ~/.bashrc' is necessary for HA commands to be accessible." >>$install_log

# Add a cron job to periodically revert nodes for primary routers
croncmd="bash $HOME/.local/lib/python2.7/site-packages/csr_ha/client_api/revert_nodes.sh"
cronjob="*/5 * * * * $croncmd"
( crontab -l | grep -v -F "$croncmd" ; echo "$cronjob" ) | crontab -
echo "Added cron job for HA node reversion" >> $install_log


# changing the directory permissions to run the debug_ha.sh script
sudo chown root:root $ha_dir/install.log $ha_dir/debug_ha.sh $ha_dir/ha_tools.sh $ha_dir/revert_nodes.sh
sudo chmod 777 $ha_dir/events
