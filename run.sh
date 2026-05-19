#!/bin/bash
# Smart Crop Health Monitor - Linux/macOS Launcher
# This script activates the virtual environment and runs the Streamlit app

echo ""
echo "======================================"
echo "  SMART CROP HEALTH MONITOR"
echo "  Plant Disease Detection System"
echo "======================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[!] Virtual environment not found!"
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
echo "[+] Activating virtual environment..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to activate virtual environment"
    exit 1
fi

# Check if requirements are installed
pip show streamlit > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "[+] Installing dependencies..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to install dependencies"
        exit 1
    fi
fi

# Check if model exists
if [ ! -f "models/plant_model.h5" ]; then
    echo ""
    echo "[!] Model not found at models/plant_model.h5"
    echo ""
    echo "The model needs to be trained first. Would you like to train it now?"
    echo "This may take 30-60 minutes."
    echo ""
    read -p "Train model now? (y/n): " train_choice
    
    if [ "$train_choice" == "y" ] || [ "$train_choice" == "Y" ]; then
        echo ""
        echo "[+] Starting model training..."
        python src/train.py
        if [ $? -ne 0 ]; then
            echo "[ERROR] Training failed"
            exit 1
        fi
    else
        echo "[!] Model training skipped. The app will not work without the model."
        echo "Please run: python src/train.py"
        exit 1
    fi
fi

# Launch Streamlit app
echo ""
echo "[+] Launching Smart Crop Health Monitor..."
echo "[+] Opening browser at http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run app/app.py
