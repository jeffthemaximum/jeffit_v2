from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from mptt.models import MPTTModel, TreeForeignKey
from hashlib import md5
from utils.helpers import generate_registration_code
from datetime import datetime
from math import log
import mistune
import pudb
import pytz

epoch = datetime(1970, 1, 1)
epoch = pytz.utc.localize(epoch)

class ContentTypeAware(models.Model):
    def get_content_type(self):
        """:return: Content type for this instance."""
        return ContentType.objects.get_for_model(self)

    def get_content_type_id(self):
        """:return: Content type ID for this instance"""
        return self.get_content_type().pk

    def add_vote(self, vote_value):
        self.score += vote_value
        if vote_value == 1:
            self.ups += 1
        elif vote_value == -1:
            self.downs += 1

    class Meta:
        abstract = True


class MttpContentTypeAware(MPTTModel):
    def get_content_type(self):
        """:return: Content type for this instance."""
        return ContentType.objects.get_for_model(self)

    def get_content_type_id(self):
        """:return: Content type ID for this instance"""
        return self.get_content_type().pk

    class Meta:
        abstract = True


class RedditUser(models.Model):
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=35, null=True, default=None,
                                  blank=True)
    last_name = models.CharField(max_length=35, null=True, default=None,
                                 blank=True)
    email = models.EmailField(null=True, blank=True, default=None)
    about_text = models.TextField(blank=True, null=True, max_length=500,
                                  default=None)
    about_html = models.TextField(blank=True, null=True, default=None)
    gravatar_hash = models.CharField(max_length=32, null=True, blank=True,
                                     default=None)
    display_picture = models.NullBooleanField(default=False)
    homepage = models.URLField(null=True, blank=True, default=None)
    twitter = models.CharField(null=True, blank=True, max_length=15,
                               default=None)
    github = models.CharField(null=True, blank=True, max_length=39,
                              default=None)
    comment_karma = models.IntegerField(default=0)
    link_karma = models.IntegerField(default=0)
    total_karma = models.IntegerField(default=0)
    is_instructor = models.BooleanField(default=False)

    def update_profile_data(self):
        self.about_html = mistune.markdown(self.about_text)
        if self.display_picture:
            self.gravatar_hash = md5(self.email.lower()).hexdigest()

    def update_total_karma(self):
        self.total_karma = self.comment_karma + self.link_karma

    # this is good. Do not edit!!!!!!!@@#Q#@one!!!
    def __unicode__(self):
        return "<RedditUser:{}>".format(self.user.username)


class Cohort(models.Model):
    title = models.CharField(max_length=70)
    reddit_users = models.ManyToManyField(RedditUser, related_name='cohorts', blank=True, default=None)
    registration_code = models.CharField(
        max_length=6,
        default=generate_registration_code()
    )

    def __unicode__(self):
        return "<Cohort:{}>".format(self.title)


class Subjeffit(models.Model):
    title = models.CharField(max_length=250)
    about = models.TextField(max_length=5000, blank=True)

    def check_title(self):
        if " " in self.title:
            return False
        else:
            return True

    def generate_url(self):
        return "/j/{}".format(self.title)

    def __unicode__(self):
        return self.title


class Submission(ContentTypeAware):
    author_name = models.CharField(null=False, max_length=12)
    author = models.ForeignKey(RedditUser)
    subjeffit = models.ForeignKey(Subjeffit)
    subjeffit_title = models.CharField(null=False, max_length=250)
    title = models.CharField(max_length=250)
    url = models.URLField(null=True, blank=True)
    text = models.TextField(max_length=5000, blank=True)
    text_html = models.TextField(blank=True)
    ups = models.IntegerField(default=0)
    downs = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    timestamp = models.DateTimeField(default=timezone.now)
    comment_count = models.IntegerField(default=0)

    def epoch_seconds(self, date):
        time_diff = date - epoch
        return time_diff.days * 86400 + time_diff.seconds + (float(time_diff.microseconds) / 1000000)

    def make_score(self, happiness, sadness):
        return happiness - sadness

    def hotness(self):
        # add ups votes and comments together for total positive karma
        total_happiness = self.ups + self.comment_count
        # check if pos or 0 or neg karma
        net_happiness = self.make_score(total_happiness, self.downs)
        # check pos, neg, or zero
        sign_check = 1 if net_happiness > 0 else -1 if net_happiness < 0 else 0
        # get log of nethappiness if nethappiness > 1 else log1
        logifier = log(max(abs(net_happiness), 1), 10)
        # get seconds since epoch
        seconds = self.epoch_seconds(self.timestamp) - 1134028003
        # return algorithm
        # smooshes happiness by log
        # makes it pos or neg
        # factors in how old it is
        return round(sign_check * logifier + seconds / 45000, 7)


    def set_subjeffit_name(self):
        self.subjeffit_title = self.subjeffit.title

    def generate_html(self):
        if self.text:
            html = mistune.markdown(self.text)
            self.text_html = html

    @property
    def linked_url(self):
        if self.url:
            return "{}".format(self.url)
        else:
            return "/comments/{}".format(self.id)

    @property
    def comments_url(self):
        return '/comments/{}'.format(self.id)

    def __unicode__(self):
        return "<Submission:{}>".format(self.id)


