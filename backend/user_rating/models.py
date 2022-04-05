from django.db import models


class MyUser(models.Model):
    """
    Модель телеграм-пользователя
    """
    tg_user_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    username = models.CharField(max_length=32, blank=True, null=True)

    @property
    def full_name(self) -> str:
        return f"{self.first_name if self.first_name else ''} {self.last_name if self.last_name else ''}"

    def __str__(self):
        return f'{self.tg_user_id=} {self.username=} {self.full_name=}'


class UserQuestion(models.Model):
    """
    Модель вопросов пользователей
    Поле has_an_answer принимает значение True, если пользователь, задавший вопрос, отметил одно из следующих за ним
    сообщений как правильный ответ
    """
    my_user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    question = models.CharField(max_length=1024)
    likes_num = models.IntegerField(default=0)
    dislikes_num = models.IntegerField(default=0)
    has_an_answer = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.my_user_id=} {self.question=} {self.has_an_answer=} {self.likes_num=} {self.dislikes_num=}'


class UserAnswer(models.Model):
    """
    Модель ответтов пользователей
    Поле best_answer принимает значение True, если пользователь, задавший вопрос, или админ
    отметил этот ответ как правильный
    """
    my_user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1024)
    likes_num = models.IntegerField(default=0)
    dislikes_num = models.IntegerField(default=0)
    best_answer = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.my_user_id=} {self.likes_num=} {self.dislikes_num=} {self.best_answer=}'