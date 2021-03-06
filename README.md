# BeBot Platform project (v1.0)
The following describes the characteristics of the project in order to facilitate the integration of the BeBotPlatform project in a Development or Production environment.

## General characteristics
The project is used [python3.5](https://www.python.org/downloads/release/python-350/) y [Django2.0.1](https://docs.djangoproject.com/en/2.0/releases/2.0.1/)

## BeBot platform

BeBot Platform is created in a development environment created with [vistualenv] (https://virtualenv.pypa.io/en/stable/), and the environment has the name of ENV and is active through

- Activate
```
cd ~/ENV
source bin/activate
```
- Deactivate
```
deactivate
```

### Config Mysql
Configuration for Mysql and Django
```
mysql -u root -p
CREATE DATABASE bebotDB CHARACTER SET UTF8;
CREATE USER bebot@localhost IDENTIFIED BY 'bebot';
GRANT ALL PRIVILEGES ON bebotDB.* TO bebot@localhost;
```

#### Migration: In the bebotPlatform directory
```
python3 manage.py makemigrations
python3 manage.py migrate
```

### Django
Super user BeBotPlatform
```
UserName = admin
Pass = bebotplatform
```

### Requirements installation: In bebotPlatform directory
```
pip3 install -r requirements.txt
```
- For: django-activity-stream==0.6.5 - Update manager.py file 'user.is_anonymous'
- For: django-notifications-hq==1.3 - Update models.py from origin
	```
	recipient = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, related_name='notifications', null=True, on_delete=models.CASCADE)
   
    actor_content_type = models.ForeignKey(ContentType, related_name='notify_actor', null=True, on_delete=models.CASCADE)

    target_content_type = models.ForeignKey(ContentType, related_name='notify_target', blank=True, null=True, on_delete=models.CASCADE)
    
    action_object_content_type = models.ForeignKey(ContentType, blank=True, null=True,
                                                    related_name='notify_action_object', on_delete=models.CASCADE)
	```
	then execute:
	```
		python3 manage.py makemigrations notifications
		python3 manage.py migrate notifications
	```
	also update notifications_tag:
	```
	from django.urls import reverse
	
	...
	@register.simple_tag(takes_context=True)
	def notifications_unread(context):

	...

	if user.is_anonymous:
	```

## Development Env Runserver
### localhost
```
python3 manage.py runserver
```

# Important Links
- [How to use django and mysql](https://www.digitalocean.com/community/tutorials/how-to-use-mysql-or-mariadb-with-your-django-application-on-ubuntu-14-04)


# Update server code
1. Do pull code.
2. Install with pip3 requirements.
3. Modify settings.py url site.
4. Execute:
```
python3 manage.py collectstatic
python3 manage.py migrate
sudo supervisorctl restart bobotPlatform
```


