#!/usr/bin/env bash
set -o errexit

python3 -m pip install -U pip
apk add --no-cache --virtual .build-deps musl-dev gcc python3-dev
python3 -m pip install flask hoedown xpinyin pyrss2gen gitpython watchdog requests
apk del --purge .build-deps
echo "{\"install\":\"docker\"}" > /home/silverblog/install/install.lock

bash /home/silverblog/install/initialization.sh
sed -i '''s/.\/config\/unix_socks\/main.sock/0.0.0.0:5000/g' uwsgi.json
sed -i '''s/.\/config\/unix_socks\/control.sock/0.0.0.0:5001/g' uwsgi.json
cp -f /home/silverblog/.develop/demo/page.json /home/silverblog/config/page.json
cp -f /home/silverblog/.develop/demo/menu.json /home/silverblog/config/menu.json
cp -f /home/silverblog/.develop/demo/system.json /home/silverblog/config/system.json
cp /home/silverblog/.develop/demo/demo-article.md /home/silverblog/document/demo-article.md
python3 manage.py update
cd /home/silverblog/templates
bash -c "$(curl -fsSL https://raw.githubusercontent.com/SilverBlogTheme/clearision/master/install.sh)"
cd /home/silverblog/
cat << EOF >pm2.json
{
  "apps": [
    {
      "name": "silverblog",
      "script": "/usr/bin/python3",
      "args": "watch.py",
      "merge_logs": true,
      "cwd": "./"
    },
    {
      "name": "silverblog-control",
      "script": "/usr/bin/python3",
      "args": [
        "watch.py",
        "--control"
      ],
      "merge_logs": true,
      "cwd": "./"
    }
  ]
}
EOF