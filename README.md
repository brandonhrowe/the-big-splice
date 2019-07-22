The Big Splice requires the following installations for use, in addition to Django:

-ffmpg (pip install ffmpy)
-internetarchive (pip install internetarchive)
-django-rest-framework (pip install django-rest-framework)
-django-cors-headers (pip install django-cors-headers)
-psycopg2 for using a Postgres database (conda install -c anaconda psycopg2 or pip install psycopg2)


***
$CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
$CONDA_PREFIX/etc/conda/deactivate.d/env_vars.sh

To install Internet Archive command line tool:
$ curl -LOs https://archive.org/download/ia-pex/ia
$ chmod +x ia

Command line: ia configure - will save to ~/.config/ia.ini
