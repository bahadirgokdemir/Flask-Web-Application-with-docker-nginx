FROM nginx:latest

RUN apt-get update && apt-get install -y \
    git \
    apt-utils\
    wget\
    zlib1g-dev\
    build-essential \
    libpcre3-dev \
    libxml2-dev \
    libcurl4-openssl-dev \
    libgeoip-dev \
    libyajl-dev \
    liblmdb-dev \
    libssl-dev \
    apache2-dev \
    automake \
    autoconf \
    libtool

# ModSecurity'i derleme işlemleri
RUN git clone --depth 1 -b v3/master --single-branch https://github.com/SpiderLabs/ModSecurity
RUN cd ModSecurity && ./build.sh && git submodule init && git submodule update && ./build.sh && ./configure && make && make install && cd ..

# ModSecurity için Nginx 
RUN git clone --depth 1 https://github.com/SpiderLabs/ModSecurity-nginx.git
RUN wget http://nginx.org/download/nginx-1.25.2.tar.gz
RUN tar zxvf nginx-1.25.2.tar.gz
RUN cd nginx-1.25.2 && ./configure --with-compat --add-dynamic-module=../ModSecurity-nginx &&  make modules &&  cp objs/ngx_http_modsecurity_module.so /etc/nginx/modules && cd ..
#RUN cd ModSecurity-nginx && git submodule init && git submodule update

#RUN load_module modules/ngx_http_modsecurity_module.so; 
RUN mkdir /etc/nginx/modsec && wget -P /etc/nginx/modsec/ https://raw.githubusercontent.com/SpiderLabs/ModSecurity/v3/master/modsecurity.conf-recommended && mv /etc/nginx/modsec/modsecurity.conf-recommended /etc/nginx/modsec/modsecurity.conf
# ModSecurity ve Nginx yapılandırmalarını kopyalama
#COPY nginx.conf /etc/nginx/nginx.conf
#COPY /modsecurity/modsecurity.conf /etc/nginx/modsecurity/modsecurity.conf
#COPY /modsecurity/rules /etc/nginx/modsecurity/rules
RUN cp ModSecurity/unicode.mapping /etc/nginx/modsec
RUN sed -i 's/SecRuleEngine DetectionOnly/SecRuleEngine On/' /etc/nginx/modsec/modsecurity.conf

EXPOSE 80
#CMD [   "tail" ,"-f","/dev/null"   ]
CMD ["nginx", "-g", "daemon off;"]
