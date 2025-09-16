from user.models import *
from django.contrib.auth.models import User
 
# Create your models here.
 
class Blog(models.Model):
    title=models.CharField(max_length=200)
    sub_title=models.CharField(max_length=200)
    content=models.TextField()
    bg_image=models.ImageField(upload_to="blog_bg")
    created_by=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="blog_created_by")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return self.title
 
 
 
class Comment(models.Model):
    comment_text=models.TextField()
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE,related_name="comment_blog")
    user=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="comment_user")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return f"comment user {self.user.user.username}"

    