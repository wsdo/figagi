import ldap
from ai_assistant.config.config import config 
from ai_assistant.utils.logger import create_logger

logger = create_logger('ldap_authectication')

def ldap_auth(username: str, password: str):
    if (not username or not password):
        return False

    try:
        # 建立连接
        ldapconn = ldap.initialize(config.LDAP_SERVER_URI)
        # 绑定管理账户，用于用户的认证
        ldapconn.simple_bind_s(config.LDAP_DEFAULT_ADMIN, config.LDAP_ADMIN_PASSWORD)
        searchScope = ldap.SCOPE_SUBTREE  # 指定搜索范围
        searchFilter = "(uid =%s)" % username   # 指定搜索字段
        # logger.info('search user: %s, %s', config.LDAP_SEARCH_BASE, searchFilter)
        # ldap_result = ldapconn.search_s(config.LDAP_SEARCH_BASE, searchScope, searchFilter, None)  # 返回该用户的所有信息，类型列表
        user_dn = f'uid={username},{config.LDAP_SEARCH_BASE}'   # 获取用户的cn,ou,dc
        try:
            ldapconn.simple_bind_s(user_dn, password)  # 对用户的密码进行验证
            return True
        except Exception as e:
            logger.info('login fail: user_dn: %s, username: %s', user_dn, username)
            logger.info(e)
            return False
        else:
            return False
    except Exception as e:
        logger.error(e)
        return False