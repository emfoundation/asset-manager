from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from ckeditor.fields import RichTextField
from model_utils import FieldTracker

from . import s3_utils
from . import strings

import mimetypes

import logging
logging.basicConfig(
    filename=settings.LOGFILE,
    level=logging.INFO,
    format=' %(asctime)s - %(levelname)s - %(message)s'
    )
# logging.disable(logging.CRITICAL)

# Create your models here.
class S3_Object(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


# ------------ Folders ------------ #

class Folder(S3_Object):
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    tracker = FieldTracker()

    def __str__(self):
        path = self.get_path()
        if path.startswith(settings.MEDIAFILES_LOCATION + '/'):
            path = path[6:]
        return path

    def get_path(self):
        """
        Returns an up to date Folder path based on its location in the Django \
        model.
        """
        if not self.parent:
            return settings.MEDIAFILES_LOCATION + '/' + self.name
        else:
            return self.parent.get_path() + '/' + self.name

    def get_files(self):
        return self.file_set.all()

    def get_all_ancestor_folders(self):
        """
        Returns a list of all the ancestors of a given folder, including the folder itself
        """
        if not self.parent:
            return [self]
        else:
            ancestors = self.parent.get_all_ancestor_folders()
            ancestors.append(self)
            return ancestors

    def is_new_parent_valid(self, new_parent):
        """
        Returns True if the new_parent Folder is a valid parent for this Folder,
        otherwise returns False
        """
        new_parent_ancestors = new_parent.get_all_ancestor_folders()
        if self in new_parent_ancestors:
            return False
        return True

# ------------ Tags ------------ #

class TagGroup(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', )

class Tag(models.Model):
    name = models.CharField(max_length=64)
    group = models.ForeignKey(TagGroup, on_delete=models.CASCADE)
    deprecated = models.BooleanField(default=False)

    def __str__(self):
        return self.group.name.title() + ' | ' + self.name

    class Meta:
        ordering = ('name', )

class ContinentTagGroup(models.Model):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=2, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', )

class CountryTag(models.Model):
    name = models.CharField(max_length=64)
    display_name = models.CharField(max_length=32, blank=True)
    code = models.CharField(max_length=3, null=True)
    continent = models.ForeignKey(ContinentTagGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.continent.name.title() + ' | ' + self.name

    class Meta:
        ordering = ('name', )

# ------------ Contributor ------------ #

class Contributor(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

# ------------ Collection ------------ #

class Collection(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

# ------------ LearnerJourney ------------ #

class LearnerJourney(models.Model):

    def get_s3_key(self, filename):
        return 'smf-prototype/thumbnails/' + filename

    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True, max_length=1024)
    duration = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Duration (hours)')
    thumbnail = models.ImageField(upload_to=get_s3_key, blank=True)

    def __str__(self):
        return self.name

# ------------ Question ------------ #

class Question(models.Model):

    def get_s3_key(self, filename):
        return 'smf-prototype/thumbnails/' + filename

    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True, max_length=1024)
    intro_title = models.TextField(blank=True, null=True, max_length=64)
    intro_text = models.TextField(blank=True, null=True, max_length=512)
    quote = models.TextField(blank=True, null=True, max_length=256)
    quote_source = models.TextField(blank=True, null=True, max_length=64)
    thumbnail = models.ImageField(upload_to=get_s3_key, blank=True)

    def __str__(self):
        return self.name

# ------------ Assets ------------ #

class Asset(S3_Object):

    def get_s3_key(self, filename):
        return str(self.parent.id) + '/' + filename

    name = models.CharField(max_length=64, help_text=strings.ASSET_NAME_HELPER)
    parent = models.ForeignKey(Folder, on_delete=models.CASCADE, help_text=strings.ASSET_PARENT_HELPER)
    file = models.FileField(upload_to=get_s3_key, blank=True, help_text=strings.ASSET_FILE_NAME_HELPER)
    link = models.URLField(blank=True)

    tags = models.ManyToManyField(Tag, blank=True)
    locations = models.ManyToManyField(CountryTag, blank=True)
    contributors = models.ManyToManyField(Contributor, blank=True)
    collections = models.ManyToManyField(Collection, blank=True)

    description = models.TextField(blank=True)
    duration = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Duration (mins)')
    creation_date = models.DateField(blank=True, null=True)
    copyright_info = models.TextField(blank=True)
    enabled = models.BooleanField(default=True)

    PROTOTYPE = 'PT'
    START_UP = 'SU'
    ACTIVE = 'AC'
    ON_MARKET = 'OM'
    PROJECT = 'PR'
    RESEARCH = 'RS'
    COMPLETE = 'CM'
    DISCONTINUED = 'DS'
    STATUS_CHOICES = (
        (PROTOTYPE, 'Prototype'),
        (START_UP, 'Start Up'),
        (ACTIVE, 'Active'),
        (ON_MARKET, 'On Market'),
        (PROJECT, 'Project'),
        (RESEARCH, 'Research'),
        (COMPLETE, 'Complete'),
        (DISCONTINUED, 'Discontinued'),
    )
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        blank=True,
        verbose_name='Status (Case Studies only)'
    )

    CASE_STUDY = 'CS'
    CO_PROJECT = 'CP'
    PAPER = 'PA'
    REPORT = 'RT'
    INFOGRAPHIC = 'IG'
    TEACHING_LEARNING = 'TL'
    OTHER = 'OT'

    TYPE_CHOICES = (
        (CASE_STUDY, 'Case study'),
        (CO_PROJECT, 'Co.Project'),
        (PAPER, 'Paper'),
        (REPORT, 'Report'),
        (INFOGRAPHIC, 'Infographic'),
        (TEACHING_LEARNING, 'Teaching & learning resource'),
        (OTHER, 'Other')
    )
    type_field = models.CharField(
        default=OTHER,
        max_length=2,
        choices = TYPE_CHOICES,
        verbose_name='Content Type'
    )

    IMAGE = 'IM'
    VIDEO = 'VI'
    PRESENTATION = 'PR'
    LINK = 'LN'
    AUDIO = 'AU'
    DOCUMENT = 'DO'

    FORMAT_CHOICES = (
        (IMAGE, 'Image'),
        (VIDEO, 'Video'),
        (PRESENTATION, 'Presentation'),
        (LINK, 'Web link'),
        (AUDIO, 'Audio'),
        (DOCUMENT, 'Document'),
        (OTHER, 'Other')
    )
    format = models.CharField(
        max_length=2,
        choices = FORMAT_CHOICES,
        default = OTHER,
        verbose_name='Format'
    )

    filetype = models.CharField(max_length=128, null=True)
    uploaded_at = models.DateTimeField(null=True)
    last_edit_at = models.DateTimeField(null=True)

    uploaded_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='asset_uploaded_by')
    last_edit_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='asset_last_edit_by')
    owner = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)

    tracker = FieldTracker()

    def __str__(self):
        return self.parent.get_path() + '/' + self.name

    def save(self, *args, **kwargs):

        # if first save
        if not self.id:
            self.update_filetype()

        # if a new file is uploaded, the filename will be updated whether or not the parent has changed
        elif self.tracker.has_changed('file'):
            old_s3_key = settings.MEDIAFILES_LOCATION + '/' + self.tracker.previous('file').name
            s3_utils.delete_s3_object(old_s3_key)
            # update filetype
            self.update_filetype()

        # but if a file is already attached, and the parent is changed, this must be handled manually
        elif self.file and self.tracker.has_changed('parent_id'):
            old_file_name = self.file.name
            self.file.name = str(self.parent.id) + '/' + self.get_filename()
            logging.info('Filename changed from {0} to {1}'.format(old_file_name, self.file.name))

            media_dir = settings.MEDIAFILES_LOCATION

            s3_utils.update_s3_key(media_dir + '/' + old_file_name, media_dir + '/' + self.file.name)

        super(Asset, self).save(*args, **kwargs)

    def get_path(self):
        return self.parent.get_path() + '/' + self.name
    get_path.short_description = 'Full Path'

    def get_filename(self):
        """
        Asset.file.name contains the full filepath, relative to MEDIAFILES_LOCATION ie 'parent_id/filename'
        To get just the filename, we split the string from the right, once, on first '/'
        """
        filename = self.file.name
        if '/' in filename:
            return filename.rsplit('/',1)[1]
        return filename

    def update_filetype(self):
        """
        Automatically update filetype field based on file field
        """
        if self.file:
            self.filetype = mimetypes.guess_type(self.get_filename())[0]
        else:
            self.filetype = ''

