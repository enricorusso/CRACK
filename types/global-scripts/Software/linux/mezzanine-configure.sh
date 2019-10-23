#!/bin/bash

set -e

ID="unknown"
test -f /etc/os-release && source /etc/os-release

dbuser=$(ctx node properties db_username)
dbpass=$(ctx node properties db_password)
dbhost=$(ctx node properties db_host)
dbname=$(ctx node properties db_name)

user=$(ctx node attributes username)
if [ "$user" != "" ] && [ "$user" != "null" ]; then
    group=$(id -gn root)
else
    user="root"
    group="root"
fi

ctx node attributes path = "/usr/local/mezzanine_env/blog/blog/"

echo "set user $user/$group"
#ctx download-resource /tmp/gunicorn.service global-scripts/Artifacts/gunicorn.service
ctx download-resource /tmp/blog.nginx global-scripts/Artifacts/blog.nginx 

echo -n "Distro: "
case $ID in
    ubuntu|debian)
        echo "ubuntu/debian"

        if [ "$proxy_url" != "" ]; then
            echo "Proxy: $proxy_url"
            export http_proxy="$proxy_url"
            export https_proxy="$proxy_url"
        fi

        while fuser /var/{lib/{dpkg,apt/lists},cache/apt/archives}/lock >/dev/null 2>&1; do echo "dpkg database is locked."; sleep 10; done

        if [ $(stat -c %y /var/lib/apt/periodic/update-success-stamp | cut -d' ' -f 1) != $(date +%Y-%m-%d) ]; then
            apt update
        fi

        while fuser /var/{lib/{dpkg,apt/lists},cache/apt/archives}/lock >/dev/null 2>&1; do echo "dpkg database is locked."; sleep 10; done

        apt -y install libmysqlclient-dev

        cd /usr/local/
        virtualenv mezzanine_env
        source mezzanine_env/bin/activate
        cd mezzanine_env/
        pip install mezzanine gunicorn mysqlclient # psycopg2-binary
        mezzanine-project blog
        cd blog
        pip install -r requirements.txt

        sed -i 's/"ENGINE": "django.db.backends.sqlite3"/"ENGINE": "django.db.backends.mysql"/g' /usr/local/mezzanine_env/blog/blog/local_settings.py
        sed -i "s/\"NAME\": \"dev.db\"/\"NAME\": \"${dbname}\"/g" /usr/local/mezzanine_env/blog/blog/local_settings.py
        sed -i "s/\"USER\": \"\"/\"USER\": \"${dbuser}\"/g" /usr/local/mezzanine_env/blog/blog/local_settings.py
        sed -i "s/\"PASSWORD\": \"\"/\"PASSWORD\": \"${dbpass}\"/g" /usr/local/mezzanine_env/blog/blog/local_settings.py
        sed -i "s/\"HOST\": \"\"/\"HOST\": \"${dbhost}\"/g" /usr/local/mezzanine_env/blog/blog/local_settings.py
        sed -i 's/"localhost", "127.0.0.1", "::1"/"*"/g' /usr/local/mezzanine_env/blog/blog/local_settings.py

        sed -i 's/# from mezzanine.blog import views as blog_views/from mezzanine.blog import views as blog_views/g' /usr/local/mezzanine_env/blog/blog/urls.py
        sed -i 's/url("^$", direct_to_template, {"template": "index.html"}, name="home"),/# url("^$", direct_to_template, {"template": "index.html"}, name="home"),/g' /usr/local/mezzanine_env/blog/blog/urls.py
        sed -i 's/# url("^$", blog_views.blog_post_list, name="home"),/url("^$", blog_views.blog_post_list, name="home"),/g' /usr/local/mezzanine_env/blog/blog/urls.py

        python manage.py createdb --noinput
        python manage.py collectstatic --noinput

        # gunicorn
        #cp /tmp/gunicorn.service /etc/systemd/system/gunicorn.service
        echo "
[Unit]
After=network.target

[Service]
User=$user
Group=$group
WorkingDirectory=/usr/local/mezzanine_env/blog
ExecStart=/usr/local/mezzanine_env/bin/gunicorn --access-logfile - --workers 3 --bind unix:/usr/local/mezzanine_env/blog/blog.sock blog.wsgi:application        
        " > /etc/systemd/system/gunicorn.service
        systemctl daemon-reload
        service gunicorn start

        # nginx
        cp /tmp/blog.nginx /etc/nginx/sites-available/blog
        cd /etc/nginx/sites-enabled/
        rm default
        ln -s /etc/nginx/sites-available/blog
        service nginx restart
        ;;
    *)
        echo "distro $ID not supported :("
        ;;
esac