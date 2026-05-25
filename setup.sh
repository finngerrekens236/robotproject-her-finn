#!/bin/bash
# Setup script voor ROS vision node dependencies (Python 3.8 + packages)
# Gebruik: bash setup.sh

echo "=== ROS Vision Package Setup ==="
echo ""

# 0. Maak schijfruimte vrij
echo "[0/6] Schijfruimte vrijmaken..."
sudo apt autoremove -y -qq > /dev/null 2>&1 || true
sudo apt autoclean -y -qq > /dev/null 2>&1 || true
DISK_FREE=$(df / | tail -1 | awk '{print $4}')
echo "     Vrije ruimte: $(numfmt --to=iec-i --suffix=B $DISK_FREE 2>/dev/null || echo $DISK_FREE KB)"
echo "[1/6] System updaten..."
sudo apt update -qq 2>/dev/null || true
sudo apt install -y -qq build-essential python3.8 python3.8-dev python3.8-venv 2>/dev/null || true
sudo apt install -y -qq python3-rospy python3-rospkg python3-catkin-pkg python3-sensor-msgs python3-geometry-msgs 2>/dev/null || true

# 2. Set Python 3.8 as default
echo "[2/6] Python 3.8 als default instellen..."
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1 > /dev/null 2>&1
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "     Python versie: $PYTHON_VERSION"

# 3. Repareer pip3 volledig
echo "[3/6] pip3 repareren en upgraden..."
sudo apt install --reinstall -y python3-pip > /dev/null 2>&1
rm -rf ~/.local/bin/pip* ~/.local/lib/python*/site-packages/pip* 2>/dev/null || true
python3 -m pip install --upgrade pip setuptools wheel --quiet

# 4. Installeer Python packages uit requirements.txt
echo "[4/6] Python packages installeren (dit kan ~3-5 minuten duren)..."
python3 -m pip install --user -r requirements.txt --quiet
python3 -m pip install --user rospy rospkg catkin-pkg --quiet

# 4b. Installeer depthai met pre-built binary (geen source compile)
echo "[4b/6] depthai installeren (pre-built)..."
python3 -m pip install --user --only-binary :all: depthai --quiet

# 5. Verify installatie
echo "[5/6] Verifiëren..."
python3 -c "import cv2; print('     ✓ opencv-python OK')" 2>/dev/null || (echo "     ✗ opencv-python FAILED"; exit 1)
python3 -c "import torch; print('     ✓ torch OK')" 2>/dev/null || (echo "     ✗ torch FAILED"; exit 1)
python3 -c "import depthai; print('     ✓ depthai OK')" 2>/dev/null || (echo "     ✗ depthai FAILED"; exit 1)
python3 -c "import yaml; print('     ✓ pyyaml OK')" 2>/dev/null || (echo "     ✗ pyyaml FAILED"; exit 1)

echo ""
echo "=== Setup voltooid! ==="
echo ""
echo "Volgende stappen:"
echo "  1. source ~/ufactory_ws/devel/setup.bash"
echo "  2. roslaunch my_depthai vision.launch"
echo ""
