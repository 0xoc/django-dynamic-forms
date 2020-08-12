# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'oq)z#t39tzq@)zznf$jt%x4!y#1kts8$xyw4ke^y2s0-q9o*7@'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'forms',
        'USER': 'postgres',
        'PASSWORD': 'thecode',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
