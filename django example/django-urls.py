'''
Получаем ссылку на вьюху!!!!!!!!!
'''

# example urls.py
from news import views
url(r'^archive/$', views.archive, name='news-archive')

# 1
from django.core.urlresolvers import reverse
reverse('news-archive')

# 2
from django.core.urlresolvers import reverse
from news import views
reverse(views.archive)

#with position args
#return HttpResponseRedirect(reverse('news-archive', args=[1945]))

#with keywords args
reverse('admin:app_list', kwargs={'app_label': 'auth'})

# !!! args kwargs вместе не передаются
# Если reverse() не найдет подходящего URL-а, будет вызвано исключение NoReverseMatch.



#у объектов модели метод get_absolute_url

#в шаблоне тег url
# {% url 'news-archive' v1 v2 %}
# {% url 'news-archive' arg1=v1 arg2=v2 %}

# ('^clients/', include('project_name.app_name.urls'))
# ('^client/([0-9]+)/$', app_views.client, name='app-views-client')
# {% url 'app-views-client' client.id %}
# /clients/client/123/

# {% url 'myapp:view-name' %}
