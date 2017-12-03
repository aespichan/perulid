from django.db import models

# Create your models here.

class Language(models.Model):
    iso_code = models.CharField(max_length=10)
    family_id = models.IntegerField(default=0)
    language_name = models.CharField(max_length=200)
    family_order = models.IntegerField(default=0)
    speakers = models.IntegerField(default=0)

    def __str__(self):
        return self.language_name

class Family(models.Model):
    family_id = models.IntegerField(default=0)
    family_name = models.CharField(max_length=200)

    def __str__(self):
        return self.family_name

class Sentence(models.Model):
    iso_code = models.CharField(max_length=10)
    sentence = models.TextField()
    length = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.sentence

class Word(models.Model):
    iso_code = models.CharField(max_length=10)
    word = models.CharField(max_length=100)
    length = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.word

class Character(models.Model):
    iso_code = models.CharField(max_length=10)
    character = models.CharField(max_length=5)
    length = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.character

class Repository_Detail(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    words = models.IntegerField(default=0)
    sentences = models.IntegerField(default=0)
    characters = models.IntegerField(default=0)
    tokens = models.IntegerField(default=0)
    files = models.IntegerField(default=0)

    def __str__(self):
        return self.language

class Repository_Source(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    file = models.CharField(max_length=200)
    source = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.file

class Inverted_Sentence(models.Model):
    sentence = models.TextField()
    file = models.ForeignKey(Repository_Source, on_delete=models.CASCADE)

    def __str__(self):
        return self.sentence

class Inverted_Word(models.Model):
    word = models.CharField(max_length=100)
    position = models.IntegerField(default=0)
    sentence = models.ForeignKey(Inverted_Sentence, on_delete=models.CASCADE)

    def __str__(self):
        return self.word

