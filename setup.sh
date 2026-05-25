#!/bin/bash
# Setup script voor ROS vision node dependencies
# Gebruik: bash setup.sh

echo "=== ROS Vision Package Setup ==="

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Huidige Python versie: $PYTHON_VERSION"

# Als Python < 3.8, upgrade naar 3.8
MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 8 ]); then
    echo "Python 3.6 gedetecteerd, upgraden naar 3.8..."
    sudo apt update
    sudo apt install -y python3.8 python3.8-venv python3.8-dev
    sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
    echo "Python upgraded naar 3.8"
fi

# Fix pip3 na Python upgrade
echo "pip3 repareren..."
python3 -m ensurepip --upgrade

# ROS dependencies (Melodic, niet Noetic)
echo "ROS dependencies installeren..."
sudo apt install -y ros-melodic-cv-bridge python3-rospy python3-yaml

# pip3 packages
echo "Python packages installeren..."
pip3 install -r requirements.txt

echo "=== Setup voltooid! ==="
echo "Volgende stap: catkin build"
