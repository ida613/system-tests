
FROM datadog/dd-trace-ci:php-8.2_buster
WORKDIR /tmp
ENV DD_TRACE_CLI_ENABLED=1
ADD utils/build/docker/php/parametric/composer.json .
ADD utils/build/docker/php/parametric/composer.lock .
ADD utils/build/docker/php/parametric/server.php .
ADD utils/build/docker/php/parametric/install.sh .
COPY binaries /binaries
RUN ./install.sh
RUN composer install
