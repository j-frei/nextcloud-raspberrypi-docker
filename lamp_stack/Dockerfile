FROM php:7.4-apache

# Setup system environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Add UTF-8 as default language encoding
# RUN locale-gen en_US.UTF-8
RUN apt-get update && apt-get install -y locales

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/de_DE.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LC_ALL="de_DE.UTF-8"
ENV LANG="de_DE.UTF-8"
ENV LANGUAGE="de_DE.UTF-8"
RUN locale-gen "de_DE.UTF-8"

# Adjust timezone
RUN ln -fs /usr/share/zoneinfo/Europe/Berlin /etc/localtime

# php zip
RUN apt-get install -y \
        zlib1g-dev \
        libzip-dev \
        libonig-dev \
        zip
RUN docker-php-ext-install zip

# php mbstring
RUN apt-get install -y --no-install-recommends \
        libonig-dev        
RUN docker-php-ext-install mbstring

# Freetype-supported php-gd
RUN apt-get install -y --no-install-recommends \
        libwebp-dev \
        libjpeg62-turbo-dev \
        libpng-dev \
        libxpm-dev \
        libfreetype6-dev
RUN docker-php-ext-configure gd \
        --with-jpeg \
        --with-freetype
RUN docker-php-ext-install gd

# php-postgres
RUN apt-get install -y --no-install-recommends \
        libpq-dev
RUN docker-php-ext-install pdo_pgsql

# php intl
RUN apt-get install -y  --no-install-recommends \
        libicu-dev
RUN docker-php-ext-configure intl
RUN docker-php-ext-install intl

# php bcmath
RUN docker-php-ext-install bcmath

# php gmp
RUN apt-get install -y --no-install-recommends \
        libgmp-dev
RUN docker-php-ext-install gmp

# php imagick
RUN apt-get install -y --no-install-recommends \
         libmagickwand-dev
RUN pecl install imagick
RUN docker-php-ext-enable imagick

# php opcache
RUN docker-php-ext-configure opcache --enable-opcache
RUN docker-php-ext-install opcache

# php redis
RUN pecl install redis
RUN docker-php-ext-enable redis

# clean apt cache
RUN rm -rf /var/lib/apt/lists/*

# add custom php settings
COPY custom-php.ini /usr/local/etc/php/conf.d/custom.ini

# setup apache configuration
COPY apache.conf /etc/apache2/sites-available/nextcloud.conf
RUN a2enmod rewrite
RUN a2enmod ssl
RUN a2enmod proxy
RUN a2enmod proxy_http
RUN a2enmod headers
RUN a2dissite 000-default.conf
RUN a2ensite nextcloud.conf
