"""
Test and Demo Script for Smart Crop Health Monitor

This script verifies that all components are properly installed and configured.
Run this before using the main application.
"""

import sys
import os
from pathlib import Path

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Print a formatted header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")


def print_success(text):
    """Print success message."""
    print(f"{Colors.GREEN}[OK] {text}{Colors.END}")


def print_error(text):
    """Print error message."""
    print(f"{Colors.RED}[FAIL] {text}{Colors.END}")


def print_warning(text):
    """Print warning message."""
    print(f"{Colors.YELLOW}[WARN] {text}{Colors.END}")


def print_info(text):
    """Print info message."""
    print(f"{Colors.BLUE}[INFO] {text}{Colors.END}")


def test_python_version():
    """Test Python version."""
    print_header("Testing Python Version")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version_str}")
        return True
    else:
        print_error(f"Python {version_str} (Required: 3.8+)")
        return False


def test_imports():
    """Test if all required packages are installed."""
    print_header("Testing Required Packages")
    
    packages = {
        'numpy': 'NumPy',
        'pandas': 'Pandas',
        'cv2': 'OpenCV',
        'tensorflow': 'TensorFlow',
        'keras': 'Keras',
        'streamlit': 'Streamlit',
        'PIL': 'Pillow',
        'sklearn': 'Scikit-learn'
    }
    
    all_ok = True
    for import_name, display_name in packages.items():
        try:
            mod = __import__(import_name)
            version = getattr(mod, '__version__', 'unknown')
            print_success(f"{display_name} ({version})")
        except ImportError:
            print_error(f"{display_name} - NOT INSTALLED")
            all_ok = False
    
    return all_ok


def test_directory_structure():
    """Test if directory structure is correct."""
    print_header("Testing Directory Structure")
    
    required_dirs = [
        'app',
        'src',
        'dataset',
        'models',
        'notebooks'
    ]
    
    all_ok = True
    for directory in required_dirs:
        if os.path.isdir(directory):
            print_success(f"Directory '{directory}/' exists")
        else:
            print_error(f"Directory '{directory}/' NOT FOUND")
            all_ok = False
    
    return all_ok


def test_files():
    """Test if required files exist."""
    print_header("Testing Required Files")
    
    required_files = {
        'app/app.py': 'Main Streamlit app',
        'src/data_loader.py': 'Data loading module',
        'src/model.py': 'Model architecture',
        'src/predict.py': 'Prediction utilities',
        'src/remedies.py': 'Disease remedies database',
        'src/train.py': 'Training script',
        'requirements.txt': 'Dependencies',
        'README.md': 'Documentation'
    }
    
    all_ok = True
    for filepath, description in required_files.items():
        if os.path.isfile(filepath):
            size = os.path.getsize(filepath)
            if size > 0:
                print_success(f"{filepath} ({size:,} bytes) - {description}")
            else:
                print_warning(f"{filepath} (EMPTY) - {description}")
        else:
            print_error(f"{filepath} NOT FOUND - {description}")
            all_ok = False
    
    return all_ok


def test_model():
    """Test if trained model exists."""
    print_header("Testing Trained Model")
    
    model_path = 'models/plant_model.h5'
    
    if os.path.isfile(model_path):
        size = os.path.getsize(model_path)
        size_mb = size / (1024 * 1024)
        print_success(f"Model found: {model_path} ({size_mb:.2f} MB)")
        
        # Try loading the model
        try:
            import tensorflow as tf
            model = tf.keras.models.load_model(model_path)
            print_success(f"Model loads successfully")
            print_info(f"Model parameters: {model.count_params():,}")
            return True
        except Exception as e:
            print_error(f"Error loading model: {str(e)}")
            return False
    else:
        print_warning(f"Model not found: {model_path}")
        print_info("To train the model, run: python src/train.py")
        return False


