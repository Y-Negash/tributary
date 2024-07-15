FROM python:3.11
COPY ./entrypoint.py .
CMD python entrypoint.py