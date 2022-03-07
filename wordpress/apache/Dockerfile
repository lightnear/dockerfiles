FROM wordpress:apache

LABEL maintainer="lightnear<lightnear@qq.com>"

ENV TZ=Asia/Shanghai
ENV LANG en_US.utf8

RUN set -ex; \
    apt-get update; \
    apt-get -y upgrade; \
    apt-get -y install tzdata; \
    ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime; \
    echo ${TZ} > /etc/timezone; \
    dpkg-reconfigure --frontend noninteractive tzdata; \
    apt-get -y install locales; \
    localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8; \
    apt-get -y autoremove; \
    apt-get -y clean;

# optimize php.ini
RUN set -ex; \
    mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"; \
    { \
    echo "max_input_vars = 5000"; \
    echo "max_execution_time = 300"; \
    echo "memory_limit = 512M"; \
    echo "post_max_size = 50M"; \
    echo "upload_max_filesize = 50M"; \
    echo "date.timezone = Asia/Shanghai"; \
    } > $PHP_INI_DIR/conf.d/php_newspaper.ini

# RUN set -ex; \
#     sed -i -e 's/listen = 127.0.0.1:9000/listen = 9000/' /usr/local/etc/php-fpm.d/www.conf; \
#     sed -i -e 's/pm.max_children.*/pm.max_children = 10/' /usr/local/etc/php-fpm.d/www.conf; \
#     sed -i -e 's/pm.start_servers.*/pm.start_servers = 3/' /usr/local/etc/php-fpm.d/www.conf; \
#     sed -i -e 's/pm.min_spare_servers.*/pm.min_spare_servers = 1/' /usr/local/etc/php-fpm.d/www.conf; \
#     sed -i -e 's/pm.max_spare_servers.*/pm.max_spare_servers = 3/' /usr/local/etc/php-fpm.d/www.conf;

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["apache2-foreground"]
