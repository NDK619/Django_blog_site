from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.
class DraftedManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset()\
		.filter(status=Post.Status.DRAFT)

class PublishedManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset()\
		.filter(status=Post.Status.PUBLISHED)

class Post(models.Model):
	class Status(models.TextChoices):
 		DRAFT = 'DF', 'Draft'
 		PUBLISHED = 'PB', 'Published'
	# создаем менеджер тегов
	tags = TaggableManager()

	# title - поле заголовка поста
	title = models.CharField(max_length=250)

	# slug - Слаг – это короткая метка, содержащая только буквы, цифры, знаки подчеркивания или дефисы
	slug = models.SlugField(max_length=250, unique_for_date='publish')

	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')

	# body: поле для хранения тела поста. Это поле с типом TextField,
	body = models.TextField() 
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
 	
	objects = models.Manager() # менеджер, применяемый по умолчанию
	published = PublishedManager() # конкретно-прикладной менеджер
	unpublished = DraftedManager()
	
 	# отвечает за метаданные модели
	class Meta:
 		#задает убывающий порядок, в том случае, если порядок не определен
		ordering = ['-publish']
 		# задает порядок по убыванию индексов, которые мы берем из БД
		indexes = [
			models.Index(fields=['-publish']),
		]


	def __str__(self): # переопределяем метод, который отвечает за стороковое представления объекта
		return self.title

	def get_absolute_url(self):
		return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'

