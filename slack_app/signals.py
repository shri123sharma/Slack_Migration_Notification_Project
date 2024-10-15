from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.shortcuts import render,HttpResponse
from django.core.management import call_command
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from io import StringIO
from django.core.management.commands.makemigrations import Command
from slackeventsapi import SlackEventAdapter 
import slack_sdk
import sys
import os


@receiver(post_migrate)
def my_callback(sender, **kwargs):
    slack_api_token = env('SLACK_API_TOKEN')
    channel_id = env('SLACK_CHANNEL_ID')

    # Initialize WebClient with the token
    client = WebClient(token=slack_api_token)
    try:
        message=[]
        if kwargs['plan']:
          # import pdb;pdb.set_trace()
          for detail in kwargs['plan']:
            migration_detail=detail[0]
            app_name=migration_detail.app_label
            migration_operation_detail=migration_detail.operations
            for operation_detail in migration_operation_detail:
                
                if operation_detail.__class__.__name__=="AddField":
                  print("add Field")
                  message.append("Field:-%s_%s_%s__%s" % (app_name,operation_detail.model_name,operation_detail.name,operation_detail.__class__.__name__))

                if operation_detail.__class__.__name__=='AlterField':
                   print('alter Field')
                   message.append("Field:-%s_%s_on_%s__%s" %(app_name,operation_detail.model_name,operation_detail.name,operation_detail.__class__.__name__))

                if operation_detail.__class__.__name__=="RemoveField":
                  print('remove field')
                  message.append("Field:-%s_%s_%s__%s" % (app_name,operation_detail.model_name,operation_detail.name,operation_detail.__class__.__name__))

                if operation_detail.__class__.__name__=="RenameField":
                  print('rename field')
                  message.append("Field:-%s_%s_%s to %s__%s" % (app_name,operation_detail.model_name,operation_detail.old_name,operation_detail.new_name,operation_detail.__class__.__name__))
                  print(message)

                if operation_detail.__class__.__name__=="CreateModel":
                      print('create table')
                      message.append("Table:-%s_%s__%s" % (app_name,operation_detail.name,operation_detail.__class__.__name__))

                if operation_detail.__class__.__name__=="RenameModel":
                  print('rename table')
                  message.append("Table:-%s_%s to %s__%s" % (app_name,operation_detail.old_name,operation_detail.new_name,operation_detail.__class__.__name__))

                if operation_detail.__class__.__name__=="DeleteModel":
                  print('Delete table')
                  message.append("Table:-%s_%s__%s" % (app_name,operation_detail.name,operation_detail.__class__.__name__))
  
            break
          response = client.chat_postMessage(channel=channel_id, text='\n'.join(message))
          print(response)
          sys.exit(0)
    except SlackApiError as e:
        print("Error sending message: ", e)
  