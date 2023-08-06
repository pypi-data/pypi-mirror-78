# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['codex',
 'codex.choices',
 'codex.librarian',
 'codex.migrations',
 'codex.serializers',
 'codex.views',
 'tests']

package_data = \
{'': ['*'],
 'codex': ['static_root/*',
           'static_root/admin/css/*',
           'static_root/admin/css/vendor/select2/*',
           'static_root/admin/fonts/*',
           'static_root/admin/img/*',
           'static_root/admin/img/gis/*',
           'static_root/admin/js/*',
           'static_root/admin/js/admin/*',
           'static_root/admin/js/vendor/jquery/*',
           'static_root/admin/js/vendor/select2/*',
           'static_root/admin/js/vendor/select2/i18n/*',
           'static_root/admin/js/vendor/xregexp/*',
           'static_root/css/*',
           'static_root/debug_toolbar/css/*',
           'static_root/debug_toolbar/img/*',
           'static_root/debug_toolbar/js/*',
           'static_root/fonts/*',
           'static_root/img/*',
           'static_root/js/*',
           'static_root/rest_framework/css/*',
           'static_root/rest_framework/docs/css/*',
           'static_root/rest_framework/docs/img/*',
           'static_root/rest_framework/docs/js/*',
           'static_root/rest_framework/fonts/*',
           'static_root/rest_framework/img/*',
           'static_root/rest_framework/js/*',
           'templates/admin/*',
           'templates/admin/codex/adminflag/change_list.html',
           'templates/admin/codex/library/change_list.html',
           'templates/browserconfig.xml',
           'templates/browserconfig.xml',
           'templates/browserconfig.xml',
           'templates/index.html',
           'templates/index.html',
           'templates/index.html',
           'templates/site.webmanifest',
           'templates/site.webmanifest',
           'templates/site.webmanifest']}

install_requires = \
['Pillow>=7.0,<8.0',
 'bidict>=0.21.0,<0.22.0',
 'coloredlogs>=14.0,<15.0',
 'comicbox>=0.1.3,<0.2.0',
 'django-cors-headers>=3.2,<4.0',
 'django>=3.1,<4.0',
 'djangorestframework>=3.11,<4.0',
 'fnvhash>=0.1,<0.2',
 'hypercorn[h3]>=0.10.1,<0.11.0',
 'pycountry>=20.7.3,<21.0.0',
 'regex>=2020.4.4,<2021.0.0',
 'simplejson>=3.17,<4.0',
 'stringcase>=1.2.0,<2.0.0',
 'watchdog>=0.10,<0.11',
 'websocket_client>=0.57.0,<0.58.0',
 'whitenoise[brotli]==5.1.0']

entry_points = \
{'console_scripts': ['codex = codex.run:main']}

