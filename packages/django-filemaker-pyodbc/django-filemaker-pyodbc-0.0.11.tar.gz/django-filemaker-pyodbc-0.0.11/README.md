# django-filemaker-pyodbc

## A Django Custom Database Engine that works with Filemaker using pyodbc.

### Initial components derived from https://github.com/lionheart/django-pyodbc. Using that package as a guide was very helpful.

#### <i>Use with a little caution</i> as some functions in some components are expecting a MS-SQL backend. 
Those will be changed in due course as needed. Pull requests welcome.

#### Note that <b>NO</b> testing has been done as yet on migrations.
Our first use case was talking to an existing filemaker solution.


Example model. Note `managed = False` and `db_table` must match the table object name in the Filemaker Relationship Graph window.

```

\# -*- coding: utf-8 -*-

from \_\_future\_\_ import unicode_literals

from django.db import models

class Depot(models.Model):

    id = models.IntegerField(primary_key=True,help_text='id',db_column='id') 
    uuid = models.UUIDField(null=True,blank=True,help_text='uuid',db_column='uuid',db_index=True,unique=True) 
    
    name = models.CharField(max_length=1024,null=True,help_text='134.13',db_column='depot_name',db_index=True)

    filemaker_base_table_id = 134

    def __str__(self):
        return '%s id: %d' % (self.name, self.id)

    class Meta:
        db_table = 'depot'
        managed = False
        verbose_name = 'Depot'
        verbose_name_plural = 'DepotList'


```


To use.

* `pip install django-filemaker-pyodbc`
* [Install ODBC Drivers for Filemaker](https://fmhelp.filemaker.com/docs/edition/en/fm_odbc_jdbc_guide.pdf)
* Create an odbc connection to the Filemaker solution and test that the credentials work.
* [install unixodbc](https://duckduckgo.com/?q=install+unixodbc)
* Add references to the Filemaker odbc library that unixodbc can see.

	Example content within `/usr/local/etc/odbcinst.ini`

	
	`[filemaker]`
	
	`Driver = /Library/ODBC/FileMaker ODBC.bundle/Contents/MacOS/fmodbc.so`
	
	`DriverManagerEncoding=UTF-16`
	
	`Setup  = `
	


	To find where the settings are for unixodbc try `odbcinst -j`
	

* Add your connection details to your settings.py file.

``` 
DATABASES = {
    'default': {
        'ENGINE': 'django_filemaker_pyodbc',
        'HOST': 'fully qualified domain or ip address',
        'PORT': '2399',
        'USER': 'filemaker user account with odbc/jdbc permissions',
        'PASSWORD': '********',
        'NAME': 'filemaker file name without the extension - preferably without spaces',
        'OPTIONS' : {
            'driver' : 'filemaker',
            'driver_supports_utf8' : True,
			'autocommit' : True,
        },
    }
}
```

Note there are some tables that need to be installed into your Filemaker solution.



Filemaker SQL is a partial implementation of SQL 92
See [Filemaker 16 SQL Reference](https://fmhelp.filemaker.com/docs/16/en/fm16_sql_reference.pdf) for more details.

Versions:
• 0.0.9 Removed +00:00 from sql date as string parameters to handle Filemaker non time zone aware timestamps.

• 0.0.8 Removed debugging print statements.
		Added django-tables.xml
		Added django-tables.fmp12
		Changed publish.sh to accept a command line parameter.

• 0.0.7 Resolved issue with selecting n+1 items in a list.
        Relates to: 'DatabaseOperations' object has no attribute 'is_db2'.
		https://taiga.bd2l.com.au/project/csmu-django-filemaker-pyodbc/issue/3
		examples of code that showed the errer which is now resolved.
		``'
		rostertemplate___shiftshot = rostertemplate___shiftslot_list[5]                             
		````
		Added a sample django-tables.fmp12 file with the tables required for django to work with filemaker solutions.
		Added django-tables.xml
		Added django-tables.xml converted to JSON files within the django-table directory.

• 0.0.6 https://taiga.bd2l.com.au/project/csmu-depot-maestro/task/221
    
  Add in django tables
    
  Added support for creating insert sql on objects with a db_column attribute.
  We now can login via a django login into a Filemaker solution with the necessary supporting tables.
			
• 0.0.5 https://taiga.bd2l.com.au/project/csmu-depot-maestro/issue/197

  'SQLCompiler' object has no attribute 'can_bulk'
  Added can_bulk to class SQLCompiler.

• 0.0.4

  Resolved issues with SQL Insert statements.
  Added has_bulk_insert = False to features.

• 0.0.3

  Removed dependencies requiring django_pyodbc to be installed.
  
  Added support for autocommit with True as the default.
    
• 0.0.2 

  Resolved issue with clobbering str types as binary on save
  
• 0.0.1 

  Initial version