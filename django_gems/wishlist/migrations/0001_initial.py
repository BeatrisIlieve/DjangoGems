# Generated by Django 4.2.10 on 2024-02-17 09:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jewelry', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JewelryLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jewelry', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='jewelry.jewelry')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('jewelry', 'user')},
            },
        ),
    ]
