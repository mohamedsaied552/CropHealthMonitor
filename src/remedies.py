"""
Plant disease remedies and treatment recommendations.
Includes organic and chemical treatment options.
"""

REMEDIES = {
    "Pepper__bell___Bacterial_spot": {
        "disease_name": "Bacterial Spot",
        "plant": "Pepper (Bell)",
        "severity": "High",
        "symptoms": [
            "Small, dark, greasy spots on leaves",
            "Spots develop yellow halos",
            "Spots may merge and cause defoliation",
            "Affects fruits as well"
        ],
        "organic_treatment": [
            "Remove and destroy infected plant parts",
            "Apply copper-based fungicide (e.g., Bordeaux mixture) early in season",
            "Ensure good air circulation by pruning lower leaves",
            "Avoid overhead watering to prevent leaf wetness",
            "Use drip irrigation instead of overhead sprinklers",
            "Sanitize pruning tools between cuts"
        ],
        "chemical_treatment": [
            "Apply copper sulfate fungicide every 7-10 days",
            "Use streptomycin-based antibiotics for severe infections",
            "Apply fixed copper products as preventative",
            "Follow label instructions carefully"
        ],
        "prevention": [
            "Use disease-resistant pepper varieties",
            "Maintain field hygiene and crop rotation",
            "Avoid working in wet plants",
            "Ensure proper spacing for air circulation",
            "Test soil pH and ensure proper nutrition"
        ]
    },
    
    "Pepper__bell___healthy": {
        "disease_name": "Healthy",
        "plant": "Pepper (Bell)",
        "severity": "None",
        "symptoms": ["No disease detected"],
        "organic_treatment": ["Plant is healthy - no treatment needed"],
        "chemical_treatment": [],
        "prevention": ["Continue regular monitoring and good cultural practices"]
    },
    
    "Potato___Early_blight": {
        "disease_name": "Early Blight",
        "plant": "Potato",
        "severity": "Medium-High",
        "symptoms": [
            "Small, dark brown spots with concentric rings (target-like)",
            "Yellow halo around spots",
            "Starts on lower leaves",
            "Can cause severe defoliation"
        ],
        "organic_treatment": [
            "Remove lower leaves (bottom 4-6 inches) for air circulation",
            "Apply copper or sulfur fungicides every 7 days",
            "Mulch around plants to prevent soil-to-leaf contact",
            "Harvest tubers immediately when mature",
            "Ensure proper spacing and avoid overhead irrigation",
            "Use crop rotation (3-4 years)"
        ],
        "chemical_treatment": [
            "Apply mancozeb or chlorothalonil fungicides every 5-7 days",
            "Use combination fungicides for better control",
            "Apply protectant fungicides before conditions favor disease",
            "Follow rotation of fungicide classes to prevent resistance"
        ],
        "prevention": [
            "Plant certified disease-free seed potatoes",
            "Use resistant varieties",
            "Ensure adequate soil drainage",
            "Maintain good air circulation",
            "Avoid wounding tubers during harvest"
        ]
    },
    
    "Potato___healthy": {
        "disease_name": "Healthy",
        "plant": "Potato",
        "severity": "None",
        "symptoms": ["No disease detected"],
        "organic_treatment": ["Plant is healthy - maintain monitoring"],
        "chemical_treatment": [],
        "prevention": ["Continue good cultural practices"]
    },
    
    "Potato___Late_blight": {
        "disease_name": "Late Blight",
        "plant": "Potato",
        "severity": "Very High",
        "symptoms": [
            "Water-soaked spots on leaves and stems",
            "White fungal growth on leaf undersides",
            "Rapid spread during wet conditions",
            "Tubers show brown rot inside"
        ],
        "organic_treatment": [
            "Remove all infected plant material immediately",
            "Apply copper fungicides weekly during wet weather",
            "Use Bacillus subtilis or Trichoderma-based products",
            "Ensure excellent drainage",
            "Apply mulch to prevent soil splash",
            "Scout for symptoms twice weekly"
        ],
        "chemical_treatment": [
            "Apply metalaxyl or mefenoxam fungicides",
            "Use combination products with mancozeb",
            "Apply protectant fungicides preventively during wet season",
            "Alternate fungicide classes to prevent resistance",
            "Apply every 5-7 days during susceptible period"
        ],
        "prevention": [
            "Use resistant varieties (R8, R9, R10 genes)",
            "Plant certified disease-free seed",
            "Avoid overhead watering",
            "Ensure good soil drainage",
            "Remove volunteer potatoes",
            "Destroy cull piles after harvest"
        ]
    },
    
    "Tomato__Target_Spot": {
        "disease_name": "Target Spot",
        "plant": "Tomato",
        "severity": "Medium",
        "symptoms": [
            "Small brown spots with concentric rings",
            "Gray center with tan background",
            "Affects older leaves first",
            "Spots coalesce causing leaf yellowing"
        ],
        "organic_treatment": [
            "Remove infected leaves",
            "Apply copper fungicides every 7 days",
            "Maintain proper spacing for air circulation",
            "Prune lower branches for better air flow",
            "Use drip irrigation to keep leaves dry",
            "Mulch around plants"
        ],
        "chemical_treatment": [
            "Apply chlorothalonil or mancozeb fungicides",
            "Use combination fungicides containing carbendazim",
            "Apply every 5-7 days during growing season",
            "Alternate fungicide classes"
        ],
        "prevention": [
            "Use resistant varieties",
            "Use disease-free seeds",
            "Ensure proper plant spacing",
            "Avoid overhead watering",
            "Practice crop rotation (2-3 years)"
        ]
    },
    
    "Tomato__Tomato_mosaic_virus": {
        "disease_name": "Tomato Mosaic Virus (ToMV)",
        "plant": "Tomato",
        "severity": "High",
        "symptoms": [
            "Mottled, mosaic pattern on leaves",
            "Light and dark green patches",
            "Leaf distortion and curling",
            "Stunted growth",
            "Poor fruit set"
        ],
        "organic_treatment": [
            "Remove infected plants to prevent spread",
            "Disinfect tools between plants",
            "Avoid handling plants when wet",
            "Remove infected leaves immediately",
            "Control aphids and other vectors",
            "Use resistant varieties"
        ],
        "chemical_treatment": [
            "No cure for viral diseases",
            "Remove and destroy infected plants",
            "Control insect vectors with neem oil or insecticidal soap"
        ],
        "prevention": [
            "Use resistant varieties (R gene)",
            "Start with virus-free seeds",
            "Disinfect tools with bleach (1:9 ratio)",
            "Avoid working in wet plants",
            "Control insect vectors",
            "Remove weeds that harbor virus"
        ]
    },
    
    "Tomato__Tomato_YellowLeaf__Curl_Virus": {
        "disease_name": "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "plant": "Tomato",
        "severity": "Very High",
        "symptoms": [
            "Yellowing of leaves",
            "Upward curling of leaf margins",
            "Stunted plant growth",
            "Reduced flowering and fruiting",
            "Plants may die"
        ],
        "organic_treatment": [
            "Remove infected plants immediately",
            "Control whitefly vectors with neem oil",
            "Use yellow sticky traps for monitoring",
            "Provide shade cloth to reduce whitefly activity",
            "Remove alternate hosts and weeds"
        ],
        "chemical_treatment": [
            "No cure for viral infection",
            "Remove and destroy infected plants",
            "Control whiteflies with insecticides",
            "Use insecticides like imidacloprid or acetamiprid"
        ],
        "prevention": [
            "Use resistant varieties (TYLCV-resistant lines)",
            "Use certified virus-free seeds",
            "Employ reflective mulches to repel whiteflies",
            "Screen seedlings before transplanting",
            "Control weeds around field perimeter",
            "Avoid working near infected plants"
        ]
    },
    
    "Tomato_Bacterial_spot": {
        "disease_name": "Bacterial Spot",
        "plant": "Tomato",
        "severity": "High",
        "symptoms": [
            "Small, dark, greasy spots on leaves and fruits",
            "Spots develop yellow halos",
            "Spots may have a target-like appearance",
            "Can cause significant defoliation"
        ],
        "organic_treatment": [
            "Remove infected plant parts",
            "Apply copper fungicides every 7-10 days",
            "Ensure good air circulation",
            "Use drip irrigation instead of overhead watering",
            "Avoid pruning plants when wet",
            "Sanitize tools between cuts"
        ],
        "chemical_treatment": [
            "Apply copper sulfate or fixed copper products",
            "Use streptomycin antibiotics for severe cases",
            "Apply every 5-7 days during growing season",
            "Spray preventively after pruning or heavy rain"
        ],
        "prevention": [
            "Use disease-resistant varieties",
            "Use certified disease-free seeds",
            "Practice crop rotation (2-3 years)",
            "Maintain proper spacing",
            "Avoid overhead watering",
            "Remove field debris after harvest"
        ]
    },
    
    "Tomato_Early_blight": {
        "disease_name": "Early Blight",
        "plant": "Tomato",
        "severity": "Medium-High",
        "symptoms": [
            "Target-like spots with concentric rings",
            "Brown rings on leaves",
            "Yellow halo around lesions",
            "Starts on lower leaves",
            "Can cause severe defoliation"
        ],
        "organic_treatment": [
            "Remove lower leaves (bottom 6-8 inches)",
            "Apply copper fungicides every 7 days",
            "Mulch to prevent soil-to-leaf contact",
            "Prune lower branches for air circulation",
            "Water at soil level to keep leaves dry",
            "Harvest regularly to reduce plant stress"
        ],
        "chemical_treatment": [
            "Apply mancozeb or chlorothalonil fungicides",
            "Use combination fungicides",
            "Apply every 5-7 days starting early season",
            "Alternate fungicide classes"
        ],
        "prevention": [
            "Use resistant varieties",
            "Remove lower leaves at planting",
            "Practice crop rotation (2-3 years)",
            "Ensure good air circulation",
            "Avoid overhead watering",
            "Remove plant debris after harvest"
        ]
    },
    
    "Tomato_healthy": {
        "disease_name": "Healthy",
        "plant": "Tomato",
        "severity": "None",
        "symptoms": ["No disease detected"],
        "organic_treatment": ["Plant is healthy - continue monitoring"],
        "chemical_treatment": [],
        "prevention": ["Maintain regular crop monitoring"]
    },
    
    "Tomato_Late_blight": {
        "disease_name": "Late Blight",
        "plant": "Tomato",
        "severity": "Very High",
        "symptoms": [
            "Water-soaked spots on leaves",
            "White fungal growth on leaf undersides",
            "Rapid spread during cool, wet weather",
            "Stems show greasy streaks",
            "Fruit rot with white fungal growth"
        ],
        "organic_treatment": [
            "Remove infected leaves and fruits",
            "Apply copper fungicides weekly",
            "Use Bacillus subtilis products",
            "Ensure excellent drainage",
            "Increase air circulation",
            "Avoid overhead watering"
        ],
        "chemical_treatment": [
            "Apply metalaxyl or mefenoxam fungicides",
            "Use combination products with mancozeb",
            "Apply every 5-7 days during susceptible conditions",
            "Start preventive treatment in cool, wet weather"
        ],
        "prevention": [
            "Use resistant varieties",
            "Use certified disease-free seeds",
            "Ensure proper drainage",
            "Avoid overhead watering",
            "Monitor for symptoms regularly",
            "Remove volunteer tomato plants"
        ]
    },
    
    "Tomato_Leaf_Mold": {
        "disease_name": "Leaf Mold",
        "plant": "Tomato",
        "severity": "Medium",
        "symptoms": [
            "Pale green patches on upper leaf surface",
            "Gray or olive-green mold on undersides",
            "Affected leaves turn brown and die",
            "Affects older leaves first"
        ],
        "organic_treatment": [
            "Remove infected leaves",
            "Improve air circulation by pruning",
            "Use sulfur-based fungicides",
            "Apply neem oil spray",
            "Reduce humidity by watering at soil level",
            "Space plants farther apart"
        ],
        "chemical_treatment": [
            "Apply benomyl or carbendazim fungicides",
            "Use chlorothalonil sprays",
            "Apply every 7-10 days",
            "Focus on undersides of leaves"
        ],
        "prevention": [
            "Ensure proper ventilation in greenhouse",
            "Use humidity control",
            "Avoid overhead watering",
            "Keep humidity below 85% if possible",
            "Remove lower leaves regularly",
            "Use resistant varieties"
        ]
    },
    
    "Tomato_Septoria_leaf_spot": {
        "disease_name": "Septoria Leaf Spot",
        "plant": "Tomato",
        "severity": "Medium",
        "symptoms": [
            "Small, dark brown circular spots",
            "Gray centers with dark margins",
            "Black dots (pycnidia) in centers",
            "Rings of spots causing yellowing",
            "Affects lower and older leaves first"
        ],
        "organic_treatment": [
            "Remove infected leaves",
            "Apply copper fungicides every 7 days",
            "Use sulfur-based treatments",
            "Ensure good air circulation",
            "Water at soil level only",
            "Mulch around plants"
        ],
        "chemical_treatment": [
            "Apply chlorothalonil fungicides",
            "Use mancozeb products",
            "Apply every 5-7 days during growing season",
            "Begin treatment when spots first appear"
        ],
        "prevention": [
            "Use resistant varieties",
            "Use certified disease-free seeds",
            "Practice crop rotation (3-4 years)",
            "Remove field debris after harvest",
            "Disinfect tools between plants",
            "Ensure proper spacing"
        ]
    },
    
    "Tomato_Spider_mites_Two_spotted_spider_mite": {
        "disease_name": "Two-Spotted Spider Mite (Pest)",
        "plant": "Tomato",
        "severity": "High",
        "symptoms": [
            "Fine webbing on leaves and stems",
            "Yellow speckles on leaves",
            "Leaves become bronzed",
            "Severe damage causes leaf drop",
            "Visible tiny red or yellow mites"
        ],
        "organic_treatment": [
            "Spray with water to dislodge mites",
            "Apply neem oil spray every 3-4 days",
            "Use insecticidal soap",
            "Introduce predatory mites",
            "Increase humidity to discourage spider mites",
            "Remove heavily infested leaves"
        ],
        "chemical_treatment": [
            "Apply miticide like abamectin",
            "Use dicofol or propargite",
            "Apply sulfur dust (if temperature permits)",
            "Rotate miticides to prevent resistance"
        ],
        "prevention": [
            "Maintain adequate humidity (60-70%)",
            "Avoid excessive nitrogen fertilizer",
            "Scout plants regularly",
            "Remove weeds that harbor mites",
            "Use reflective mulches",
            "Encourage beneficial insects"
        ]
    }
}


