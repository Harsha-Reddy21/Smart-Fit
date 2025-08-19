# Smart-Fit (Minimal)
1) Ingest data
```
cd backend
python rag\ingest_data.py
```

2) Backend 
```
cd backend
uvicorn main:app --reload
```

3) Frontend
```
streamlit run frontend/app.py
```

API highlights:
- POST /auth/register
- POST /auth/login
- GET /auth/user/{user_id}
- CRUD: /exercises, /workouts, /nutrition, /progress
- Chat: POST /chat/ask, GET /chat/history/{user_id}

