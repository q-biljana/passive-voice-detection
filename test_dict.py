


def find(key, dictionary):
    for k, v in dictionary.items():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in find(key, d):
                    yield result

example = {'app_url': '', 'models': [{'perms': {'add': True, 'change': True, 'delete': True}, 'add_url': '/admin/cms/news/add/', 'admin_url': '/admin/cms/news/', 'name': ''}], 'has_module_perms': True, 'name': u'CMS'}

example2 = {"bulkText":
[{"4561079":{"text":"hello tst hellot tree test"}},
{"4561127":{"text":"hello tst hellotst"}},
{"4561128":{"text":"hello tst hellotst"}}]}
print (list(find('text', example2)))
