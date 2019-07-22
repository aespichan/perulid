# Generated by Django 2.1.5 on 2019-02-11 03:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iso_code', models.CharField(max_length=10)),
                ('character', models.CharField(max_length=5)),
                ('length', models.IntegerField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('family_id', models.IntegerField(default=0)),
                ('family_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Inverted_Sentence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sentence', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Inverted_Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100)),
                ('position', models.IntegerField(default=0)),
                ('sentence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lid.Inverted_Sentence')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iso_code', models.CharField(max_length=10)),
                ('family_id', models.IntegerField(default=0)),
                ('language_name', models.CharField(max_length=200)),
                ('family_order', models.IntegerField(default=0)),
                ('speakers', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Repository_Detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('words', models.IntegerField(default=0)),
                ('sentences', models.IntegerField(default=0)),
                ('characters', models.IntegerField(default=0)),
                ('tokens', models.IntegerField(default=0)),
                ('files', models.IntegerField(default=0)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lid.Language')),
            ],
        ),
        migrations.CreateModel(
            name='Repository_Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.CharField(max_length=200)),
                ('source', models.CharField(max_length=200, null=True)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lid.Language')),
            ],
        ),
        migrations.CreateModel(
            name='Sentence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iso_code', models.CharField(max_length=10)),
                ('sentence', models.TextField()),
                ('length', models.IntegerField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iso_code', models.CharField(max_length=10)),
                ('word', models.CharField(max_length=100)),
                ('length', models.IntegerField(default=0, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='inverted_sentence',
            name='file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lid.Repository_Source'),
        ),
    ]
