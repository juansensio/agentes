## Minimal Architecture Design

### **Single Agent Flow**

```
Business Idea Input
        ↓
Keyword Agent
        ↓
Keywords + Questions
```

### **Agent Specification**

#### **Keyword Agent**
- **Input**: Business idea description
- **Process**: 
  - Generate relevant keywords
  - Generate related questions
- **Output**: 
  - List of keywords
  - List of questions

### **Output Structure**

Simple JSON output:
```json
{
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "questions": ["question1", "question2", "question3"]
}
```

### **Example**

**Input**: "SaaS for invoice automation"

**Output**:
```json
{
  "keywords": ["invoice automation", "automated invoicing", "invoice software", "billing automation"],
  "questions": ["How to automate invoice processing?", "What is the best invoice automation software?", "Why automate invoicing?"]
}
```

That's it. Simple and focused.