from rest_framework import serializers
from .models import CustomUser, UserActivityLog

class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle CustomUser"""
    password = serializers.CharField(write_only=True, required=False, min_length=8)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 
                 'role', 'is_active', 'password', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = CustomUser.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class UserActivityLogSerializer(serializers.ModelSerializer):
    """Serializer pour les logs d'activité utilisateur"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    
    class Meta:
        model = UserActivityLog
        fields = ['id', 'user', 'user_username', 'action', 'action_display', 
                 'description', 'ip_address', 'timestamp']
        read_only_fields = ['id', 'timestamp']
