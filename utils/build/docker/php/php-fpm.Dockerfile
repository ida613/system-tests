
FROM ubuntu:20.04

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata

RUN printf '#!/bin/sh\n\nexit 101\n' > /usr/sbin/policy-rc.d && \
	chmod +x /usr/sbin/policy-rc.d && \
	apt-get install -y curl apache2 libapache2-mod-fcgid software-properties-common \
	&& rm -rf /var/lib/apt/lists/* && \
	rm -rf /usr/sbin/policy-rc.d

RUN add-apt-repository ppa:ondrej/php -y && apt-get update

ARG PHP_VERSION=8.0
RUN apt-get install -y php8.0-fpm

RUN find /var/www/html -mindepth 1 -delete
RUN echo '<?php phpinfo();' > /var/www/html/index.php
RUN echo '<?php echo "OK";' > /var/www/html/sample_rate_route.php
RUN echo '<?php echo "Hello, WAF!";' > /var/www/html/waf.php
RUN echo '<?php http_response_code(404);' > /var/www/html/404.php
RUN a2enmod rewrite

ADD utils/build/docker/php/php-fpm/php8.0-fpm.conf /etc/apache2/conf-available/
ADD utils/build/docker/php/common/php.ini /etc/php/8.0/fpm/php.ini

RUN a2enconf php8.0-fpm
RUN a2enmod proxy
RUN a2enmod proxy_fcgi

ENV DD_TRACE_ENABLED=1
ENV DD_TRACE_GENERATE_ROOT_SPAN=1
ENV DD_TRACE_AGENT_FLUSH_AFTER_N_REQUESTS=0
ENV DD_TRACE_DEBUG=1
ENV DD_APPSEC_ENABLED=1
ENV DD_TRACE_SAMPLE_RATE=1
ENV DD_TAGS='key1:val1, key2 : val2 '
ENV DD_APPSEC_TRACE_RATE_LIMIT=0

RUN curl -Lf -o /tmp/dumb_init.deb https://github.com/Yelp/dumb-init/releases/download/v1.2.5/dumb-init_1.2.5_amd64.deb && \
	dpkg -i /tmp/dumb_init.deb && rm /tmp/dumb_init.deb

RUN sed -i s/80/7777/ /etc/apache2/ports.conf
EXPOSE 7777/tcp

ARG TRACER_VERSION=latest
ARG APPSEC_VERSION=latest
ADD binaries* /binaries/
ADD utils/build/docker/php/common/install_ddtrace.sh /
RUN /install_ddtrace.sh

ADD utils/build/docker/php/php-fpm/entrypoint.sh /

WORKDIR /binaries
ENTRYPOINT ["dumb-init", "/entrypoint.sh"]