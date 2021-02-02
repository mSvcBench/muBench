FROM python:slim
COPY . /app
WORKDIR /app
RUN apt update
RUN apt install -y screen vim ssh
RUN pip install -r requirements.txt

# Debug
RUN apt -y install openssh-server iproute2 vim curl
COPY id_rsa.pub /root/.ssh/authorized_keys
EXPOSE 22
# End debug


CMD [ "/bin/bash", "./start.sh"]

EXPOSE 8080