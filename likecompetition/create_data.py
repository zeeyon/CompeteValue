from posts.models import Post, Comment, Sido, Sigungu
from users.models import User
import random

User.objects.all().delete()
for user_id in range(1, 11):
    user = User.objects.create_user(email='user%d@naver.com' % user_id, nickname='����� %d' % user_id, password='12345678')
    print(user)

Sido.objects.all().delete()
sido_list = ['����', '�λ�', '�뱸', '��õ', '����', '����', '���', '����', '���', '����', '���', '�泲', '����', '����', '���', '�泲', '����']
for sido_name in sido_list:
    sido = Sido(name=sido_name)
    sido.save()
    print(sido)
    for sigungu_num in range(1, 6):
        sigungu = Sigungu(sido=sido, name='%s%d' % (sido.name, sigungu_num))
        sigungu.save()
        print(sigungu)

field_list = ['web', 'android', 'ios', 'game', 'ml', 'bigdata', 'iot', 'blockchain', 'vr', 'etc']
for post_id in range(1, 101):
    user = User.objects.filter(nickname='����� %d' % random.randint(1, 10))[0]
    sido_name = random.choice(sido_list)
    area = Sigungu.objects.filter(name='%s%d' % (sido_name, random.randint(1, 5)))[0]
    r1 = random.randint(0, len(field_list)-1)
    r2 = random.randint(0, len(field_list)-1)
    while r1 == r2:
        r2 = random.randint(0, len(field_list)-1)
    post = Post(user=user, area=area, field='%s,%s' % (field_list[r1], field_list[r2]), content='���ſ� ������ǥ�� ������ ���� �� ���翡 ���� �繫�� ó���ϱ� ���Ͽ� ���Ű�������ȸ�� �д�. ������ ����깰�� ���ޱ����� ���뱸���� ������ ����Ͽ� ���ݾ����� ���������ν� �󡤾���� ������ ��ȣ�Ѵ�.\n������� ��3�װ� ��4���� ������ ��ü���� �����Ͽ��� �Ѵ�. �ٷ������� ������ �ΰ��� �������� �����ϵ��� ������ ���Ѵ�.')
    post.save()
    print(post)
    for i in range(10):
        user = User.objects.filter(nickname='����� %d' % random.randint(1, 10))[0]
        content = '��� �ް� ���ϴ� :3'
        comment = Comment(post=post, user=user, content=content)
        comment.save()

print('end')
