# Generated by Django 4.2.5 on 2023-09-11 04:09

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(help_text='카테고리', max_length=150)),
                ('price', models.DecimalField(decimal_places=0, default=Decimal('0'), help_text='가격', max_digits=10)),
                ('cost', models.DecimalField(decimal_places=0, default=Decimal('0'), help_text='원가', max_digits=10)),
                ('name', models.CharField(help_text='이름', max_length=254)),
                ('name_to_choseong', models.CharField(blank=True, default='', help_text='이름(초성 검색을 위해서 상품 이름에서 초성만 저장)', max_length=512, null=True)),
                ('description', models.CharField(help_text='설명', max_length=1024)),
                ('barcode', models.CharField(help_text='바코드', max_length=150)),
                ('expiration_date', models.DateTimeField(blank=True, default=None, help_text='유통기한', null=True)),
                ('size', models.CharField(choices=[('LARGE', 'LARGE'), ('SMALL', 'SMALL')], default='SMALL', help_text='사이즈', max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, help_text='상품 삭제일(날짜값이 있으면, 삭제된 상태임)', null=True)),
                ('seller', models.ForeignKey(help_text='상품 등록자', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
