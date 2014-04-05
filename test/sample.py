import itertools

json_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
plugins_list = list(itertools.zip_longest(*[iter(json_list)]*3))

print(str(json_list))
print(str(plugins_list))
print(str(len(plugins_list)))

for _plugin in plugins_list:
    print(_plugin)
