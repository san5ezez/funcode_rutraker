from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_usergame_trailer_download_screenshot'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamerequest',
            name='status',
            field=models.CharField(
                choices=[('pending', 'На рассмотрении'), ('approved', 'Одобрено'), ('rejected', 'Не одобрено')],
                default='pending',
                max_length=20,
            ),
        ),
    ]
