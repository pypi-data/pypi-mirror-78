"""
This is the standard way to include a multiple-line
comment in your code
"""
def print_lol(the_list):
    # 遍历列表
    for lol_list in the_list:
        # 如果元素为列表，递归重新遍历
        if (isinstance(lol_list, list)):
            print_lol(lol_list)
        else:
            print(lol_list)
