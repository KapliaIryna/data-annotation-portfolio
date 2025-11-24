# Annotation Validation Script - Validates annotation quality for visual and text datasets

import json
import sys

def validate_visual_annotations(json_file):
    """
    Validate bounding box annotations from COCO JSON format.
    
    Args:
        json_file: Path to COCO format JSON file
    
    Returns:
        dict: Validation results with issues found
    """
    print("-" * 40)
    print("VISUAL ANNOTATION VALIDATION")
    print("-" * 40)
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {json_file}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format")
        return None
    
    images = data.get('images', [])
    annotations = data.get('annotations', [])
    categories = data.get('categories', [])
    
    print(f"\nDataset Overview:")
    print(f"   Images: {len(images)}")
    print(f"   Annotations: {len(annotations)}")
    print(f"   Categories: {len(categories)}")
    
    issues = []
    
    # Check 1: Valid bbox coordinates
    print("\nCheck 1: Bounding Box Validation")
    print("-" * 40)
    
    for ann in annotations:
        bbox = ann.get('bbox', [])
        image_id = ann.get('image_id')
        ann_id = ann.get('id')
        
        if len(bbox) != 4:
            issues.append(f"Invalid bbox format in annotation {ann_id}")
            continue
        
        x, y, w, h = bbox
        
        # Check if width/height are positive
        if w <= 0 or h <= 0:
            issues.append(f"Annotation {ann_id}: Invalid bbox dimensions (w={w}, h={h})")
        
        # Check if bbox is within image bounds
        img = next((img for img in images if img['id'] == image_id), None)
        if img:
            if x < 0 or y < 0:
                issues.append(f"Annotation {ann_id}: Negative coordinates (x={x}, y={y})")
            
            if x + w > img['width'] or y + h > img['height']:
                issues.append(f"Annotation {ann_id}: Bbox exceeds image bounds")
    
    # Check 2: Small objects (potential annotation errors)
    print("\nCheck 2: Small Object Detection")
    print("-" * 40)
    
    small_objects = []
    for ann in annotations:
        area = ann.get('area', 0)
        img_id = ann.get('image_id')
        img = next((img for img in images if img['id'] == img_id), None)
        
        if img:
            img_area = img['width'] * img['height']
            relative_area = (area / img_area) * 100
            
            if relative_area < 1:  # Less than 1% of image
                small_objects.append({
                    'id': ann['id'],
                    'image_id': img_id,
                    'area_percent': relative_area
                })
    
    if small_objects:
        print(f"Found {len(small_objects)} very small objects (<1% of image)")
        print(f"Examples:")
        for obj in small_objects[:3]:
            print(f"      - Annotation {obj['id']}: {obj['area_percent']:.2f}% of image")
    else:
        print("No unusually small objects found")
    
    # Check 3: Large background boxes
    print("\nCheck 3: Large Background Boxes")
    print("-" * 40)
    
    large_boxes = []
    background_cat_id = None
    
    # Find background category
    for cat in categories:
        if 'background' in cat['name'].lower():
            background_cat_id = cat['id']
            break
    
    if background_cat_id:
        for ann in annotations:
            if ann['category_id'] == background_cat_id:
                img_id = ann['image_id']
                img = next((img for img in images if img['id'] == img_id), None)
                
                if img:
                    img_area = img['width'] * img['height']
                    relative_area = (ann['area'] / img_area) * 100
                    
                    if relative_area > 50:  # More than 50% of image
                        large_boxes.append({
                            'id': ann['id'],
                            'image_id': img_id,
                            'area_percent': relative_area
                        })
        
        if large_boxes:
            print(f"Found {len(large_boxes)} large background boxes (>50% of image)")
            for box in large_boxes[:3]:
                print(f"      - Annotation {box['id']}: {box['area_percent']:.1f}% of image")
        else:
            print("No oversized background boxes found")
    
    # Check 4: Missing annotations
    print("\nCheck 4: Annotation Coverage")
    print("-" * 40)
    
    images_without_annotations = []
    for img in images:
        img_anns = [ann for ann in annotations if ann['image_id'] == img['id']]
        if len(img_anns) == 0:
            images_without_annotations.append(img['id'])
    
    if images_without_annotations:
        print(f"{len(images_without_annotations)} images have no annotations")
    else:
        print(f"All images have at least one annotation")
    
    # Summary
    print("\n" + "-" * 40)
    print("VALIDATION SUMMARY")
    print("-" * 40)
    
    if len(issues) == 0:
        print("No critical issues found!")
    else:
        print(f"Found {len(issues)} issues:")
        for issue in issues[:5]:
            print(f"   - {issue}")
        if len(issues) > 5:
            print(f"   ... and {len(issues) - 5} more")
    
    results = {
        'total_images': len(images),
        'total_annotations': len(annotations),
        'critical_issues': len(issues),
        'small_objects': len(small_objects),
        'large_backgrounds': len(large_boxes),
        'images_without_annotations': len(images_without_annotations)
    }
    
    return results


