FROM python:3.8

RUN pip install --upgrade setuptools
RUN pip install cython
RUN pip install numpy
RUN pip install pandas
RUN pip install matplotlib
RUN pip install pystan
RUN pip install fbprophet
RUN pip install prophetable

RUN mkdir -p /home/project/pm
WORKDIR /home/project/pm
COPY . /home/project/pm

ENTRYPOINT [ "python", "docker/run.py" ]