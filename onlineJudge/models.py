from sqlite3 import Timestamp
from tkinter import CASCADE
from django.db import models


class Problems(models.Model):
    Problem_Name = models.CharField(max_length=50)
    Problem_Description = models.TextField()
    difficulty_choice=(
        ('easy','easy'),
        ('medium','medium'),
        ('difficult','difficult'),
    )
    Problem_Difficulty = models.CharField(max_length=20,choices=difficulty_choice,default='easy')

    def __str__(self):
        return self.Problem_Name

class Test_Case(models.Model):
    Pname = models.ForeignKey(Problems, on_delete=models.CASCADE)
    test_input = models.FileField(upload_to='test_input/',null=False)
    test_output = models.FileField(upload_to='test_output/',null=False)
    def __str__(self):
        return self.test_input

class Solutions(models.Model):
    Pname = models.ForeignKey(Problems,on_delete=models.CASCADE)
    language_choices=(
        ('c++','cpp'),
        ('c','c'),
        ('java','java'),
        ('python','python'),
    )
    Language = models.CharField(max_length=20,choices=language_choices)
    Code_file = models.FileField(upload_to='Code_file', null=False)
    verdict_choice=(
        ('Exe','Executing'),
        ('WA','Wrong Answer'),
        ('AC','All Correct'),
        ('TLE','Time Limit Exeeded'),
        ('MLE','Memory Limit Exeeded'),
    )
    verdict = models.CharField(max_length=10,choices=verdict_choice)
    timestamp= models.TimeField(auto_now_add=True)
    def __str__(self):
        return self.verdict