# 3-dbs
This project will be done by ale guevara and Santiago Montes de Oca
 the plan is having one huge python file that connectst to the 3 dbs.

 so we will write the whol process and documentation here, so lets gooo.

dependencies
model -> routes / client
routes -> client
client -> routes

## mongo db
```bash
# Install project python requirements
pip install -r requirements.txt

#run the api service
python -m uvicorn main:app --reload

#ensure you have a mongo db instance
docker run --name mongodb -d -p 27017:27017 mongo

#script to populate
missing

```

## final command
```bash
#run the main file

python main.py

```