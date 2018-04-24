PIHOME=/home/pi
DEXTER=Dexter
DEXTER_PATH=$PIHOME/$DEXTER

source $DEXTER_PATH/script_tools/functions_library.sh

install_line_follower(){
  feedback "--> Installing Line Follower Calibration"
  # Install GoPiGo Line Follower Calibration
  delete_file /home/pi/Desktop/line_follow.desktop
  sudo cp /home/pi/Dexter/GoPiGo/Software/Python/line_follower/line_follow.desktop /home/pi/Desktop/
  sudo chmod +x /home/pi/Desktop/line_follow.desktop
  sudo chmod +x /home/pi/Dexter/GoPiGo/Software/Python/line_follower/line_sensor_gui.py

  # if the configuration files exist in the home directory
  # then move them to their new place
  # otherwise create new ones
  if file_exists "$PIHOME/black_line.txt"
  then
    sudo mv $PIHOME/black_line.txt $PIHOME/Dexter/black_line.txt
  else
    sudo cp $PIHOME/Dexter/GoPiGo/Software/Python/line_follower/black_line.txt $PIHOME/Dexter/black_line.txt
  fi

  if file_exists "$PIHOME/white_line.txt"
  then
    sudo mv $PIHOME/white_line.txt $PIHOME/Dexter/white_line.txt
  else
    sudo cp $PIHOME/Dexter/GoPiGo/Software/Python/line_follower/white_line.txt $PIHOME/Dexter/white_line.txt
  fi
  if file_exists "$PIHOME/range_line.txt"
  then
    sudo mv $PIHOME/range_line.txt $PIHOME/Dexter/range_line.txt
  else
    sudo cp $PIHOME/Dexter/GoPiGo/Software/Python/line_follower/range_line.txt $PIHOME/Dexter/range_line.txt
  fi

  sudo chmod 666 $PIHOME/Dexter/*line.txt
}

install_control_panel(){
  sudo cp "$ROBOT_DIR/Software/Python/control_panel/gopigo_control_panel.desktop" $PIHOME/Desktop
}