def get_remedy(disease_name):
    """
    Get treatment recommendations for a specific disease.
    
    Args:
        disease_name: Name of the disease class
        
    Returns:
        dict: Treatment information or None if not found
    """
    return REMEDIES.get(disease_name)


def get_all_diseases():
    """Get list of all recognized diseases."""
    return list(REMEDIES.keys())


def get_disease_info(disease_name):
    """
    Get formatted disease information.
    
    Args:
        disease_name: Name of the disease class
        
    Returns:
        str: Formatted disease information
    """
    remedy = get_remedy(disease_name)
    if not remedy:
        return "Disease information not found"
    
    info = f"Disease: {remedy['disease_name']}\n"
    info += f"Plant: {remedy['plant']}\n"
    info += f"Severity: {remedy['severity']}\n"
    info += f"\nSymptoms:\n"
    for symptom in remedy['symptoms']:
        info += f"  • {symptom}\n"
    
    info += f"\nOrganic Treatment:\n"
    for treatment in remedy['organic_treatment']:
        info += f"  • {treatment}\n"
    
    info += f"\nChemical Treatment:\n"
    if remedy['chemical_treatment']:
        for treatment in remedy['chemical_treatment']:
            info += f"  • {treatment}\n"
    else:
        info += "  • No chemical treatment available (viral disease)\n"
    
    info += f"\nPrevention:\n"
    for prevention in remedy['prevention']:
        info += f"  • {prevention}\n"
    
    return info
