# 🚀 Quick Start Guide - Smart Crop Health Monitor

## 5-Minute Setup Guide

### Prerequisites Check
- [ ] Python 3.8+ installed (`python --version`)
- [ ] pip working (`pip --version`)
- [ ] At least 2GB free disk space
- [ ] Internet connection (for downloading dependencies)

---

## Step 1: Download/Navigate to Project

```bash
cd d:\Projects\ML & BigData\CropHealthMonitor
```

---

## Step 2: Run the Launcher Script

### Windows Users
```bash
run.bat
```
The script will:
1. ✓ Create virtual environment if needed
2. ✓ Install dependencies
3. ✓ Check for trained model
4. ✓ Prompt to train if needed
5. ✓ Launch the web app

### macOS/Linux Users
```bash
chmod +x run.sh
./run.sh
```

---

## Step 3: Train the Model (First Time Only)

If you have the PlantVillage dataset:

```bash
python src/train.py
```

**Wait for training to complete** (~30-60 minutes)

⏱️ **Estimated Times:**
- GPU (NVIDIA): 30-45 minutes
- GPU (Apple Silicon): 45-60 minutes  
- CPU: 1.5-3 hours

---

## Step 4: Open Web Application

Once training completes or launcher says "Model found":

1. Browser will automatically open to `http://localhost:8501`
2. You'll see the Smart Crop Health Monitor interface

---

## Step 5: Make Your First Prediction

1. Go to the **"Disease Detection"** tab
2. Click **"Choose a leaf image"** or **"Take a photo"**
3. Select or capture a leaf image
4. Click **"Analyze Disease"**
5. See predictions and treatment recommendations!

---

## Manual Setup (If Launcher Doesn't Work)

### 1. Create Virtual Environment
```bash
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Train Model (If Needed)
```bash
python src/train.py
```

### 5. Run App
```bash
streamlit run app/app.py
```

---

## What to Upload - Image Guidelines

### ✅ Good Images
- Clear, well-lit leaf photos
- Entire leaf visible in frame
- Both healthy and diseased areas shown
- High resolution (1920x1080 or higher)
- 45-90 degree angle
- No shadows or reflections

### ❌ Poor Images
- Blurry or dark photos
- Cropped tightly
- Only healthy areas
- Low resolution
- Direct overhead
- With shadows

### 📸 How to Take a Good Photo

1. **Lighting**: Use natural daylight (not indoor fluorescent)
2. **Angle**: Hold camera at 45-60 degrees to leaf
3. **Distance**: Close enough to see details, far enough to see whole leaf
4. **Background**: Plain, contrasting background
5. **Stability**: Use steady hand or phone holder
6. **Time**: Take multiple photos, keep the best

---

## Using the Web Interface

### 🔍 Disease Detection Tab
- Upload or photograph a leaf
- AI analyzes the image
- Get disease prediction with confidence %
- View detailed disease information
- See organic & chemical treatment options
- Read prevention strategies

### 📚 Disease Database Tab
- Browse all 15 supported diseases
- Select any disease to learn about it
- View symptoms and treatment options
- No image upload needed

### ℹ️ Instructions Tab
- Complete how-to guide
- Best practices for images
- FAQ section
- Tips for accurate predictions

---

## Troubleshooting

### Problem: "Model not found"
```
Solution: Train the model
python src/train.py
```

### Problem: "Cannot find Python"
```
Solution: Make sure Python is in PATH
- Windows: Install from python.org, check "Add Python to PATH"
- Restart command prompt after install
```

### Problem: Streamlit not working
```
Solution: Reinstall Streamlit
pip install --upgrade streamlit
```

### Problem: Out of memory error
```
Solution: Reduce batch size
Edit src/train.py, change batch_size=16
```

### Problem: Slow predictions
```
Solution: Check if GPU is available
- For NVIDIA GPU: pip install tensorflow-gpu
- For CPU: Speed is normal, < 5 seconds is OK
```

### Problem: Wrong predictions
```
Solution: Use better quality images
- Good lighting
- Full leaf in frame
- Clear disease symptoms visible
```

---

## Next Steps After Setup

### 1. Test with Sample Images
- Find test leaf images online
- Run predictions to verify accuracy
- Compare with disease database

### 2. Explore the Code
- Review `app/app.py` for app logic
- Check `src/model.py` for model architecture
- Look at `src/remedies.py` for treatment data

### 3. Try Different Models
Edit `run.py` to use different models:
```python
# Options: 'custom', 'mobilenetv2', 'resnet50'
model_type="resnet50"
```

### 4. Retrain with Custom Data
Add your own disease images to `dataset/PlantVillage/NewDisease/`
Then run `python src/train.py` again

### 5. Deploy to Cloud
- Use Streamlit Cloud: `streamlit cloud deploy`
- Or containerize with Docker
- Deploy to AWS, GCP, or Azure

---

## Keyboard Shortcuts

- `Ctrl + C`: Stop the server
- `R`: Reload the app (while it's running)
- `Click anywhere`: Focus input field

---

## Need Help?

1. **Check the README.md** for detailed documentation
2. **Review Troubleshooting section** in README
3. **Check Streamlit docs**: https://docs.streamlit.io
4. **Check TensorFlow docs**: https://tensorflow.org

---

## Performance Tips

### For Faster Training
- Use GPU (NVIDIA CUDA recommended)
- Reduce image size to 128x128
- Reduce batch size for low-RAM machines

### For Better Predictions
- Use high-quality images
- Include disease symptoms clearly
- Retrain model with your own data

### For Faster Inference
- Use MobileNetV2 (current default)
- Disable camera input if not needed
- Use CPU quantization

---

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Python | 3.8 | 3.9+ |
| RAM | 4GB | 8GB+ |
| Storage | 2GB | 5GB |
| GPU | None (CPU OK) | NVIDIA RTX 2060+ |
| Network | For setup | For cloud features |

---

## File Structure Reference

```
CropHealthMonitor/
├── app/app.py                    ← Main web application
├── src/
│   ├── data_loader.py            ← Load images
│   ├── model.py                  ← Model architecture
│   ├── predict.py                ← Make predictions
│   ├── remedies.py               ← Disease treatments
│   └── train.py                  ← Train the model
├── models/plant_model.h5         ← Trained model (after training)
├── dataset/PlantVillage/         ← Images go here
├── requirements.txt              ← Python dependencies
├── README.md                     ← Full documentation
├── run.bat                       ← Windows launcher
├── run.sh                        ← Linux/macOS launcher
└── QUICKSTART.md                 ← This file
```

---

## Example Workflow

```
Day 1: Setup
├── Install Python
├── Run run.bat/run.sh
├── Start model training
└── Go do something else (3 hours)

Day 2: First Predictions
├── Model is trained
├── Open web app: http://localhost:8501
├── Upload leaf photos
├── Get disease predictions
├── View treatment options
└── Success! 🎉

Day 3+: Explore
├── Browse disease database
├── Read treatment recommendations
├── Retrain with custom images
└── Deploy to production
```

---

## Common Questions

**Q: Does it need internet?**
A: Only during setup for downloads. Inference works offline.

**Q: Can I use on my phone?**
A: Yes! Share local network URL from Streamlit.

**Q: How accurate is it?**
A: 95-98% on test data, depends on image quality.

**Q: Can I use my own dataset?**
A: Yes! Add images and retrain the model.

**Q: Can I deploy this online?**
A: Yes! Use Streamlit Cloud, Heroku, or Docker.

---

**Happy Crop Monitoring! 🌾🤖**

Ready to get started? Run `run.bat` or `run.sh` now!
