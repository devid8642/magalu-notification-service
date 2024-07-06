from fastapi import FastAPI


app = FastAPI(version='0.1.0', title='Magalu Notification API')


@app.get('/')
def root():
    return {'message': 'Hello, Magalu!'}