setup_kwargs = {
    'name': 'codex',
    'version': '0.5.9',
    'description': 'A comic archive web server.',
    'long_description': '# Codex\n\nCodex is a comic archive browser and reader.\n\n## Features\n\n- A web server, not a desktop or mobile app.\n- Per user bookmarking.\n- Filter and sort on comic metadata and unread status per user.\n- Watches the filesystem and automatically imports new or changed comics.\n\n## State of Development\n\nCodex is in alpha test. It has not received widespread testing.\n[Please file bug reports on GitHub.](https://github.com/ajslater/codex/issues) It is still possible that the data model might change enough that subsequent versions might require a database reset.\n\n## Demonstration\n\nYou may browse a [live demo server](https://codex.sl8r.net/) on a very small VPS, with no CDN. Caching is likely unsufficient for heavy load at this time. It would probably crash if it got swarmed right now.\n\n## Install Codex\n\n### Docker\n\nAll dependancies bundled in the official [Docker Image](https://hub.docker.com/r/ajslater/codex).\n\n### Install with pip\n\n#### Wheel Build Dependencies\n\nYou\'ll need to install these system dependencies before installing codex.\n\n##### MacOS\n\n```sh\nbrew install libffi jpeg openssl libyaml libzip python\n```\n\n##### Linux\n\n###### Debian based (e.g. Ubuntu)\n\n```sh\napt install build-essential libffi-dev libjpeg-dev libssl-dev libyaml-dev python3-pip zlib1g-dev\n```\n\n###### Alpine\n\n```sh\napk add bsd-compat-headers build-base libffi-dev openssl-dev yaml-dev jpeg-dev zlib-dev\n```\n\n#### Install unrar Runtime Dependancy\n\nCodex requires unrar to read cbr formatted comic archives.\n\n##### Linux\n\n[How to install unrar in Linux](https://www.unixtutorial.org/how-to-install-unrar-in-linux/)\n\n##### MacOS\n\n```sh\nbrew install unrar\n```\n\n#### Install Codex with pip\n\nFinally, you may install codex with pip\n\n```sh\npip3 install codex\n```\n\n## Run Codex\n\npip should install the codex binary on your path. Run\n\n```sh\ncodex\n```\n\nand then navigate to [http://localhost:9810/](http://localhost:9810/)\n\n### Administration\n\n#### Change the Admin password\n\nThe first thing you need to do is to log in as an Administrator and change the admin password.\n\n- Log in with the **&vellip;** menu in the upper right of the browse view. The default administator username/password is admin/admin.\n- Navigate to the Admin Panel by selecting it from under the three dots menu after you have logged in.\n- Navigate to the Users panel.\n- Select the `admin` user.\n- Change the admin password using the tiny "this form" link in the password section.\n- You may also change the admin user\'s name or anything else.\n\n#### Adding Comic Libraries\n\nThe second thing you should do is log in as an Administrator and add one or more comic libraries.\n\n- Log in with any superuser (such as the default adimin account) using the **&vellip;** menu in the upper right of the browse view.\n- Navigate to the Admin Panel by selecting it from under the three dots menu after you have logged in.\n- Navigate to the Codex API Librarys (sic) on the Admin Panel\n- Add a Library with the "ADD LIBRARY +" button in the upper right.\n\n##### Reset the admin password.\n\nIf you forget all your superuser passwords, you may restore the original default admin account by running codex with the `CODEX_RESET_ADMIN` environment variable set.\n\n```sh\nCODEX_RESET_ADMIN=1 codex\n```\n\nor, if using Docker:\n\n```sh\ndocker run -e CODEX_RESET_ADMIN=1 -v <host path to config>/config:/config ajslater/codex\n```\n\n## Configure Codex\n\n### Config Dir\n\nThe default config directory is named `config/` directly under the working directory you run codex from. You may specificy an alternate config directory with the environment variable `CODEX_CONFIG_DIR`.\n\nThe config directory contains a hypercorn config `hypercorn.toml` where you can specify ports and bind addresses. If no `hypercorn.toml` is present a default one is copied to that directory on startup. The default port is 9810.\n\nThe config directory also holds the main sqlite database, a django cache and comic book cover thumbnails generated when comics are imported. Reimport a comic or an entire library to regenereate these cover thumbnails.\n\n### Reverse Proxy\n\n[nginx](https://nginx.org/) is often used as a TLS terminator and subpath proxy.\n\nHere\'s an example nginx config with a subpath named \'/codex\'.\n\n```nginx\nproxy_set_header  Host              $http_host;\n    proxy_set_header  X-Forwarded-For   $proxy_add_x_forwarded_for;\n    proxy_set_header  X-Forwarded-Host  $server_name;\n    proxy_set_header  X-Forwarded-Port  $server_port;\n    proxy_set_header  X-Forwarded-Proto $scheme;\n    proxy_set_header  X-Real-IP         $remote_addr;\n    proxy_set_header  X-Scheme          $scheme;\n\n    # WS\n    proxy_http_version 1.1;\n    proxy_set_header Upgrade $http_upgrade;\n    proxy_set_header Connection "Upgrade"\n\n    # This example uses a docker container named \'codex\' at sub-path /codex\n    # Use a valid IP or resolvable host name for other configurations.\n    location /codex {\n        proxy_pass  http://codex:9810;\n    }\n```\n\nSpecify a reverse proxy sub path (if you have one) in the config/hypercorn.toml\n\n```toml\nroot_path = "/codex"\n\n```\n\n#### Nginx Reverse Proxy 502 when container is refreshed.\n\nNginx requires a special trick to refresh dns when linked Docker containers\nare recreated. See this [nginx with dynamix upstreams](https://tenzer.dk/nginx-with-dynamic-upstreams/) article.\n\n## Using Codex\n\n### Sessions & Accounts\n\nOnce your administrator has added some comic libraries, you may browse and read comics. Codex will remember your preferences, bookmarks and progress in the browser session. Sessions last 60 days at which point they are destroyed.\nTo preserve these settings across browsers and after sessions expire, you may register an account with a username and password.\nYou will have to contact your administrator to reset your password if you forget it.\n\n## Codex Roadmap\n\n### Alpha Test\n\n- Fix bugs that I haven\'t found in my private testing\n\n### Next Up\n\n- Edit & write metadata for one comic at a time.\n- Add more Filters & Sort options (e.g. filter by story_arc, location)\n- [OPDS](https://en.wikipedia.org/wiki/Open_Publication_Distribution_System)\n- Dark Admin Panel Styling.\n- Upgrade Vue to version 3\n\n## Out of Scope\n\n- No intention of making this an eBook reader like [Ubooquity](https://vaemendis.net/ubooquity/).\n- Not interested in this becoming a sophisticated comic manager like [Mylar](https://github.com/mylar3/mylar3)\n- Unsure if I want to implement a mass tag editor.\n\n## Alternatives to Codex\n\n- [Komga](https://komga.org/) has light metadata editing and full text search of metadata.\n- [Ubooquity](https://vaemendis.net/ubooquity/) is a good looking comic webserver. It also reads eBooks.\n\n## Develop Codex\n\nCodex is a Django Python webserver with a VueJS front end. This is my first ever Javascript frontend. In retrospect I wish I\'d known about FastAPI when I started, that looks nice. But I\'m pretty satisfied with VueJS.\n\n`/codex/codex/` is the main django app which provides the webserver and database.\n\n`/codex/frontend/` is where the vuejs frontend lives.\n\n`/codex/setup-dev.sh` will install development dependancies.\n\n`/codex/dev-server-ttabs.sh` will run the three or four different servers reccomended for development in terminal tabs.\n\n`/codex/run.sh` runs the main Django server. Set the `DEV` environment variable to activea development and debug mode: `DEV=1 ./run.sh`. This also lets you run the server without collecting static files for production and with a hot reloading frontend.\n\n### Links\n\n- [Docker Image](https://hub.docker.com/r/ajslater/codex)\n- [PyPi Package](https://pypi.org/project/codex/)\n- [GitHub Project](https://github.com/ajslater/codex/)\n\n## Special Thanks\n\nThanks to [Aurélien Mazurie](https://pypi.org/user/ajmazurie/) for allowing me to use the PyPi name \'codex\'.\n\n## Enjoy!\n\n![These simple people have managed to tap into the spiritual forces that mystics and yogis spend literal lifetimes seeking. I feel... ...I feel...](strange.jpg)\n',
    'author': 'AJ Slater',
    'author_email': 'aj@slater.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ajslater/codex',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
