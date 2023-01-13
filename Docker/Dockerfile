from python:3.8.16-slim-buster

RUN apt update

# muBench software
WORKDIR /root
RUN apt install -y git --no-install-recommends
RUN git clone https://github.com/mSvcBench/muBench.git
RUN pip3 install -r muBench/requirements.txt

# kubectl
RUN mkdir /etc/apt/keyrings
RUN apt install -y ca-certificates curl bash-completion --no-install-recommends
RUN curl -fsSLo /etc/apt/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
RUN echo "deb [signed-by=/etc/apt/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" > /etc/apt/sources.list.d/kubernetes.list
RUN apt update
RUN apt install -y kubectl

# kubectl autocomplete
RUN apt install -y bash-completion --no-install-recommends 
RUN echo "source /usr/share/bash-completion/bash_completion" >> .bashrc
RUN echo 'source <(kubectl completion bash)' >>~/.bashrc
RUN  echo 'alias k=kubectl' >>~/.bashrc
RUN  echo 'complete -o default -F __start_kubectl k' >>~/.bashrc

# heml
RUN apt install -y gpg
RUN curl https://baltocdn.com/helm/signing.asc | gpg --dearmor > /usr/share/keyrings/helm.gpg
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" > /etc/apt/sources.list.d/helm-stable-debian.list
RUN apt update
RUN apt install -y helm

# welcome message
COPY welcome.sh /etc/profile.d
RUN chmod a+rx /etc/profile.d/welcome.sh
RUN echo "/etc/profile.d/welcome.sh" >> .bashrc

RUN mkdir /root/.kube

CMD [ "sleep", "infinity"]


