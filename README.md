<!-- setup frontend -->
# Start frontend app
cd frontend
npm install
npm run dev

<!-- Backend1 (Node.js Auth API) -->
# Start backend1 
cd backend1
npm install
node app.js

# Start backend2
cd backend2
pip install -r requirements.txt
python -m uvicorn main:app --reload