def validate_text_annotations(csv_file):
    """
    Validate text annotation consistency.
    
    Args:
        csv_file: Path to annotated texts CSV
    
    Returns:
        dict: Validation results
    """
    print("\n" + "-" * 40)
    print("TEXT ANNOTATION VALIDATION")
    print("-" * 40)
    
    try:
        import pandas as pd
        df = pd.read_csv(csv_file)
    except ImportError:
        print("Error: pandas not installed. Run: pip install pandas")
        return None
    except FileNotFoundError:
        print(f"Error: File not found: {csv_file}")
        return None
    
    print(f"\nDataset Overview:")
    print(f"   Total annotations: {len(df)}")
    
    # Check 1: Required columns
    print("\nCheck 1: Required Columns")
    print("-" * 40)
    
    required_cols = ['id', 'text', 'intent', 'confidence']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        print(f"Missing columns: {missing_cols}")
    else:
        print(f"All required columns present")
    
    # Check 2: Empty values
    print("\n🔍 Check 2: Empty Values")
    print("-" * 40)
    
    empty_counts = df.isnull().sum()
    if empty_counts.sum() > 0:
        print("Found empty values:")
        for col, count in empty_counts[empty_counts > 0].items():
            print(f"      - {col}: {count} empty")
    else:
        print("No empty values found")
    
    # Check 3: Intent distribution
    print("\nCheck 3: Intent Distribution")
    print("-" * 40)
    
    intent_counts = df['intent'].value_counts()
    print(f"   Intents found: {len(intent_counts)}")
    for intent, count in intent_counts.items():
        percentage = (count / len(df)) * 100
        print(f"      - {intent}: {count} ({percentage:.1f}%)")
    
    # Check for imbalance
    max_count = intent_counts.max()
    min_count = intent_counts.min()
    if max_count / min_count > 3:
        print(f"Class imbalance detected (ratio: {max_count/min_count:.1f}:1)")
    else:
        print(f"Balanced distribution")
    
    # Check 4: Confidence levels
    print("\nCheck 4: Confidence Levels")
    print("-" * 40)
    
    confidence_counts = df['confidence'].value_counts()
    for conf, count in confidence_counts.items():
        percentage = (count / len(df)) * 100
        print(f"      - {conf}: {count} ({percentage:.1f}%)")
    
    low_confidence = len(df[df['confidence'] == 'low'])
    if low_confidence > len(df) * 0.1:
        print(f"High number of low confidence annotations ({low_confidence})")
    
    results = {
        'total_annotations': len(df),
        'unique_intents': len(intent_counts),
        'empty_values': int(empty_counts.sum()),
        'low_confidence_count': low_confidence
    }
    
    return results


if __name__ == "__main__":
    print("\n" + "-" * 40)
    print("DATA ANNOTATION VALIDATION TOOL")
    print("-" * 40)
    
    # HARDCODED шляхи (найнадійніше)
    visual_file = r'/Users/irinakapla/Documents/Learning/projects/data-annotation-portfolio/1_visual_annotation/_annotations.coco.json'
    text_file = r'/Users/irinakapla/Documents/Learning/projects/data-annotation-portfolio/2_text_annotation/data/annotated_texts.csv'
    
    print(f"\nФайли:")
    print(f"   Visual: {visual_file}")
    print(f"   Text: {text_file}")
    
    # Validate visual annotations
    visual_results = None
    try:
        visual_results = validate_visual_annotations(visual_file)
    except Exception as e:
        print(f"Помилка при валідації візуальних анотацій: {e}")
    
    # Validate text annotations
    text_results = None
    try:
        text_results = validate_text_annotations(text_file)
    except Exception as e:
        print(f"Помилка при валідації текстових анотацій: {e}")
    
    print("\n" + "-" * 40)
    print("OVERALL VALIDATION COMPLETE")
    print("-" * 40)
    
    if visual_results:
        print(f"\nVisual Annotations:")
        print(f"   Critical issues: {visual_results['critical_issues']}")
        print(f"   Small objects: {visual_results['small_objects']}")
        print(f"   Large backgrounds: {visual_results['large_backgrounds']}")
    
    if text_results:
        print(f"\nText Annotations:")
        print(f"   Total: {text_results['total_annotations']}")
        print(f"   Unique intents: {text_results['unique_intents']}")
        print(f"   Low confidence: {text_results['low_confidence_count']}")
    
    print("\nValidation complete!")