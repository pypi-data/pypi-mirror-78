"""
    UserAPITestCase
    ~~~~~~~~~

    基于 rest_framework APITestCase 的基础之上，支持以不同的用户身份进行接口测试。

    :copyright: 2020 Lawes
"""

import sys

from django.conf import settings
from rest_framework.schemas.generators import SchemaGenerator
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.test import APIClient
from rest_framework.test import APITestCase


class UserAPITestCase(APITestCase):
    """ 基于 rest_framework APITestCase 的基础之上，支持以不同的用户身份进行接口测试。 """

    def __init__(self, *args, **kwargs):
        """ 初始化会产生一个匿名用户 """

        # 注册之后的用户存放，格式：{ user_type：{ agency: APIClient1， agency2: APIClient2}， }
        self.type_users = {}

        # 注册匿名用户
        self.register_user(user_name='anonymous')

        # 需要 authorized 检测的接口
        self.path_unauthorized_conf = []

        # 存在需要屏蔽 forbidden 检测的端点
        self.forbidden_ignore = []
        # 需要 forbidden 检测的接口
        self.path_forbidden_conf = {}

        # 存在需要屏蔽 not_found 检测的端点
        self.not_found_ignore = []
        # 需要 not_found 检测的接口
        self.path_not_found_conf = {}

        super().__init__(*args, **kwargs)

    def register_user(self, *, user_name, http_authorization='', user_id=None, user_types='') -> None:
        """ 注册用户，注册完之后，可以以该用户的身份 post or get 操作。

        :param user_name:               用户的名字，注册完成之后，可以进行 self.{user_name}.post 操作
        :param http_authorization:      Authorization in reqests headers
        :param user_id:                 用户 id
        :param user_types:              用户类型，用于分类，多类型使用"," 分割。使用 get_users_by_user_type 获得该分类用户

        ..versionadded:: 0.1

        """
        obj = APIClient()
        obj.credentials(HTTP_AUTHORIZATION=http_authorization)
        obj.user_id = user_id
        obj.user_name = user_name
        setattr(self, user_name, obj)
        for user_type in user_types.split(','):
            self.type_users.setdefault(user_type, {})
            self.type_users[user_type][user_name] = obj

    def get_users_by_user_type(self, *, user_types) -> list:
        """ 根据用户类型， 获得所有的用户 """
        return list(self.type_users.get(user_types, []).values())

    @property
    def registered_users(self) -> list:
        """ 获得注册过的所有的用户  """
        results = set()
        for users in self.type_users.values():
            for user in users.values():
                results.add(user)
        return list(results)

    @property
    def endpoints(self) -> dict:
        """ 获得所有的端点

        return: {
            {path:method}: {callback}
        }
        """
        if not hasattr(self, '_path_method_conf'):
            self._path_method_conf = {}
            sg = SchemaGenerator()
            sg.get_schema()
            for path, method, callback in sg.endpoints:
                endpoint = path + ':' + method
                # 如果存在版本控制，遍历出所有的 version
                if '{version}' in path:
                    for allowed_versions in settings.REST_FRAMEWORK['ALLOWED_VERSIONS']:
                        version_endpoint = endpoint.replace('{version}', allowed_versions)
                        if version_endpoint not in self.path_unauthorized_conf:
                            version_path = path.replace('{version}', allowed_versions)
                            r = getattr(self.anonymous, method.lower())(version_path, )
                            if r.status_code == 404:
                                continue
                        self._path_method_conf[version_endpoint] = callback
                else:
                    self._path_method_conf[endpoint] = callback
        return self._path_method_conf

    def set_unauthorized(self, path, method) -> None:
        """ 设置不需要 authorized 认证的接口 """
        endpoint = path + ':' + method
        if not endpoint in self.endpoints:
            assert False, '不存在：{}'.format(endpoint)
        self.path_unauthorized_conf.append(endpoint)

    def is_valid_for_unauthorized(self) -> None:
        """ 遍历所有的用户，对所有的端点进行 unauthorized 检测 """

        for endpoint in self.endpoints:
            path, method = endpoint.split(':')
            method_function = getattr(self.anonymous, method.lower(), )
            path_replace = path.replace('{pk}', '1')
            try:
                status_code = method_function(path_replace, data={}).status_code
            except:
                status_code = 200

            # 需要 authorized 认证的接口
            if endpoint not in self.path_unauthorized_conf:
                # 匿名用户访问，返回非 401，警告
                if status_code not in (HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND):
                    sys.stderr.write('Unauthorized 警告：endpoint: {}:{}, 允许未认证用户访问，'
                                     '返回状态:{}.\n'.format(path, method, status_code))
            # 不需要 authorized 认证的接口
            else:
                # 匿名用户访问，返回 401，警告
                if status_code == HTTP_401_UNAUTHORIZED:
                    sys.stderr.write('Unauthorized 警告：endpoint: {}:{}, 不允许未认证用户访问，'
                                     '返回状态:{}.\n'.format(path, method, status_code))

    def add_forbidden_ignore(self, *, endpoint) -> None:
        """  设置需要屏蔽 forbidden 检测的端点
        :param endpoint:                需要屏蔽检测的端点，格式： {path}:{method}
        """
        self.forbidden_ignore.append(endpoint)

    def set_forbidden(self, path, method, exclude_auth_user) -> None:
        """ 为路由添加访问允许的用户 exclude_auth_user
        :param path:                    请求 url
        :param method:                  请求方法：'GET', 'PUT', 'POST'
        :param exclude_auth_user:       允许访问的用户
        :return:
        """
        endpoint = path + ':' + method
        if not endpoint in self.endpoints:
            assert False, '不存在：{}'.format(endpoint)
        self.path_forbidden_conf.setdefault(endpoint, [])
        if not isinstance(exclude_auth_user, list):
            exclude_auth_user = [exclude_auth_user]
        self.path_forbidden_conf[endpoint].extend([user.user_name for user in exclude_auth_user])

    def is_valid_for_forbidden(self) -> None:
        """ 遍历所有的端点, 进行 forbidden 检测。默认所有的路由不允许未认证的匿名用户访问
            如果允许匿名用户访问，请使用 set_unauthorized 进行申明
        """

        for endpoint in self.endpoints:
            if endpoint in self.forbidden_ignore:
                continue
            path, method = endpoint.split(':')
            # 遍历认证用户，检测权限
            for auth_user in self.registered_users:
                method_function = getattr(auth_user, method.lower(), )
                r = method_function(path, data={})
                if auth_user.user_name in self.path_forbidden_conf.get(endpoint, []):
                    if r.status_code == HTTP_403_FORBIDDEN:
                        sys.stderr.write('Forbidden 警告：endpoint: {}:{}, 用户: {} 访问限制, 返回状态:{}\n'.format(
                            path, method, auth_user.user_name, r.status_code))
                else:
                    if r.status_code not in [HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND]:
                        sys.stderr.write('Forbidden 警告：endpoint: {}:{}, 用户: {} 访问通过。返回状态:{}\n'.format(
                            path, method, auth_user.user_name, r.status_code))

    def add_not_found_ignore(self, *, endpoint) -> None:
        """  设置需要屏蔽 not_found 检测的端点

        :param endpoint:                需要屏蔽检测的端点，格式： {path}:{method}

        ..versionadded:: 0.1
        """
        self.not_found_ignore.append(endpoint)

    def set_found(self, path, method, auth_user, found_count=1) -> None:
        """ 为路由添加限制访问认证用户 auth_user
        :param path:        请求 url
        :param method:      请求方法：'GET', 'PUT', 'POST'
        :param auth_user:   认证用户
        :param found_count: 可以访问的资源公司
        :return:
        """
        endpoint = path + ':' + method
        if not endpoint in self.endpoints:
            assert False, '不存在：{}'.format(endpoint)
        self.path_not_found_conf.setdefault(endpoint, {})
        self.path_not_found_conf[endpoint][auth_user] = found_count

    def is_valid_for_not_found(self) -> None:
        """ 编辑检测所有的路由权限, 判断是否存在用户的限制访问. 只支持 ModelViewSet
        """

        for endpoint in self.endpoints:

            path, method = endpoint.split(':')
            # 遍历有 pk 识别的路由
            if '/{pk}/' not in path:
                continue

            if endpoint in self.not_found_ignore:
                continue

            callback = self.endpoints[endpoint]
            # 获得该路由对应的 model
            if not hasattr(callback.cls.serializer_class, 'Meta'):
                continue
            model = callback.cls.serializer_class.Meta.model
            # 获得现有的所有数据 pk
            pk_list = model._default_manager.all().values('pk', )
            pk_list = [pk['pk'] for pk in pk_list]

            if endpoint not in self.path_not_found_conf:
                msg = 'Not Found endpoint: {}, 需要进行 set_found 的申明\n'.format(endpoint)
                sys.stderr.write(msg)

            path_key_not_found_conf = {user: 0 for user in self.registered_users}
            if endpoint in self.path_not_found_conf:
                path_key_not_found_conf.update(self.path_not_found_conf[endpoint])
            # 遍历认证用户，检测访问资源不存在
            for auth_user in path_key_not_found_conf:
                count = path_key_not_found_conf[auth_user]
                status_code_200_list = []
                method_function = getattr(auth_user, method.lower(), )
                for pk in pk_list:
                    path_replace = path.replace('{pk}', str(pk))
                    r = method_function(path_replace, data={})
                    if r.status_code not in [HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND]:
                        status_code_200_list.append(auth_user)

                # 实际访问个数
                trust_count = len(status_code_200_list)
                if count != trust_count:
                    msg = 'Not Found 警告：endpoint: {}, 期望：只允许用户访问 {} 个该类资源, 实际用户访问 {} 个该类资源, auth_user: {}\n'.format(
                        endpoint, count, trust_count, auth_user.user_name
                    )
                    sys.stderr.write(msg)
