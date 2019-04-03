PIHOME=/home/pi
DEXTER=Dexter
DEXTER_PATH=$PIHOME/$DEXTER
SCRIPT_TOOLS=$DEXTER_PATH/lib/Dexter/script_tools

source $SCRIPT_TOOLS/functions_library.sh

configure_line_follower(){
  # Install Line Follower Calibration
  if [ -d /home/pi/Desktop ]; then
    delete_file $PIHOME/Desktop/line_follow.desktop
    delete_file $PIHOME/Desktop/line_follower_calibration.desktop
    sudo cp $PIHOME/$DEXTER/DI_Sensors/Python/di_sensors/line_follower_calibration/line_follower_calibration.desktop $PIHOME/Desktop/
    sudo chmod +x $PIHOME/Desktop/line_follower_calibration.desktop
    sudo chmod +x $PIHOME/Dexter/DI_Sensors/Python/di_sensors/line_follower_calibration/line_sensor_calibration_gui.py
  fi

  # if the configuration files exist in the home directory
  # then move them to their new place
  # otherwise create new ones
  if file_exists "$PIHOME/black_line.txt"
  then
    sudo mv $PIHOME/black_line.txt $PIHOME/Dexter/black_line.txt
  else
    sudo cp $PIHOME/Dexter/DI_Sensors/Python/di_sensors/red_line_follower/line_follower/black_line.txt $PIHOME/Dexter/black_line.txt
  fi

  if file_exists "$PIHOME/white_line.txt"
  then
    sudo mv $PIHOME/white_line.txt $PIHOME/Dexter/white_line.txt
  else
    sudo cp $PIHOME/Dexter/DI_Sensors/Python/di_sensors/red_line_follower/line_follower/white_line.txt $PIHOME/Dexter/white_line.txt
  fi
  if file_exists "$PIHOME/range_line.txt"
  then
    sudo mv $PIHOME/range_line.txt $PIHOME/Dexter/range_line.txt
  else
    sudo cp $PIHOME/Dexter/DI_Sensors/Python/di_sensors/red_line_follower/line_follower/range_line.txt $PIHOME/Dexter/range_line.txt
  fi

  sudo chmod 666 $PIHOME/Dexter/*line.txt
}
