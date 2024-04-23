from rest_framework import serializers
from configs.models import User


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['username', 'name_uz', 'name_ru', 'name_en', 'password', 'role', 'parent', 'grade', 'children' ]

    
    def create(self, validated_data):
        parent = validated_data.get("parent", [])
        children = validated_data.get("children", [])

        if parent:
            validated_data.pop("parent")
        if children:
            validated_data.pop("children")

        user = User.objects.create_user(**validated_data)

        user.parent.add(*parent)
        user.children.add(*children)

        return user


# class UserCreateUpdateSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = ['username', 'name_uz', 'name_ru', 'name_en', 'password', 'role', 'parent', 'grade', 'children' ]
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if self.context['request'].user.is_superuser:
#             self.fields.pop('role')
#             self.fields.pop('grade')
#             self.fields.pop('parent')
#             self.fields.pop('children')



    # def create(self, validated_data):
    #     username = validated_data.get('username')
    #     password = validated_data.get('password')
    #     parent = validated_data.get("parent")
        
    #     user = User.objects.create_user(username, password)

    #     if parent:
    #         user.parent.add(*parent)

    #     return user