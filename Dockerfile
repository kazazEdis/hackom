FROM python:3

WORKDIR /app

COPY . /app
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN grep -q -o 'avx[^ ]*' /proc/cpuinfo || pip install dependecies/tensorflow-2.10.0-no-AVX.whl

EXPOSE 8080

ENTRYPOINT [ "uwsgi" ]

CMD ["uwsgi-config.ini"]