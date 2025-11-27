# AI-Procure ML Service

ML module for the AI-Procure system.  
The service performs three main tasks:

- Extract data from text (extract)
- Search for similar suppliers (match)
- Risk analysis

The service is written in **Python + FastAPI** and runs inside **Docker**.

---

## 📦 Technology stack

- Python 3.11
- FastAPI
- Uvicorn
- Pandas / NumPy
- Machine Learning models (joblib)
- Docker

---

# 🚀 Launching without Docker

Install Dependencies:

```bash
pip install -r requirements.txt


start the server
uvicorn app.main:app --host 0.0.0.0 --port 8000

documentation is available at 
http://127.0.0.1:8000/docs
```

, Launching via Docker

Assemble an image 
docker build -t ml_service_app .

Launch
the docker container run -p 8000:8000 ml_service_app

if needed in the background
, docker run -d -p 8000:8000 --name ml_service ml_service_app
    
view logs 
docker logs -f ml_service




Health check
http://127.0.0.1:8000/docs


check using curl 
curl http://127.0.0.1:8000/health


Useful Docker Commands

delete
the docker rm -f ml_service container

rebuild
the docker build image -t ml_service_app .

go inside the container 
docker exec -it ml_service bash





P.S:
the start of application can take some time be patient!