class Comment(MttpContentTypeAware):
    author_name = models.CharField(null=False, max_length=12)
    author = models.ForeignKey(RedditUser)
    submission = models.ForeignKey(Submission)
    parent = TreeForeignKey('self', related_name='children',
                            null=True, blank=True, db_index=True)
    timestamp = models.DateTimeField(default=timezone.now)
    ups = models.IntegerField(default=0)
    downs = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    raw_comment = models.TextField(blank=True)
    html_comment = models.TextField(blank=True)

    class MPTTMeta:
        order_insertion_by = ['-score']

    def get_ancestor(self):
        if self.parent != None:
            return 'comment'
        else:
            return 'submission'

    def update_html(self):
        self.html_comment = mistune.markdown(self.raw_comment)

    def get_ancestor_id(self):
        if self.parent != None:
            return self.parent.id
        else:
            return self.submission.id

    @classmethod
    def create(cls, author, raw_comment, parent):
        """
        Create a new comment instance. If the parent is submisison
        update comment_count field and save it.
        If parent is comment post it as child comment
        :param author: RedditUser instance
        :type author: RedditUser
        :param raw_comment: Raw comment text
        :type raw_comment: str
        :param parent: Comment or Submission that this comment is child of
        :type parent: Comment | Submission
        :return: New Comment instance
        :rtype: Comment
        """

        html_comment = mistune.markdown(raw_comment)
        # todo: any exceptions possible?
        comment = cls(author=author,
                      author_name=author.user.username,
                      raw_comment=raw_comment,
                      html_comment=html_comment)

        if isinstance(parent, Submission):
            submission = parent
            comment.submission = submission
        elif isinstance(parent, Comment):
            submission = parent.submission
            comment.submission = submission
            comment.parent = parent
        else:
            return
        submission.comment_count += 1
        submission.save()

        return comment

    def __unicode__(self):
        return "<Comment:{}>".format(self.id)


class Vote(models.Model):
    user = models.ForeignKey(RedditUser)
    submission = models.ForeignKey(Submission)
    vote_object_type = models.ForeignKey(ContentType)
    vote_object_id = models.PositiveIntegerField()
    vote_object = GenericForeignKey('vote_object_type', 'vote_object_id')
    value = models.IntegerField(default=0)

    @classmethod
    def create(cls, user, vote_object, vote_value):
        """
        Create a new vote object and return it.
        It will also update the ups/downs/score fields in the
        vote_object instance and save it.

        :param user: RedditUser instance
        :type user: RedditUser
        :param vote_object: Instance of the object the vote is cast on
        :type vote_object: Comment | Submission
        :param vote_value: Value of the vote
        :type vote_value: int
        :return: new Vote instance
        :rtype: Vote
        """

        if isinstance(vote_object, Submission):
            submission = vote_object
            vote_object.author.link_karma += vote_value
        else:
            submission = vote_object.submission
            vote_object.author.comment_karma += vote_value

        # update total vote count on RedditUser model
        vote_object.author.update_total_karma()

        vote = cls(user=user,
                   vote_object=vote_object,
                   value=vote_value)

        vote.submission = submission
        # the value for new vote will never be 0
        # that can happen only when removing up/down vote.
        vote_object.score += vote_value
        if vote_value == 1:
            vote_object.ups += 1
        elif vote_value == -1:
            vote_object.downs += 1


        vote_object.save()
        vote_object.author.save()

        return vote

    def change_vote(self, new_vote_value):
        if self.value == -1 and new_vote_value == 1:  # down to up
            vote_diff = 2
            self.vote_object.score += 2
            self.vote_object.ups += 1
            self.vote_object.downs -= 1
        elif self.value == 1 and new_vote_value == -1:  # up to down
            vote_diff = -2
            self.vote_object.score -= 2
            self.vote_object.ups -= 1
            self.vote_object.downs += 1
        elif self.value == 0 and new_vote_value == 1:  # canceled vote to up
            vote_diff = 1
            self.vote_object.ups += 1
            self.vote_object.score += 1
        elif self.value == 0 and new_vote_value == -1:  # canceled vote to down
            vote_diff = -1
            self.vote_object.downs += 1
            self.vote_object.score -= 1
        else:
            return None

        if isinstance(self.vote_object, Submission):
            self.vote_object.author.link_karma += vote_diff
        else:
            self.vote_object.author.comment_karma += vote_diff

        # update total vote count on RedditUser model
        self.vote_object.author.update_total_karma()

        self.value = new_vote_value
        self.vote_object.save()
        self.vote_object.author.save()
        self.save()

        return vote_diff

    def cancel_vote(self):
        if self.value == 1:
            vote_diff = -1
            self.vote_object.ups -= 1
            self.vote_object.score -= 1
        elif self.value == -1:
            vote_diff = 1
            self.vote_object.downs -= 1
            self.vote_object.score += 1
        else:
            return None

        if isinstance(self.vote_object, Submission):
            self.vote_object.author.link_karma += vote_diff
        else:
            self.vote_object.author.comment_karma += vote_diff

        # update total vote count on RedditUser model
        self.vote_object.author.update_total_karma()

        self.value = 0
        self.save()
        self.vote_object.save()
        self.vote_object.author.save()
        return vote_diff
