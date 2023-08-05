import uuid 
import datetime

from multiselectfield import MultiSelectField

from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.db import models
from django.contrib.sites.models import Site

from .settings import app_settings


##################
# CHOICES
##################


class StatusChoices(models.IntegerChoices):
    OPEN = 1, _("Open")
    ACTIVE = 10, _("Active")
    HOLD = 20, _("Hold")
    CLOSED = 30, _("Closed")
    CANCELED = 40, _("Canceled")

class PriorityChoices(models.IntegerChoices):
    SUGGESTION = 1, _("Suggestion")
    LOW = 2, _("Low")
    MEDIUM = 3, _("Medium")
    HIGH = 4, _("High")
    URGENT = 5, _("Urgent")

class VisibilityChoices(models.IntegerChoices):
    REPORTERS = 1, _("Reporters")
    SUPPORT = 10, _("Support Handlers")
    DEVELOPERS = 15, _("Developers")
    SUPERVISORS = 20, _("Supervisors")


##################
# ABSTRACT MODELS
##################

class CreateUpdateModelBase(models.Model):
    created = models.DateTimeField("date created", auto_now_add=True)
    updated = models.DateTimeField("last updated", auto_now=True)

    class Meta:
        abstract = True

    def been_updated(self):
        return (self.updated - self.created) > datetime.timedelta(seconds=1)
    
##################
# MODELS
##################

class Team(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=30)
    global_team = models.BooleanField()
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    sites = models.ManyToManyField(Site, default=1)
    categories = MultiSelectField(choices=app_settings.TICKET_CATEGORIES.choices)

    def __str__(self):
        return self.name
    

class Ticket(CreateUpdateModelBase):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.IntegerField(_("Status"), default=StatusChoices.OPEN, choices=StatusChoices.choices)
    priority = models.IntegerField(_("Priority"), default=PriorityChoices.MEDIUM, choices=PriorityChoices.choices)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="support_tickets")
    user_meta = models.JSONField(blank=True, null=True, default=dict)
    category = models.IntegerField(_("Category"), choices=app_settings.TICKET_CATEGORIES.choices)
    teams = models.ManyToManyField(Team, blank=True, related_name="support_tickets")
    subject = models.CharField(_("Subject"), max_length=120)
    description = models.TextField(_("Description"))
    history = models.JSONField(blank=True, null=True, default=list)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="assigned_tickets")
    dev_ticket = models.CharField(max_length=30, blank=True, null=True)
    related_to = models.ManyToManyField("self", blank=True)
    site = models.ForeignKey(Site, default=1, on_delete=models.CASCADE)

    class Meta:
        permissions = (
            ("see-support-tickets", "Access to support-level tickets"), 
            ("see-developer-tickets", "Access to developer-level tickets"), 
            ("see-all-tickets", "Access to all tickets"),
        ) 

    def __str__(self):
        return "{0} - {1}".format(self.user.username, self.subject)

    def log_history_event(self, event, user=None, notes=None, isotime=None):
        '''
        "history": [
            {
                "time": "2020-04-08T23:45:02.225609+00:00",
                "event": "created"
            }
        ],
        '''
        if not isotime:
            isotime = timezone.now().isoformat()           # '2019-12-18T22:27:28.222000+00:00'

        event = {'event':event, 'time':isotime}

        if user:
            event['user'] = user.pk
            event['username'] = user.username

        if notes:
            event['notes'] = notes

        self.history.append(event)

    
class Comment(CreateUpdateModelBase):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    content = models.TextField(_("Content"))
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="comments")
    visibility = models.IntegerField(_("Visibility"), default=VisibilityChoices.REPORTERS, choices=VisibilityChoices.choices)

    def __str__(self):
        return "{0} - {1}".format(self.user.username, self.created)
