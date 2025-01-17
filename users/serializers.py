from rest_framework import serializers
from .models import CustomUser, Discipline, Match, PlayerSlot

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email', 
            'nickname', 'date_of_birth', 'gender', 
            'weight', 'weight_unit', 'height', 'height_unit', 
            'country', 'disability'
        ]

# Discipline Serializer
class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = [
            'id', 'name', 'favorite_position', 'dominant_foot', 
            'pace', 'defending', 'shooting', 'passing', 'dribbling', 
            'arm', 'chest', 'back', 'leg', 'strength', 'resistance', 
            'max_distance', 'pace_avg', 'level', 
            'forehand', 'backhand', 'tennis_level', 'created_at'
        ]


class PlayerSlotSerializer(serializers.ModelSerializer):
    player_username = serializers.SerializerMethodField()
    class Meta:
        model = PlayerSlot
        fields = '__all__'
        extra_fields = ['player_username']

    def get_player_username(self, obj):
        return obj.player.username if obj.player else None


class MatchSerializer(serializers.ModelSerializer):
    player_slots = PlayerSlotSerializer(many=True,read_only=True)
    team_1_players = serializers.SerializerMethodField()
    team_2_players = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = [
            'id', 
            'place', 
            'location_coordinates', 
            'date_time', 
            'player_count', 
            'formation', 
            'field_type', 
            'player_slots',
            'team_1_players',
            'team_2_players',
        ]

    def get_team_1_players(self, obj):
        return obj.player_slots.filter(team=1, player__isnull=False).count()

    def get_team_2_players(self, obj):
        return obj.player_slots.filter(team=2, player__isnull=False).count()
    
    def create(self, validated_data):
        match = super().create(validated_data)

        # Create player slots for team 1
        for slot_number in range(1, match.player_count + 1):
            PlayerSlot.objects.create(
                match=match,
                team=1,
                slot_number=slot_number
            )
        # Create player slots for team 2
        for slot_number in range(1, match.player_count + 1):
            PlayerSlot.objects.create(
                match=match,
                team=2,
                slot_number=slot_number
            )
        return match




class MatchDetailSerializer(serializers.ModelSerializer):
    player_slots = PlayerSlotSerializer(many=True)

    class Meta:
        model = Match
        fields = ['id', 'place', 'location_coordinates', 'date_time', 'player_count', 'formation', 'field_type', 'player_slots']

