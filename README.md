### Hi there

To execute this project in local
1. Clone this project
2. Go the the project directory
#### to run this Execute following commands in your terminal
1. To create Virutal Env
``` bash
virtualenv venv
```
2. Activate Virtual Env
```
venv\scripts\activate
```
3. Install dependencies
```
pip install -r requirements.txt
```
4. run the app
```
uvicorn product.main:app
```
5. visit http://localhost:8000/docs to see the api docs and can test api as well