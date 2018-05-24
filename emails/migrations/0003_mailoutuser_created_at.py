from django.utils import timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0002_ondelete'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailoutuser',
            name='created_at',
            field=models.DateTimeField(default=timezone.now),
        ),
    ]
