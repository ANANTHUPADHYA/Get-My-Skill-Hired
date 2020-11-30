# HireMyServices

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 10.1.3.

## Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The app will automatically reload if you change any of the source files.

## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory. Use the `--prod` flag for a production build.

## Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via [Protractor](http://www.protractortest.org/).

## Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI README](https://github.com/angular/angular-cli/blob/master/README.md).


## Deploy to EC2

### Install and configure Nginx

https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-18-04-quickstart

  create nginx config ```sudo nano /etc/nginx/sites-available/hms ```
  
  ```
  upstream hms{
    server 127.0.0.1:8000;
}

upstream ui{
    server 127.0.0.1:4200;
}


server{
   listen 443;
   listen 80;
   server_name 18.209.223.190;
   client_max_body_size 10M;

location / {
        include proxy_params;
        add_header Access-Control-Allow-Origin *;
         #proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP ip_address;
        proxy_pass http://ui;
        #proxy_pass http://unix:/home/ubuntu/hms/hms.sock;
  }

location /api/ {
        include proxy_params;
        add_header Access-Control-Allow-Origin *;
	 #proxy_pass http://127.0.0.1:8000;
	proxy_set_header Host $host;
	proxy_set_header X-Real-IP ip_address;	
        proxy_pass http://hms;
        #proxy_pass http://unix:/home/ubuntu/hms/hms.sock;
  }
}
```

### Test nginx config
``` sudo nginx -t```

### Restart nginx
```sudo systemctl restart nginx```

### Check status
```sudo systemctl status nginx```

## Issue on running ```ng serve``` on aws EC2 t2.micro instance
https://github.com/angular/angular/issues/21035

### Solution

```
sudo /bin/dd if=/dev/zero of=/var/swap.1 bs=1M count=1024
sudo /sbin/mkswap /var/swap.1
sudo chmod 600 /var/swap.1
sudo /sbin/swapon /var/swap.1
```

```ng build --prod --build-optimizer=false```

## Running UI and Backend in background

``` 
cd <project dir>

nohup python3 flask_app.py > log.txt 2>&1 &
```

``` 
cd <project dir>/UI/hire-my-services

nohup ng serve > log.txt 2>&1 &
```

## List running processes
``` ps -aux | grep flask_app.py```
