from posts.models import *
from rest_framework import serializers
from users.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	date = serializers.SerializerMethodField()

	class Meta:
		model = Comment
		fields = ['id', 'user', 'date', 'content']

	def get_date(self, obj):
		return obj.date.strftime('%Y-%m-%d %H:%M')


class PostSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	date = serializers.SerializerMethodField()
	area = serializers.SerializerMethodField()
	field = serializers.SerializerMethodField()
	scrapped = serializers.SerializerMethodField()
	comment_cnt = serializers.SerializerMethodField()

	class Meta:
		model = Post
		fields = ['id', 'user', 'date', 'area', 'field', 'content', 'scrapped', 'comment_cnt']

	def get_date(self, obj):
		return obj.date.strftime('%Y-%m-%d %H:%M')

	def get_area(self, obj):
		return obj.area.get_full_name()

	def get_field(self, obj):
		return str(obj.field)

	def get_scrapped(self, obj):
		return obj.scrapped

	def get_comment_cnt(self, obj):
		return Comment.objects.filter(post=obj).count()


class SidoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Sido
		fields = ['id', 'name']


class SigunguSerializer(serializers.ModelSerializer):
	class Meta:
		model = Sigungu
		fields = ['id', 'name']


class ScrapSerializer(serializers.ModelSerializer):
	class Meta:
		model = Scrap
		fields = ['user', 'post']
