"""
Command-line interface for making predictions with the Smart Crop Health Monitor model.

Usage:
    python predict_cli.py image.jpg
    python predict_cli.py image.jpg --show-all
    python predict_cli.py image.jpg --save-results results.txt
"""

import sys
import os
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from src.predict import PlantDiseasePredictor
from src.remedies import get_remedy, get_disease_info


def format_disease_name(name):
    """Format disease class name for display."""
    return name.replace("__", " - ").replace("_", " ")


def print_header(text, width=70):
    """Print formatted header."""
    print("\n" + "=" * width)
    print(f" {text:^{width-2}} ")
    print("=" * width + "\n")


def print_result(results, show_all=False):
    """Print prediction results."""
    if results is None:
        print("❌ Error: Prediction failed")
        return
    
    prediction = results["prediction"]
    remedy = results["remedy"]
    
    # Main prediction
    print_header("PREDICTION RESULT")
    
    predicted_class = prediction["predicted_class"]
    confidence = prediction["confidence"] * 100
    
    print(f"Predicted Disease: {format_disease_name(predicted_class)}")
    print(f"Confidence:       {confidence:.2f}%")
    
    if confidence < 70:
        print("⚠️  WARNING: Low confidence - image quality may affect accuracy")
    elif confidence >= 90:
        print("✓ High confidence prediction")
    
    # Top predictions
    print("\nTop Predictions:")
    for i, pred in enumerate(prediction["top_predictions"], 1):
        class_name = format_disease_name(pred["class"])
        conf = pred["confidence"] * 100
        print(f"  {i}. {class_name:40s} {conf:6.2f}%")
    
    # Disease information
    if remedy:
        print_header("DISEASE INFORMATION")
        
        print(f"Disease Name:  {remedy.get('disease_name', 'Unknown')}")
        print(f"Plant Type:    {remedy.get('plant', 'Unknown')}")
        print(f"Severity:      {remedy.get('severity', 'Unknown')}")
        
        print("\n📋 Symptoms:")
        for symptom in remedy.get("symptoms", []):
            print(f"   • {symptom}")
        
        print("\n🌿 Organic Treatment Options:")
        for treatment in remedy.get("organic_treatment", []):
            print(f"   • {treatment}")
        
        print("\n⚗️  Chemical Treatment Options:")
        treatments = remedy.get("chemical_treatment", [])
        if treatments:
            for treatment in treatments:
                print(f"   • {treatment}")
        else:
            print("   ℹ️  No chemical treatment available (viral disease)")
        
        print("\n🛡️  Prevention Strategies:")
        for prevention in remedy.get("prevention", []):
            print(f"   • {prevention}")
    
    # Show all predictions if requested
    if show_all:
        print_header("ALL PREDICTIONS")
        
        all_preds = sorted(
            prediction["all_predictions"].items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        for class_name, confidence in all_preds:
            formatted_name = format_disease_name(class_name)
            conf_pct = confidence * 100
            bar_length = int(conf_pct / 5)
            bar = "█" * bar_length + "░" * (20 - bar_length)
            print(f"{formatted_name:35s} [{bar}] {conf_pct:6.2f}%")


def save_results(results, filepath):
    """Save prediction results to a text file."""
    if results is None:
        return False
    
    try:
        with open(filepath, 'w') as f:
            prediction = results["prediction"]
            remedy = results["remedy"]
            
            f.write("SMART CROP HEALTH MONITOR - PREDICTION RESULTS\n")
            f.write("=" * 70 + "\n\n")
            
            # Prediction
            f.write("PREDICTION\n")
            f.write("-" * 70 + "\n")
            f.write(f"Predicted Disease: {format_disease_name(prediction['predicted_class'])}\n")
            f.write(f"Confidence: {prediction['confidence']*100:.2f}%\n\n")
            
            # Top predictions
            f.write("TOP PREDICTIONS\n")
            f.write("-" * 70 + "\n")
            for i, pred in enumerate(prediction["top_predictions"], 1):
                f.write(f"{i}. {format_disease_name(pred['class']):40s} {pred['confidence']*100:6.2f}%\n")
            f.write("\n")
            
            # Disease information
            if remedy:
                f.write("DISEASE INFORMATION\n")
                f.write("-" * 70 + "\n")
                f.write(f"Disease Name: {remedy.get('disease_name', 'Unknown')}\n")
                f.write(f"Plant Type: {remedy.get('plant', 'Unknown')}\n")
                f.write(f"Severity: {remedy.get('severity', 'Unknown')}\n\n")
                
                f.write("SYMPTOMS\n")
                for symptom in remedy.get("symptoms", []):
                    f.write(f"  • {symptom}\n")
                f.write("\n")
                
                f.write("ORGANIC TREATMENT\n")
                for treatment in remedy.get("organic_treatment", []):
                    f.write(f"  • {treatment}\n")
                f.write("\n")
                
                f.write("CHEMICAL TREATMENT\n")
                if remedy.get("chemical_treatment"):
                    for treatment in remedy.get("chemical_treatment", []):
                        f.write(f"  • {treatment}\n")
                else:
                    f.write("  (No chemical treatment available)\n")
                f.write("\n")
                
                f.write("PREVENTION\n")
                for prevention in remedy.get("prevention", []):
                    f.write(f"  • {prevention}\n")
        
        return True
    
    except Exception as e:
        print(f"❌ Error saving results: {str(e)}")
        return False


def main():
    """Main CLI function."""
    
    parser = argparse.ArgumentParser(
        description='Smart Crop Health Monitor - Command-line Prediction Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python predict_cli.py leaf.jpg
  python predict_cli.py leaf.jpg --show-all
  python predict_cli.py leaf.jpg --save-results output.txt
  python predict_cli.py leaf.jpg --model models/custom_model.h5
        """
    )
    
    parser.add_argument('image', help='Path to leaf image file')
    parser.add_argument('--model', default='models/plant_model.h5',
                       help='Path to trained model (default: models/plant_model.h5)')
    parser.add_argument('--show-all', action='store_true',
                       help='Show all predictions with confidence scores')
    parser.add_argument('--save-results', metavar='FILE',
                       help='Save results to a text file')
    parser.add_argument('--json', action='store_true',
                       help='Output results as JSON')
    
    args = parser.parse_args()
    
    # Check if image exists
    if not os.path.isfile(args.image):
        print(f"❌ Error: Image file not found: {args.image}")
        sys.exit(1)
    
    # Check if model exists
    if not os.path.isfile(args.model):
        print(f"❌ Error: Model file not found: {args.model}")
        print("Please train the model first: python src/train.py")
        sys.exit(1)
    
    print_header("SMART CROP HEALTH MONITOR")
    print(f"Image:  {args.image}")
    print(f"Model:  {args.model}\n")
    
    # Initialize predictor
    print("Loading model...")
    predictor = PlantDiseasePredictor(model_path=args.model)
    
    if predictor.model is None:
        print("❌ Error: Failed to load model")
        sys.exit(1)
    
    # Set class names
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
    
    # Make prediction
    print("Analyzing image...\n")
    results = predictor.predict_with_remedy(args.image)
    
    # Handle JSON output
    if args.json:
        import json
        json_output = {
            "prediction": {
                "predicted_class": results["prediction"]["predicted_class"],
                "confidence": float(results["prediction"]["confidence"]),
                "top_predictions": results["prediction"]["top_predictions"]
            }
        }
        print(json.dumps(json_output, indent=2))
    else:
        # Print results
        print_result(results, show_all=args.show_all)
    
    # Save results if requested
    if args.save_results:
        if save_results(results, args.save_results):
            print(f"\n✓ Results saved to: {args.save_results}")
        else:
            print(f"\n❌ Failed to save results")
            sys.exit(1)
    
    print("\n" + "=" * 70)
    print("Prediction complete!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)
