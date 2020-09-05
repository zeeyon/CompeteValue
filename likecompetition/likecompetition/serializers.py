from rest_framework import serializers
from posts.models import Post, Comment
from users.models import User


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'nickname']


class CommentSerializer(serializers.ModelSerializer):
	user = UserSerializer()

	class Meta:
		model = Comment
		fields = ['id', 'user', 'content']


class PostSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	date = serializers.SerializerMethodField()
	city = serializers.SerializerMethodField()
	area = serializers.SerializerMethodField()
	field = serializers.SerializerMethodField()
	scrapped = serializers.SerializerMethodField()
	comments = CommentSerializer(many=True)

	class Meta:
		model = Post
		fields = ['id', 'title', 'user', 'date', 'city', 'area', 'field', 'content', 'scrapped', 'comments']

	def get_date(self, obj):
		return obj.date.strftime('%Y-%m-%d %H:%M')

	def get_city(self, obj):
		return obj.city.name

	def get_area(self, obj):
		return obj.area.name

	def get_field(self, obj):
		return str(obj.field)

	def get_scrapped(self, obj):
		return obj.scrapped
