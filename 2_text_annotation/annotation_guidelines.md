# User Intent Classification Guidelines v1.0

## 1. Objective

Classify user messages into intents for chatbot training.

## 2. Intent Classes

| Intent              | Definition                         | Trigger Words                           |
| ------------------- | ---------------------------------- | --------------------------------------- |
| `billing_inquiry`   | Questions about payments, invoices | "charge", "invoice", "payment", "bill"  |
| `technical_support` | Technical issues with website      | "error", "not working", "bug", "broken" |
| `feature_request`   | Asking for new features            | "would be nice", "can you add", "wish"  |
| `cancellation`      | Want to cancel service             | "cancel", "stop", "unsubscribe"         |
| `general_question`  | Other inquiries                    | None of above                           |

## 3. Annotation Rules

### 3.1 Single Intent per Message

Choose the PRIMARY intent even if multiple present.

**Example**:

```
"I want to cancel because the payment system is broken"
- Primary: `cancellation` (main goal)
- Secondary: `technical_support` (reason)
→ Label: `cancellation`
```

### 3.2 Confidence Levels

- **High**: Clear intent, obvious keywords
- **Medium**: Intent likely but ambiguous
- **Low**: Multiple interpretations possible

## 4. Edge Cases

### 4.1 Sarcasm/Irony

```
"Oh great, another bug!"
→ Intent: `technical_support`
→ Sentiment: negative
→ Confidence: high
```

### 4.2 Implicit Intent

```
"My website has been down for 3 days"
→ Intent: `technical_support` (implied complaint)
→ NOT `general_question`
```

### 4.3 Multi-turn Context

```
Previous: "How much is premium plan?"
Current: "That's too expensive"
→ Intent: `billing_inquiry` (continues previous topic)
```

## 5. Quality Checks

- Inter-annotator agreement > 85%
- Label all messages (no skips)
- Flag ambiguous cases for review
