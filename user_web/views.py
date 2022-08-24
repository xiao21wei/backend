import json
import time

import simplejson as simplejson
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from user_web.models import UserWebUser, Code, Element, ProjectDocument, Room, Folder, OtherDocument, Project, Test, \
    Test1
from utils.send_code import send_sms_code
from utils.token import create_token
from utils.token import get_username
from utils.tools import valid_username, valid_password, random_room


@csrf_exempt  # 跨域设置
def register(request):  # 继承请求类
    if request.method == 'POST':  # 判断请求方式是否为 POST（要求POST方式）
        req = simplejson.loads(request.body)
        print(req)
        username = req['username']  # 获取请求数据
        password_1 = req['password_1']
        password_2 = req['password_2']
        e_mail = req['email']
        code = req['code']
        nickname = req['name']

        if valid_username(username):
            if valid_password(password_1):
                if password_1 == password_2:
                    email_code = Code.objects.filter(mail=e_mail, code=code)
                    print(email_code.first())
                    if email_code.exists():
                        user1 = UserWebUser.objects.filter(user_name=username)
                        if user1.exists():
                            return JsonResponse({'errno': 1006, 'msg': "用户名已注册"})

                        user = UserWebUser()
                        user.user_name = username
                        user.pass_word = password_1
                        user.mail = e_mail
                        user.real_name = nickname
                        user.status = 'offline'
                        user.save()
                        return JsonResponse({'errno': 0, 'msg': "注册成功"})
                    else:
                        return JsonResponse({'errno': 1001, 'msg': "验证码不正确"})
                else:
                    return JsonResponse({'errno': 1002, 'msg': "两次输入的密码不同"})
            else:
                return JsonResponse({'errno': 1003, 'msg': "密码不合法"})
        else:
            return JsonResponse({'errno': 1004, 'msg': "用户名不合法"})
    else:
        return JsonResponse({'errno': 1005, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def check_mail(request):
    if request.method == 'POST':
        req = simplejson.loads(request.body)
        print(req)
        e_mail = req['email']
        print(e_mail)
        if e_mail is None:
            return JsonResponse({'errno': 2002, 'msg': "验证码发送失败"})
        user = UserWebUser.objects.filter(mail=e_mail)
        if user.exists():
            return JsonResponse({'errno': 2001, 'msg': "邮箱已注册"})
        res_email = send_sms_code(e_mail)
        if res_email:
            return JsonResponse({'errno': 0, 'msg': "验证码发送成功，请前往邮箱查收"})
        return JsonResponse({'errno': 2002, 'msg': "验证码发送失败"})
    else:
        return JsonResponse({'errno': 2003, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def login(request):  # 继承请求类
    if request.method == 'POST':  # 判断请求方式是否为 POST（要求POST方式）
        username = request.POST.get('username')
        password = request.POST.get('password')
        # req = simplejson.loads(request.body)
        # username = req['username']
        # password = req['password']
        print(username)
        print(password)
        user1 = UserWebUser.objects.filter(user_name=username)
        if user1.exists():
            user = user1.first()
            if user.status == 'offline':
                if user.pass_word == password:
                    user.status = 'online'
                    user.save()
                    token = create_token(username)
                    return JsonResponse({
                        'errno': 0,
                        'msg': "登录成功",
                        'data': {
                            'username': user.user_name,
                            'authorization': token
                        }
                    })
                else:
                    return JsonResponse({'errno': 3001, 'msg': "密码不正确"})
            else:
                return JsonResponse({'errno': 3004, 'msg': "用户已登录"})
        else:
            return JsonResponse({'errno': 3002, 'msg': "用户名不存在"})
    else:
        return JsonResponse({'errno': 3003, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def logout(request):  # 继承请求类
    if request.method == 'POST':  # 判断请求方式是否为 POST（要求POST方式）
        token = request.META.get("HTTP_AUTHORIZATION")
        username = get_username(token)
        print(username)
        if username is not None:
            user2 = UserWebUser.objects.get(user_name=username)
            if user2.status == 'online':
                user2.status = 'offline'
                user2.save()

                return JsonResponse({'errno': 0, 'msg': "登出成功"})
            else:
                return JsonResponse({'errno': 4001, 'msg': "用户已下线"})
        else:
            return JsonResponse({'errno': 6001, 'msg': "当前无用户登录"})
    else:
        return JsonResponse({'errno': 4002, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def get_user(request):
    if request.method == 'POST':
        token = request.META.get("HTTP_AUTHORIZATION")
        try:
            username = get_username(token)
        except IndexError:
            return JsonResponse({'errno': 5003, 'msg': "未接收到token信息"})

        if username is not None:
            user = UserWebUser.objects.get(user_name=username)
            username = user.user_name
            name = user.real_name
            user_id = user.user_id
            phone = user.phone
            mail = user.mail
            print(username)
            print(user_id)
            print(name)
            print(phone)
            print(mail)
            return JsonResponse({'errno': 0, 'msg': "success",
                                 'data': {'user_id': user_id, 'username': username, 'name': name, 'phone': phone, 'mail':mail}})
        else:
            return JsonResponse({'errno': 5001, 'msg': "当前无用户登录"})

    else:
        return JsonResponse({'errno': 5002, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def update_user(request):
    if request.method == "POST":
        req = simplejson.loads(request.body)
        new_name = req['new_name']
        new_phone = req['new_phone']

        token = request.META.get("HTTP_AUTHORIZATION")
        try:
            username = get_username(token)
        except IndexError:
            return JsonResponse({'errno': 5003, 'msg': "未接收到token信息"})

        if username is not None:
            user = UserWebUser.objects.get(user_name=username)
            user.phone = new_phone
            user.real_name = new_name
            user.save()
            return JsonResponse({'errno': 0, 'msg': "修改信息成功", 'username': user.user_name})
        else:
            return JsonResponse({'errno': 6001, 'msg': "当前无用户登录"})
    else:
        return JsonResponse({'errno': 6002, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def save_element(request):
    if request.method == "POST":
        element_list = request.POST.getlist('list', [])
        custom_id = element_list[0]
        print(custom_id)
        print(len(element_list))
        print(element_list)
        if len(element_list) == 8:
            element1 = Element.objects.filter(custom_id=custom_id)
            if element1.exists():
                element = element1.first()
            else:
                element = Element()
            element.custom_id = element_list[0]
            element.prototype_id = element_list[1]
            element.width = element_list[2]
            element.height = element_list[3]
            element.x = element_list[4]
            element.y = element_list[5]
            element.element_type = element_list[6]
            element.rotation = element_list[7]
            element.save()
            return JsonResponse({'errno': 0, 'msg': "上传成功"})
        else:
            return JsonResponse({'errno': 7001, 'msg': "元素参数个数不正确"})
    else:
        return JsonResponse({'errno': 7002, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def delete_element(request):
    if request.method == "POST":
        custom_id = request.POST.get('custom_id')
        element = Element.objects.get(custom_id=custom_id)
        if element is None:
            return JsonResponse({'errno': 8001, 'msg': "组件不存在"})
        element.delete()
        return JsonResponse({'errno': 0, 'msg': "组件删除成功"})
    else:
        return JsonResponse({'errno': 8002, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def create_document(request):
    if request.method == "POST":
        req = simplejson.loads(request.body)
        project_id = req['project_id']
        folder_id = req['folder_id']
        title = req['title']
        content = req['content']
        document_type = req['document_type']
        if document_type == "project_document":
            project = Project.objects.filter(project_id=project_id)
            if not project.exists():
                return JsonResponse({'errno': 9004, 'msg': "项目不存在"})
            document1 = ProjectDocument.objects.filter(project_id=project_id, title=title)
            if document1.exists():
                return JsonResponse({'errno': 9001, 'msg': "文档名重复"})

            room_name = random_room()
            room = Room.objects.filter(room_name=room_name)
            while room is None:
                room_name = random_room()
                room = Room.objects.filter(room_name=room_name)
            room1 = Room()
            room1.room_name = room_name
            room1.save()

            document = ProjectDocument()
            document.project_id = project_id
            document.room_name = room_name
            document.title = title
            document.content = content
            document.open_type = 'first'
            document.save()
            return JsonResponse({'errno': 0, 'msg': "文档创建成功", 'room_name': room_name, 'type': 'project_document'})
        elif document_type == "other_document":
            folder = Folder.objects.filter(folder_id=folder_id)
            if not folder.exists():
                return JsonResponse({'errno': 9005, 'msg': "文件夹不存在"})
            document1 = OtherDocument.objects.filter(folder_id=folder_id, title=title)
            if document1.exists():
                return JsonResponse({'errno': 9001, 'msg': "文档名重复"})

            room_name = random_room()
            room = Room.objects.filter(room_name=room_name)
            while room is None:
                room_name = random_room()
                room = Room.objects.filter(room_name=room_name)
            room1 = Room()
            room1.room_name = room_name
            room1.save()

            document = OtherDocument()
            document.folder_id = folder_id
            document.room_name = room_name
            document.title = title
            document.content = content
            document.open_type = 'first'
            document.save()
            return JsonResponse({'errno': 0, 'msg': "文档创建成功", 'room_name': room_name, 'document_type': document_type})
        else:
            return JsonResponse({'errno': 9003, 'msg': "文档类型不正确"})
    else:
        return JsonResponse({'errno': 9002, 'msg': "请求方式错误"})


@csrf_exempt
def open_document(request):
    if request.method == "POST":
        req = simplejson.loads(request.body)
        document_id = req['document_id']
        document_type = req['document_type']
        if document_type == "project_document":
            document1 = ProjectDocument.objects.filter(document_id=document_id)
        elif document_type == "other_document":
            document1 = OtherDocument.objects.filter(document_id=document_id)
        else:
            return JsonResponse({'errno': 10003, 'msg': "文档类型不正确"})
        if document1.exists():
            document = document1.first()
            if document.open_type == "first":
                content = document.content
                document.open_type = None
            else:
                content = None
            room_name = document.room_name
            return JsonResponse({'errno': 0, 'msg': "文档打开成功", 'room_name': room_name, 'content': content})
        else:
            return JsonResponse({'errno': 10001, 'msg': "未查询到文档信息"})
    else:
        return JsonResponse({'errno': 10002, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def delete_document(request):
    if request.method == "POST":
        req = simplejson.loads(request.body)
        document_id = req['document_id']
        document_type = req['document_type']
        if document_type == "project_document":
            document1 = ProjectDocument.objects.filter(document_id=document_id)
        elif document_type == "other_document":
            document1 = OtherDocument.objects.filter(document_id=document_id)
        else:
            return JsonResponse({'errno': 11003, 'msg': "文档类型不正确"})

        if document1.exists():
            document = document1.first()
            document.delete()

            room_name = document.room_name
            room = Room.objects.filter(room_name=room_name)
            room1 = room.first()
            room1.delete()

            return JsonResponse({'errno': 0, 'msg': "文档删除成功"})
        else:
            return JsonResponse({'errno': 11001, 'msg': "未查询到文档信息"})
    else:
        return JsonResponse({'errno': 11002, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def create_folder(request):
    if request.method == "POST":
        req = simplejson.loads(request.body)
        team_id = req['team_id']
        folder_name = req['folder_name']
        folder1 = Folder.objects.filter(team_id=team_id, folder_name=folder_name)
        if folder1.exists():
            return JsonResponse({'errno': 12001, 'msg': "文件夹名重复"})
        folder = Folder()
        folder.folder_name = folder_name
        folder.team_id = team_id
        folder.save()
        return JsonResponse({'errno': 0, 'msg': "文件夹创建成功", 'folder_name': folder_name})
    else:
        return JsonResponse({'errno': 12002, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def delete_folder(request):
    if request.method == "POST":
        req = simplejson.loads(request.body)
        folder_id = req['folder_id']
        folder = Folder.objects.filter(folder_id=folder_id)
        if not folder.exists():
            return JsonResponse({'errno': 13001, 'msg': "文件夹不存在"})
        document = OtherDocument.objects.filter(folder_id=folder_id)
        for d in document:
            d.delete()
        folder1 = folder.first()
        folder1.delete()
        return JsonResponse({'errno': 0, 'msg': "文件夹删除成功"})
    else:
        return JsonResponse({'errno': 13002, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def try_prototype(request):
    if request.method == "POST":
        req = json.loads(request.body)
        test = Test()
        test.content = req
        test.save()
        return JsonResponse({'errno': 0, 'mag': "success", 'test_id': test.id, 'data': test.content})
    else:
        return JsonResponse({'errno': 13002, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def get_prototype(request):
    if request.method == "POST":
        req = simplejson.loads(request.body)
        test_id = req['id']

        test = Test.objects.filter(id=test_id)
        if test.exists():
            test1 = test.first()
            return JsonResponse(
                {'errno': 0,
                 'mag': "success",
                 'id': test1.id,
                 'title': test1.title,
                 'data': test1.content
                 })
        else:
            return JsonResponse({'errno': 14001, 'msg': "原型图不存在"})
    else:
        return JsonResponse({'errno': 14002, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def update_document(request):
    if request.method == "POST":
        req = simplejson.loads(request.body)
        project_id = req['project_id']
        folder_id = req['folder_id']
        open_type = req['open_type']
        content = req['content']
        document_id = req['document_id']
        document_type = req['document_type']
        if document_type == "project_document":
            project = Project.objects.filter(project_id=project_id)
            if not project.exists():
                return JsonResponse({'errno': 15004, 'msg': "项目不存在"})
            document2 = ProjectDocument.objects.filter(document_id=document_id)
            document = document2.first()
            document.open_type = open_type
            document.content = content
            document.save()
            return JsonResponse({'errno': 0, 'msg': "文档重命名成功", 'room_name': document.room_name})

        elif document_type == "other_document":
            folder = Folder.objects.filter(folder_id=folder_id)
            if not folder.exists():
                return JsonResponse({'errno': 15005, 'msg': "文件夹不存在"})
            document2 = OtherDocument.objects.filter(document_id=document_id)
            document = document2.first()
            document.save()
            return JsonResponse({'errno': 0, 'msg': "文档重命名成功", 'room_name': document.room_name})
        else:
            return JsonResponse({'errno': 15003, 'msg': "文档类型不正确"})
    else:
        return JsonResponse({'errno': 15002, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def update_prototype(request):
    if request.method == "POST":
        req = json.loads(request.body)
        test_id = req['test_id']
        title = req['title']
        content = req['data']
        project_id = req['project_id']
        test1 = Test.objects.filter(id=test_id)
        if not test1.exists():
            return JsonResponse({'errno': 16002, 'msg': "文件不存在"})
        test2 = test1.first()
        test2.project_id = project_id
        test2.title = title
        test2.content = content
        test2.save()
        return JsonResponse({'errno': 0, 'msg': "修改文件信息成功"})
    else:
        return JsonResponse({'errno': 16003, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def check_document(request):
    if request.method == "POST":
        req = json.loads(request.body)
        project_id = req['project_id']
        title = req['title']
        data = req['data']
        test = Test1()
        test.content = data
        test.title = title
        test.project_id = project_id
        test.save()
        return JsonResponse({'errno': 0, 'msg': "保存成功", 'data': test.content})
    else:
        return JsonResponse({'errno': 17001, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def delete_prototype(request):
    if request.method == "POST":
        req = simplejson.loads(request.body)
        test_id = req['test_id']
        test = Test.objects.filter(id=test_id)
        if test.exists():
            test.delete()
            return JsonResponse({'errno': 0, 'msg': "删除成功"})
        else:
            return JsonResponse({'errno': 18001, 'msg': "原型图不存在"})
    else:
        return JsonResponse({'errno': 18002, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def update_title(request):
    if request.method == "POST":
        req = simplejson.loads(request.body)
        project_id = req['project_id']
        folder_id = req['folder_id']
        new_title = req['new_title']
        document_id = req['document_id']
        document_type = req['document_type']
        if document_type == "project_document":
            project = Project.objects.filter(project_id=project_id)
            if not project.exists():
                return JsonResponse({'errno': 19004, 'msg': "项目不存在"})
            document1 = ProjectDocument.objects.filter(project_id=project_id, title=new_title)
            if document1.exists():
                return JsonResponse({'errno': 19001, 'msg': "文档名重复"})
            document2 = ProjectDocument.objects.filter(document_id=document_id)
            document = document2.first()
            document.title = new_title
            document.save()
            return JsonResponse({'errno': 0, 'msg': "文档重命名成功", 'room_name': document.room_name})

        elif document_type == "other_document":
            folder = Folder.objects.filter(folder_id=folder_id)
            if not folder.exists():
                return JsonResponse({'errno': 19005, 'msg': "文件夹不存在"})
            document1 = OtherDocument.objects.filter(folder_id=folder_id, title=new_title)
            if document1.exists():
                return JsonResponse({'errno': 19001, 'msg': "文档名重复"})
            document2 = OtherDocument.objects.filter(document_id=document_id)
            document = document2.first()
            document.title = new_title
            document.save()
            return JsonResponse({'errno': 0, 'msg': "文档重命名成功", 'room_name': document.room_name})
        else:
            return JsonResponse({'errno': 19003, 'msg': "文档类型不正确"})
    else:
        return JsonResponse({'errno': 19002, 'msg': "请求方式错误"})
