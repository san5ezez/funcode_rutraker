from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_usergame'),
    ]

    operations = [
        migrations.AddField(
            model_name='usergame',
            name='download_url',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='usergame',
            name='screenshot',
            field=models.ImageField(blank=True, null=True, upload_to='user_games/screenshots/'),
        ),
        migrations.AddField(
            model_name='usergame',
            name='trailer_url',
            field=models.URLField(blank=True),
        ),
    ]
