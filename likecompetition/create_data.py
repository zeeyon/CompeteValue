from posts.models import Post, Comment, City, Area
from users.models import User
import random

User.objects.all().delete()
for user_id in range(1, 11):
    user = User.objects.create_user(email='user%d@naver.com' % user_id, nickname='사용자 %d' % user_id, password='12345678')
    print(user)

City.objects.all().delete()
city_list = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주']
for city_name in city_list:
    city = City(name=city_name)
    city.save()
    print(city)
    for area_num in range(1, 4):
        area = Area(city=city, name='%s%d' % (city.name, area_num))
        area.save()
        print(area)

field_list = ['web', 'android', 'ios', 'game', 'ml', 'bigdata', 'iot', 'blockchain', 'vr', 'etc']
for post_id in range(1, 101):
    user = User.objects.filter(nickname='사용자 %d' % random.randint(1, 10))[0]
    city = City.objects.filter(name=random.choice(city_list))[0]
    area = Area.objects.filter(name='%s%d' % (city.name, random.randint(1, 3)))[0]
    r1 = random.randint(0, len(field_list)-1)
    r2 = random.randint(0, len(field_list)-1)
    while r1 == r2:
        r2 = random.randint(0, len(field_list)-1)
    post = Post(title='게시글 %d' % post_id, user=user, city=city, area=area, field='%s,%s' % (field_list[r1], field_list[r2]))
    post.save()
    print(post)
    for i in range(10):
        user = User.objects.filter(nickname='사용자 %d' % random.randint(1, 5))[0]
        content = '댓글 달고 갑니당 :3'
        comment = Comment(post=post, user=user, content=content)
        comment.save()

print('end')
