# 3-dbs
This project will be done by ale guevara and Santiago Montes de Oca
 the plan is having one huge python file that connectst to the 3 dbs.

 so we will write the whol process and documentation here, so lets gooo.

 i use python 3.10 yep

## Requierements
realistically, we didnt add anything special, s you should be able to run it without these, but in case you are building it in a virtual env, here they are
```bash
cd requierments/
pip install -r cass_req.txt
pip install -r dgraph_req.txt
pip install -r mongo_req.txt
```
## installign docker dbs
first off, please dont run **RATEL**, because as it is exposed to port 8000, and so is mongodb, so mongo db wont work if you try so.

```bash
#dgraph
docker run --name dgraph -d -p 8080:8080 -p 9080:9080 dgraph/standalone:latest
#mongo
docker run --name mongodb -d -p 27017:27017 mongo
#cassandra + 
docker run --name node01 -p 9042:9042 -d cassandra
```
## you should be able to just **runTheApp.py**

    that is all, the unicorn for mongo db should open automatically in a terminal, i dont think i wll give you problems.
```bash
#run the main file

python TheApp.py

```

## if you are trying to understand the code, good luck

all i can say is that the transition towards integrating everything towards one document was not smotth, and some of the files that we in charge of a single database still exist even though they are redundant.
<br><br> though in fear of messing somethign up, i will not modify it.

## conclusions on the work

time managment was our downfall, there were lots of proyects this last week, and some assumptions we made that were already complete, were not, which in turn led to some areas missing.
<br><br>
also i struggled enourmously with mongo db, which my fellow clasmates did not, which is really weird. also i didnt want to do mongo, and i got that port, so yeah.

## final command
```bash
#run the main file

python TheApp.py

```



# further down are comments for myself
## mongo db || commands that might be useful.
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

