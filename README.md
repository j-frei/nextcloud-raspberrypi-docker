# Docker-based Nextcloud on Raspberry Pi

## Prerequisits
 - Docker installed
 - Docker-compose installed
 - Mounted data directory for data storage
 - `$user` is part of group `docker`

## Installation

### Presteps
 - [Optional] Generate self-signed certificates:
   ```bash
   openssl req -new -newkey rsa:4096 -sha256 -nodes -x509 -keyout ./cert.key -out ./cert.crt -subj "/C=ExCountry/ST=ExState/L=ExLoc/O=ExOrg/OU=ExOrgUnit/CN=*.myfritz.net"
   ```  
   or get your certificates via Let's Encrypt.
 - Put certificates `tls.crt`, `tls.key` into the `./certs` folder
 - Access data directory and create directories:
   ```bash
   # move to data directory (e.g. USB HDD)
   cd /data
   # create directory for nextcloud data
   mkdir data_nextcloud
   sudo chown -R www-data:www-data data_nextcloud

   # create directory for nextcloud db data
   mkdir data_nextcloud
   sudo chown -R root:root db_nextcloud
   ```
 - Create webroot directory:
   ```bash
   cd /path/to/rpi-docker-compose

   # setup webroot and download setup-nextcloud script
   mkdir webroot
   wget https://download.nextcloud.com/server/installer/setup-nextcloud.php -O webroot/setup-nextcloud.php
   sudo chown -R www-data:www-data webroot
   ```
 - Modify `docker-compose.yml`:
   * Line 13: Change `/data/data_nextcloud` to `$DATA_DIR/data_nextcloud`
   * Line 24: Change `/data/db_nextcloud` to ``$DATA_DIR/db_nextcloud`

### Mainsteps
 - Run `docker-compose build --pull` to create the Docker image.
 - Run `docker-compose up -d`.
 - Access `https://<HOST>/setup-nextcloud.php` from your browser.
 - Install Nextcloud in webroot directory (by entering `.` into the web form).
 - Wait for finish and setup the Nextcloud credentials:
   - Select PostgreSQL (not accessible outside of Docker)
     - Username: nextcloud_user
     - Password: nextcloud_password
     - Database: nextcloud
     - Host: nextcloud-db
   - Set data directory to: `/var/www/data`
   - Uncheck installation of recommended apps.
- Finalize setup.

### Poststeps
 - Setup Redis for caching:
   ```bash
   docker-compose exec -u www-data nextcloud-lamp php /var/www/html/occ -n config:system:set memcache.local --value="\OC\Memcache\Redis"
   docker-compose exec -u www-data nextcloud-lamp php /var/www/html/occ -n config:system:set memcache.distributed --value="\OC\Memcache\Redis"
   docker-compose exec -u www-data nextcloud-lamp php /var/www/html/occ -n config:system:set memcache.locking --value="\OC\Memcache\Redis"
   docker-compose exec -u www-data nextcloud-lamp php /var/www/html/occ -n config:system:set filelocking.enabled --type=boolean --value=true
   docker-compose exec -u www-data nextcloud-lamp php /var/www/html/occ -n config:system:set redis host --value="nextcloud-redis"
   docker-compose exec -u www-data nextcloud-lamp php /var/www/html/occ -n config:system:set redis password --value="nextcloud_redis_pass"
   docker-compose exec -u www-data nextcloud-lamp php /var/www/html/occ -n config:system:set redis port --type=integer --value=6379
   ```
## Remarks
 - Redis needs a password in order to be used by Nextcloud. Nextcloud 19 seems unable to work with a passwordless Redis instance. The password security level does not matter since it only operates inside the Docker environment.