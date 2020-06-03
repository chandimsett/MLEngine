FROM python:3.6
WORKDIR /ml_webservice/prediction_engine/
COPY requirements.txt /ml_webservice/prediction_engine/
RUN pip install -r requirements.txt  --index-url https://pypi.org/simple/  --extra-index-url http://192.168.0.104:8081/repository/python-repo/simple --trusted-host 192.168.0.104
RUN pip install common_utils  --index-url https://pypi.org/simple/  --extra-index-url http://192.168.0.104:8081/repository/python-repo/simple --trusted-host 192.168.0.104
COPY prediction_engine /ml_webservice/prediction_engine/
EXPOSE 8080
ENTRYPOINT python3.6 ./app.py
