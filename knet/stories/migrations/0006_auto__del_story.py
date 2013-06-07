# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Story'
        db.delete_table('stories_story')


    def backwards(self, orm):
        # Adding model 'Story'
        db.create_table('stories_story', (
            ('submitter_email', self.gf('django.db.models.fields.EmailField')(max_length=254, blank=True)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(related_name='old_stories', to=orm['teachers.TeacherProfile'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('submitter_name', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('private', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('stories', ['Story'])


    models = {
        
    }

    complete_apps = ['stories']