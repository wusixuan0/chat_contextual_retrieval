### Get Started
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Plan
considerations:
1. separators=["\n\nHuman:", "\n\nAssistant:"] # Preserve turn boundaries

### Evaluation
manual evaluate retrieved result
todo

### project structure
```
/
├── src/                    # Core application code
│   ├── __init__.py
│   ├── vector_store/
│   │   ├── __init__.py
│   │   └── vector_db.py
│   └── embed/
│       ├── __init__.py
│       └── rag_engine.py
├── data/                 # Application data (in memory vector DB, chat history)
│   ├── chat.json
├── requirements.txt
├── .env
└── main.py
```

```
import pdb; pdb.set_trace()
```