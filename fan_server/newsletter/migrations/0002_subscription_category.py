# Generated by Django 5.0.7 on 2024-07-31 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='category',
            field=models.CharField(choices=[('TANKS', 'Танки'), ('HEALERS', 'Хилы'), ('DPS', 'ДД'), ('TRADERS', 'Торговцы'), ('GUILDMASTERS', 'Гилдмастеры'), ('QUESTGIVERS', 'Квестгиверы'), ('BLACKSMITHS', 'Кузнецы'), ('LEATHERWORKERS', 'Кожевники'), ('POTIONMAKERS', 'Зельевары'), ('SPELLMASTERS', 'Мастера заклинаний')], default=2, max_length=20),
            preserve_default=False,
        ),
    ]
