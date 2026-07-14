FROM mysql:8.0

ENV MYSQL_DATABASE=news_app
ENV TZ=Asia/Shanghai

COPY my.cnf /etc/mysql/conf.d/custom.cnf
COPY init.sql /docker-entrypoint-initdb.d/

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone