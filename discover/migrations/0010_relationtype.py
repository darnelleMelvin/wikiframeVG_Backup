# Generated by Django 4.1.8 on 2023-04-25 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discover', '0009_alter_oralhistory_itemdesc'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelationType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(db_index=True, max_length=20)),
                ('relation_type', models.CharField(max_length=20)),
            ],
        ),
    ]
