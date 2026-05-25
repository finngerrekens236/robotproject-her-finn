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
    echo "Python < 3.8 gedetecteerd, upgraden naar 3.8..."
    sudo apt update
    sudo apt install -y python3.8 python3.8-venv python3.8-dev
    sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
    echo "Python upgraded naar 3.8"
fi

# Installeer pip3 via apt (betrouwbaarder dan ensurepip op Debian/Ubuntu)
echo "pip3 installeren..."
sudo apt install -y python3-pip

# pip3 packages
echo "Python packages installeren (dit kan even duren)..."
pip3 install --user -r requirements.txt

echo ""
echo "=== Setup voltooid! ==="
echo "Volgende stap:"
echo "  source ~/ufactory_ws/devel/setup.bash"
echo "  roslaunch my_depthai vision.launch"
