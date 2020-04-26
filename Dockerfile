FROM python:3

RUN pip install jupytext --upgrade
ADD ./src/entrypoint.py /entrypoint.py
ENTRYPOINT ["python", "/src/entrypoint.py"]
