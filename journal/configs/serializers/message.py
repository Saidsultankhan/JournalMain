from rest_framework import serializers
from configs.models import Message
from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import AuthenticationFailed


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'
        

class MessageCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('text', 'conversation', 'reply_id')

    def create(self, validated_data):
        sender = self.context['request'].user
        validated_data.update(sender=sender)
        
        return Message.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.is_changed = True
        instance.save()
        
        return instance
