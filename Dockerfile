FROM nicolaka/netshoot:v0.11

RUN python3 -m pip install -U pip

COPY --chown=root:root requirements.txt /opt/requirements.txt
RUN pip3 install -r /opt/requirements.txt

WORKDIR /app
COPY . .

EXPOSE 8000

CMD "python3" "-m" "app.main"
