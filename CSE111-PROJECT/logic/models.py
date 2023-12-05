from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def validate_word_length(value, max_length=30):
    for word in value.split():
        if len(word) > max_length:
            raise ValidationError(f"Word '{word}' in the title exceeds maximum length of {max_length} characters.")

class Topic(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Poll(models.Model):
    host =  models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    debate_title = models.TextField(validators=[validate_word_length])
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True) # Takes a timestamp every single time it's updated
    created = models.DateTimeField(auto_now_add=True)  # only creates timestamp when it was created
    photo = models.ImageField(upload_to='poll_photos/', blank=True)  # optional photo upload field

    def upvote(self):
        self.up_votes += 1
        self.save()

    def downvote(self):
        self.down_votes += 1
        self.save()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f" ({self.debate_title})"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    bio = models.TextField(validators=[validate_word_length],max_length=500,blank=True, null=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to= 'profiles/', default = "poll_photos/picTest.jpg")
    following = models.ManyToManyField(User, related_name='followers', blank=True)
    saved_posts = models.ManyToManyField(Poll, related_name='saved_by', blank=True)


    def __str__(self):
        return str(self.user.username)
    
    def save_post(self, post_to_save):
        self.saved_posts.add(post_to_save)

    def unsave_post(self, post_to_unsave):
        self.saved_posts.remove(post_to_unsave)


    def follow(self, user_to_follow):
        if user_to_follow != self.user:
            self.following.add(user_to_follow)

    def unfollow(self, user_to_unfollow):
        self.following.remove(user_to_unfollow)

    def followers_count(self):
        return Profile.objects.filter(following__in=[self.user]).count()
    
    def following_users(self):
        return self.following.all()

    def followers(self):
        return Profile.objects.filter(following__in=[self.user])

    
class Vote(models.Model):
    userprofile = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    vote_status = models.IntegerField(default=0)

    class Meta:
        unique_together = ('userprofile', 'poll')

    def __str__(self):
        return f"{self.userprofile.username} - {self.poll.debate_title} - {self.vote_status}"


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Poll, on_delete=models.CASCADE) #Deletes all messages in the post
    body = models.TextField(validators=[validate_word_length])
    updated = models.DateTimeField(auto_now = True) 
    created = models.DateTimeField(auto_now_add = True)  

    def __str__(self):
        return self.body[0:30]
    
    class Meta:
        ordering = ['-updated', '-created']


