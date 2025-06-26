from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from authentication.models import User, UserProfile


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True,
                                    validators=[UniqueValidator(
                                        queryset=User.objects.all(),
                                          message="This email is already in use."
                                          )])
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
    
    
class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'first_name', 'last_name', 'bio', 'words_count_learned')
        read_only_fields = ('username', 'user')

    def create(self, validated_data):
        user = self.context['request'].user
        user_profile = UserProfile.objects.create(user=user, **validated_data)
        return user_profile
    
    def get_username(self, obj):
        return obj.user.username if obj.user else None
