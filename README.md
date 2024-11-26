# 3-dbs
This project will be done by ale guevara and Santiago Montes de Oca
 the plan is having one huge python file that connectst to the 3 dbs.

 so we will write the whol process and documentation here, so lets gooo.

 i use python 3.10 yep

dependencies
model -> routes / client
routes -> client
client -> routes

## mongo db
```bash
# Install project python requirements
pip install -r requirements.txt

#run the api service
cd .\mongoDB\
python -m uvicorn main:app --reload

#ensure you have a mongo db instance
docker run --name mongodb -d -p 27017:27017 mongo
#if you wanna see whats going on inside
docker exec -it mongodb mongosh
use iteso
db.posts.find({})

#script to populate
cd .\data\mongoData\
python .\populate.py

#testing crud funcs xd
cd ../../mongoDB/
python client.py posts list #should return all posts registered
python client.py posts get -i 67425ba682034efeb71f673e

#how can we choose to do a query request
python client.py posts get -p visibility_status+friends
python client.py posts get -p visibility_status+friends user_id+0x55
python client.py posts get -p visibility_status+private

#tryng put
python client.py posts update -i 67425ba682034efeb71f673e -p likes+100

#trying delete
python client.py posts delete -i 67425bba82034efeb71f6748 

```

## final command
```bash
#run the main file

python main.py

```











things i have yet to do:
- when egtting all elements, for some reason, it doesnt return all the elements ids, i dont know why?
- we are not gonna be able to update comments, i left the m there for the posibility of agregation pipelines