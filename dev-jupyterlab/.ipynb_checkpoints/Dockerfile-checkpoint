FROM python:3.9-alpine
ADD aaa_monitor.py .
RUN pip install slack_sdk requests flask bs4
CMD [“python”, “./aaa_monitor.py”]