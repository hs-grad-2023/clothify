# Generated by Django 4.2 on 2023-05-11 10:44

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import muapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('height', models.IntegerField(blank=True, null=True, verbose_name='키')),
                ('weight', models.IntegerField(blank=True, null=True, verbose_name='몸무게')),
                ('sex', models.CharField(blank=True, max_length=1, null=True, verbose_name='성별')),
                ('name', models.CharField(blank=True, max_length=4, null=True, verbose_name='이름')),
                ('style', models.CharField(blank=True, max_length=50, null=True, verbose_name='스타일')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='clothes',
            fields=[
                ('uploadUserName', models.CharField(default='unknown', max_length=30)),
                ('type1', models.CharField(max_length=10)),
                ('type2', models.CharField(max_length=50)),
                ('tag', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.CharField(max_length=50)),
                ('details', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('upload_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('groupID', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('ucodi', models.BooleanField(blank=True, null=True)),
                ('like', models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL)),
                ('uploadUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-upload_date'],
            },
        ),
        migrations.CreateModel(
            name='viton_upload_cloth',
            fields=[
                ('clothesname', models.CharField(default='sample', max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('image', muapp.models.ResizedImageField(upload_to=muapp.models.random_name_C)),
                ('maskimage', muapp.models.ResizedImageField(blank=True, null=True, upload_to='datasets/cloth-mask')),
                ('uploadUser', models.CharField(max_length=30)),
                ('uploadDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('ID', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'ordering': ['-ID'],
            },
        ),
        migrations.CreateModel(
            name='viton_upload_model',
            fields=[
                ('clothesname', models.CharField(default='sample', max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('image', muapp.models.ResizedImageField(upload_to=muapp.models.random_name_M)),
                ('maskmodel', muapp.models.ResizedImageField(blank=True, null=True, upload_to='datasets/image-parse')),
                ('openposeImage', muapp.models.ResizedImageField(blank=True, null=True, upload_to='datasets/openpose-img')),
                ('openposeJson', models.FileField(blank=True, null=True, upload_to='datasets/openpose-json')),
                ('uploadUser', models.CharField(max_length=30)),
                ('uploadDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('ID', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'ordering': ['-ID'],
            },
        ),
        migrations.CreateModel(
            name='viton_upload_result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('image', muapp.models.ResizedImageField(upload_to='datasets/results')),
                ('uploadUser', models.CharField(default='sample', max_length=50)),
                ('cloth', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='muapp.viton_upload_cloth')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='muapp.viton_upload_model')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='photos',
            fields=[
                ('photoID', models.AutoField(primary_key=True, serialize=False)),
                ('imgfile', models.ImageField(blank=True, default='imgfiles/no_image.png', null=True, upload_to='imgfiles/%m/%d')),
                ('groupID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='muapp.clothes', verbose_name='groupClothes')),
            ],
        ),
        migrations.CreateModel(
            name='Musinsa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_text', models.TextField()),
                ('item_title', models.TextField()),
                ('item_model', models.TextField()),
                ('item_picture', models.URLField()),
                ('item_page', models.URLField()),
                ('like', models.ManyToManyField(blank=True, related_name='likes2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='muapp.clothes')),
            ],
        ),
    ]
