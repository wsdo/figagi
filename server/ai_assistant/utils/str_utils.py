# 截取字符串的后半段
def tract_prefix(full_str, prefix):
    if prefix in full_str:
        return full_str.split(prefix, 1)[1]
    else:
        return full_str
