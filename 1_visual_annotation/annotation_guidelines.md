# Product Image Annotation Guidelines v1.0

## 1. Objective

Annotate product images with bounding boxes for e-commerce catalog automation.

## 2. Classes

| Class            | Definition                   | Example             |
| ---------------- | ---------------------------- | ------------------- |
| `main_product`   | Primary product in the image | Dress on model      |
| `secondary_item` | Secondary items              | Bag, shoes, jewelry |
| `background`     | Non-product elements         | Furniture, plants   |
| `packaging`      | Elements of packaging        | Box, packet, bag    |

## 3. Bounding Box Rules

### 3.1 General Rules

- Draw TIGHT boxes around objects (max 5px padding)
- Include partially visible objects (>30% visible)
- Exclude objects <10% of image area

### 3.2 Background annotations

- Annotate background ONLY if prominent decorative element
- Skip background if >50% of image area
- Examples: flowers, furniture, props

### 3.3 Positive Examples 🟢

```
[Image 1] Dress on model
- Box covers entire dress including sleeves
- Tight fit, minimal background included
- Labeled as `product_main`
```

### 3.4 Negative Examples 🔴

```
[Image 2] Same dress
- Box cuts off part of dress
- Too much padding (>10px)
- Wrong class label
```

## 4. Edge Cases

### 4.1 Overlapping Products

**Rule**: Each product gets separate box, overlaps allowed

```
Example: Necklace over dress
- Box 1: Full dress (`product_main`)
- Box 2: Necklace only (`product_accessory`)
```

### 4.2 Reflections/Shadows

**Rule**: Include if product feature, exclude if artifact

### 4.3 Partially Visible

**Rule**: Annotate if >30% visible AND identifiable

```
Example: Bag partially cut off
- >30% visible → Annotate
- <30% visible → Skip
```

## 5. Conflict Resolution

1. When in doubt, choose the MORE INCLUSIVE option
2. Flag uncertain cases with `needs_review` tag
3. Escalate to senior annotator if unresolved after 2 attempts

## 6. Quality Criteria

- IoU (Intersection over Union) > 0.7 with ground truth
- Class accuracy > 95%
- No missing objects >10% of image area
