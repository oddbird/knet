# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Story.profile'
        db.add_column('stories_story', 'profile',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='stories', to=orm['teachers.TeacherProfile'], null=True),
                      keep_default=False)


        # Changing field 'Story.teacher'
        db.alter_column('stories_story', 'teacher_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.User'], null=True))

    def backwards(self, orm):
        # Deleting field 'Story.profile'
        db.delete_column('stories_story', 'profile_id')


        # Changing field 'Story.teacher'
        db.alter_column('stories_story', 'teacher_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.User'], default=1))

    models = {
        'accounts.user': {
            'Meta': {'object_name': 'User'},
            'bio': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'name': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'db_table': "'django_content_type'", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'stories.story': {
            'Meta': {'object_name': 'Story'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stories'", 'to': "orm['teachers.TeacherProfile']", 'null': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'submitter_email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '254'}),
            'submitter_name': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'teacher': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stories'", 'to': "orm['accounts.User']", 'null': 'True'})
        },
        'teachers.teacherprofile': {
            'Meta': {'object_name': 'TeacherProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'school': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'teacher_profile'", 'to': "orm['accounts.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['stories']