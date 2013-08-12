# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Origin'
        db.create_table(u'hubs_origin', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'hubs', ['Origin'])

        # Adding model 'Stream'
        db.create_table(u'hubs_stream', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('origin', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hubs.Origin'], null=True, blank=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('stream', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('content_path', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('content_encoding', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('md5', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
            ('size', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('started', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('ended', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'hubs', ['Stream'])


    def backwards(self, orm):
        # Deleting model 'Origin'
        db.delete_table(u'hubs_origin')

        # Deleting model 'Stream'
        db.delete_table(u'hubs_stream')


    models = {
        u'hubs.origin': {
            'Meta': {'object_name': 'Origin'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'hubs.stream': {
            'Meta': {'ordering': "('-modified',)", 'object_name': 'Stream'},
            'content_encoding': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'content_path': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'ended': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'md5': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'origin': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hubs.Origin']", 'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'started': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'stream': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['hubs']