# K1S
- https://hub.docker.com/_/httpd 

# BUILD
```bash
$ docker build -t my-apache2 .
```

# RUN
```bash
$ docker run -dit --name my-running-app -p 8080:80 my-apache2
```

# 컨테이너 접속
```bash
$ docker exec -it my-apache2 bash
```

