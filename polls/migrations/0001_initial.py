# Generated by Django 4.2.10 on 2024-02-20 17:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('on_try', models.CharField(choices=[('rewrite', 'Переписать результат'), ('add', 'Добавить новый'), ('one', 'Запретить')], default='rewrite', max_length=32, verbose_name='При повторном прохождении?')),
                ('name', models.CharField(max_length=255, verbose_name='Название опроса')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание опроса')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='UUID')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст вопроса')),
                ('question_type', models.CharField(choices=[('text', 'Text'), ('single_choice', 'Single Choice'), ('multiple_choice', 'Multiple Choice')], max_length=20)),
                ('other_field', models.BooleanField(default=False, verbose_name='Добавить поле "Другое"?')),
                ('position', models.PositiveSmallIntegerField(null=True, verbose_name='Position')),
                ('required', models.BooleanField(default=False, verbose_name='Обязательный вопрос?')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='UserPoll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='polls.poll')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Ответы Пользователя',
                'verbose_name_plural': 'Ответы Пользователей',
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название секции')),
                ('position', models.PositiveSmallIntegerField(null=True, verbose_name='Position')),
                ('poll', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='polls.poll')),
            ],
            options={
                'verbose_name': 'Секция опроса',
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='QuestionCondition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation', models.CharField(choices=[('>=', '>='), ('<=', '<='), ('==', '=='), ('!=', '!=')], max_length=20)),
                ('value', models.CharField(max_length=255)),
                ('position', models.PositiveSmallIntegerField(null=True, verbose_name='Position')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conditions', to='polls.question')),
                ('question_to_condition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conditions_operand', to='polls.question')),
            ],
            options={
                'verbose_name': 'Условие',
                'verbose_name_plural': 'Условия',
                'ordering': ['position'],
            },
        ),
        migrations.AddField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='polls.section'),
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, verbose_name='Текст варианта ответа')),
                ('position', models.PositiveSmallIntegerField(null=True, verbose_name='Position')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='polls.question')),
            ],
            options={
                'verbose_name': 'Вариант ответа',
                'verbose_name_plural': 'Варианты ответа',
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(blank=True, null=True)),
                ('old_text', models.CharField(blank=True, max_length=255, null=True)),
                ('position', models.PositiveSmallIntegerField(null=True, verbose_name='Position')),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('poll_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='polls.userpoll')),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='polls.question')),
            ],
        ),
    ]