# ------------ Asset-LearnerJourney Through table (Chapter) ------------ #

class Chapter(models.Model):

    def get_s3_key(self, filename):
        return 'smf-prototype/thumbnails/' + filename

    def __str__(self):
        return 'Learner Journey: {} Asset: {} Position: {}'.format(
            self.learner_journey,
            self.asset,
            self.position
        )

    title = models.CharField(blank=True, null=True, max_length=128)
    description = models.TextField(blank=True, null=True, max_length=1024)
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT)
    content = RichTextField(blank=True, null=True)
    learner_journey = models.ForeignKey(LearnerJourney, on_delete=models.PROTECT)
    position = models.PositiveSmallIntegerField()
    thumbnail = models.ImageField(upload_to=get_s3_key, blank=True)


# ------------ Asset-Question Through table (Answer) ------------ #

class Answer(models.Model):

    def get_s3_key(self, filename):
        return 'smf-prototype/thumbnails/' + filename

    def __str__(self):
        return 'TITLE: {} --- QUESTION: {} --- ASSET: {} --- POSITION: {}'.format(
            self.title,
            self.question,
            self.asset,
            self.position
        )

    title = models.CharField(blank=True, null=True, max_length=128)
    tile_description = models.TextField(blank=True, null=True, max_length=256, help_text="Appears on Answer tile in the Question Page.")
    question_context = models.TextField(blank=True, null=True, max_length=512, help_text="Appears below Question name, in Banner on individual Answer Page.")
    description = models.TextField(blank=True, null=True, max_length=1024, help_text="Appears on individual Answer Page.")
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT)
    content = RichTextField(blank=True, null=True)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    position = models.PositiveSmallIntegerField(help_text="Choose the position that the Answer will appear in on the Question Page.")
    thumbnail = models.ImageField(upload_to=get_s3_key, blank=True, help_text="Background image used on Answer tile on Question Page.")
