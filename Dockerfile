FROM --platform=linux/amd64 python:3.8-slim-buster as build

ENV PATH /root/.local/bin/:$PATH

WORKDIR /app

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install gcc 
RUN apt-get -y install libpq-dev

#libpq postgresql-dev  libc-dev postgresql-libs libgssapi_krb5
#RUN apt-get install  build-base linux-headers pcre-dev

#RUN apk add libpq-dev && rm -rf /var/lib/apt/lists/*
#RUN apk add python3-dev

COPY requirements.txt ./

#RUN pip install pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org wheel --upgrade distribute
#RUN pip install  pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org gdal

RUN pip install  --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org --upgrade setuptools --timeout 60
RUN python3 -m pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org --upgrade pip --timeout 60
RUN pip install  --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt 
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org --upgrade pip --timeout 60
RUN pip install --user  --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org gevent --pre --timeout 600
RUN pip install --user  --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org  auto-py-to-exe --timeout 60
RUN pip install --user  --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org flask_sqlalchemy --timeout 60
RUN pip install --user  --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org passlib --timeout 60
RUN pip install --user  --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org flask_login --timeout 60
RUN pip install --user  --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org psycopg2-binary --timeout 60
RUN pip install --user  --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org wheel --timeout 60
RUN pip install --user  --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org uwsgi flask --timeout 60
RUN pip install --user  --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org flask_restful --timeout 60

#COPY uwsgi.ini /usr/local/bin/uwsgi
#RUN chmod a+x /usr/local/bin/uwsgi
#RUN chmod a+x /root/.local/bin/uwsgi

COPY . .
 
EXPOSE 4000
#CMD [   "tail" ,"-f","/dev/null"   ]
CMD ["uwsgi", "--ini", "/app/uwsgi.ini"]

 