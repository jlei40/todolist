# Generated by Django 4.2 on 2024-04-19 02:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_remove_task_created_at_remove_task_due_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('homework', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['name']},
        ),
        migrations.RenameField(
            model_name='task',
            old_name='completed',
            new_name='homework',
        ),
        migrations.RemoveField(
            model_name='task',
            name='title',
        ),
        migrations.AddField(
            model_name='task',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='name',
            field=models.CharField(default='john smith', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.CharField(default='description', max_length=5000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='tags',
            field=models.ManyToManyField(to='tasks.tag'),
        ),
    ]