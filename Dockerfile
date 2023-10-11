FROM python:3.11.4

WORKDIR /pap
COPY PapPack /pap
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 13956

CMD ["/bin/bash", "/pap/pap.sh"]
