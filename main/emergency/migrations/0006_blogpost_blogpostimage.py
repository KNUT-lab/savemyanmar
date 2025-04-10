# Generated by Django 5.2 on 2025-04-09 07:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emergency', '0005_paymentplatforms_state_helpcentres_city_state_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blogpost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('general', 'General'), ('warning', 'Warning'), ('update', 'Update'), ('resource', 'Resource'), ('safety', 'Safety')], default='general', max_length=10)),
                ('title', models.TextField()),
                ('content', models.TextField()),
                ('poster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emergency.suppliers')),
            ],
        ),
        migrations.CreateModel(
            name='BlogpostImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_reference', models.ImageField(upload_to='blog_images/')),
                ('blogpost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_images', to='emergency.blogpost')),
            ],
        ),
    ]