def test_dataset():
    """Test if dataset exists."""
    print_header("Testing Dataset")
    
    dataset_path = 'dataset/PlantVillage'
    
    if os.path.isdir(dataset_path):
        classes = [d for d in os.listdir(dataset_path) 
                  if os.path.isdir(os.path.join(dataset_path, d))]
        total_images = 0
        
        for class_name in classes[:3]:  # Check first 3 classes
            class_path = os.path.join(dataset_path, class_name)
            images = [f for f in os.listdir(class_path) 
                     if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
            total_images += len(images)
            print_info(f"{class_name}: {len(images)} images")
        
        print_success(f"Dataset found with {len(classes)} disease classes")
        return True
    else:
        print_warning(f"Dataset not found: {dataset_path}")
        print_info("Download PlantVillage dataset from: https://plantvillage.psu.edu/")
        return False


def test_remedies():
    """Test if remedies database is working."""
    print_header("Testing Remedies Database")
    
    try:
        from src.remedies import get_all_diseases, get_remedy, get_disease_info
        
        diseases = get_all_diseases()
        print_success(f"Remedies database loaded with {len(diseases)} diseases")
        
        # Test a sample disease
        if len(diseases) > 0:
            sample_disease = diseases[0]
            remedy = get_remedy(sample_disease)
            
            if remedy:
                disease_name = remedy.get('disease_name', 'Unknown')
                print_info(f"Sample disease: {disease_name}")
                print_info(f"  - Severity: {remedy.get('severity', 'Unknown')}")
                print_info(f"  - Organic treatments: {len(remedy.get('organic_treatment', []))}")
                print_info(f"  - Prevention tips: {len(remedy.get('prevention', []))}")
            
            return True
        else:
            print_error("No diseases found in remedies database")
            return False
    
    except Exception as e:
        print_error(f"Error loading remedies: {str(e)}")
        return False


def test_prediction():
    """Test prediction system."""
    print_header("Testing Prediction System")
    
    try:
        from src.predict import PlantDiseasePredictor
        
        model_path = 'models/plant_model.h5'
        
        if not os.path.isfile(model_path):
            print_warning("Model not found - skipping prediction test")
            print_info("Prediction test will work after training the model")
            return True
        
        predictor = PlantDiseasePredictor(model_path)
        
        if predictor.model is not None:
            print_success("Predictor initialized successfully")
            
            class_names = [
                "Pepper__bell___Bacterial_spot", "Pepper__bell___healthy",
                "Potato___Early_blight", "Potato___healthy", "Potato___Late_blight",
                "Tomato__Target_Spot", "Tomato__Tomato_mosaic_virus",
                "Tomato__Tomato_YellowLeaf__Curl_Virus", "Tomato_Bacterial_spot",
                "Tomato_Early_blight", "Tomato_healthy", "Tomato_Late_blight",
                "Tomato_Leaf_Mold", "Tomato_Septoria_leaf_spot",
                "Tomato_Spider_mites_Two_spotted_spider_mite"
            ]
            
            predictor.set_class_names(class_names)
            print_success(f"Prediction system ready for {len(class_names)} classes")
            return True
        else:
            print_error("Failed to initialize predictor")
            return False
    
    except Exception as e:
        print_error(f"Error testing prediction: {str(e)}")
        return False


def run_all_tests():
    """Run all tests."""
    print_header("SMART CROP HEALTH MONITOR - SYSTEM CHECK")
    
    results = {
        'Python Version': test_python_version(),
        'Required Packages': test_imports(),
        'Directory Structure': test_directory_structure(),
        'Required Files': test_files(),
        'Remedies Database': test_remedies(),
        'Prediction System': test_prediction(),
        'Trained Model': test_model(),
        'Dataset': test_dataset()
    }
    
    # Summary
    print_header("Test Summary")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = f"{Colors.GREEN}PASS{Colors.END}" if result else f"{Colors.RED}FAIL{Colors.END}"
        print(f"  {test_name:.<40} {status}")
    
    print(f"\n{Colors.BOLD}Total: {passed}/{total} tests passed{Colors.END}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}All systems operational!{Colors.END}")
        print(f"{Colors.BLUE}You can now run: streamlit run app/app.py{Colors.END}")
        return True
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}Some tests failed{Colors.END}")
        if not test_imports():
            print(f"\n{Colors.YELLOW}Run this to install missing packages:{Colors.END}")
            print(f"{Colors.BOLD}pip install -r requirements.txt{Colors.END}")
        if not test_model():
            print(f"\n{Colors.YELLOW}Run this to train the model:{Colors.END}")
            print(f"{Colors.BOLD}python src/train.py{Colors.END}")
        return False


def demo_remedies():
    """Demo the remedies database."""
    print_header("REMEDIES DATABASE DEMO")
    
    try:
        from src.remedies import get_all_diseases, get_disease_info
        
        diseases = get_all_diseases()
        
        if len(diseases) > 0:
            # Show info for first disease
            disease = diseases[0]
            info = get_disease_info(disease)
            print(info)
            
            print(f"\n{Colors.BLUE}Total diseases in database: {len(diseases)}{Colors.END}")
        
    except Exception as e:
        print_error(f"Error showing demo: {str(e)}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Test Smart Crop Health Monitor setup')
    parser.add_argument('--demo', action='store_true', help='Show remedies database demo')
    parser.add_argument('--quick', action='store_true', help='Run only quick tests')
    
    args = parser.parse_args()
    
    if args.demo:
        demo_remedies()
    elif args.quick:
        print_header("QUICK TEST")
        test_python_version()
        test_imports()
        test_files()
    else:
        success = run_all_tests()
        sys.exit(0 if success else 1)
