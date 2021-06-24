FROM nginx

# 추후 ps -ef | grep nginx로 pid 확인하기 위해서
RUN apt-get update
RUN apt-get install -y procps

# error.log, access.log 파일 여부에 따라서 파일 생성

RUN rm /etc/nginx/conf.d/default.conf

# COPY nginx.conf /etc/nginx/conf.d/
COPY nginx.conf /etc/nginx/
# COPY default.conf /etc/nginx/conf.d/
# CMD ["nginx", "-g", "daemon off;"]