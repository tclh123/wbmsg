from web.template import CompiledTemplate, ForLoop, TemplateResult


# coding: utf-8
def base():
    __lineoffset__ = -5
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'<!DOCTYPE html>\n'])
    extend_([u'<html>\n'])
    extend_([u'<head>\n'])
    extend_([u'    <title></title>\n'])
    extend_([u'</head>\n'])
    extend_([u'<body>\n'])
    extend_([u'\n'])
    extend_([u'</body>\n'])
    extend_([u'</html>\n'])

    return self

base = CompiledTemplate(base, 'templates/base.html')
join_ = base._join; escape_ = base._escape

# coding: utf-8
def index (name):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'<b>hello, ', escape_(name, True), u'. test by web.py</b>\n'])

    return self

index = CompiledTemplate(index, 'templates/index.html')
join_ = index._join; escape_ = index._escape

# coding: utf-8
def readme():
    __lineoffset__ = -5
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'python web/template.py --compile templates\n'])

    return self

readme = CompiledTemplate(readme, 'templates/readme.txt')
join_ = readme._join; escape_ = readme._escape

# coding: utf-8
def test (content):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'<html>\n'])
    extend_([u'<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>\n'])
    extend_([u'<head>\n'])
    extend_([u'    <title>wbmsg</title>\n'])
    extend_([u'</head>\n'])
    extend_([u'<body>\n'])
    extend_([escape_(content, True), u'\n'])
    extend_([u'</body>\n'])
    extend_([u'</html>\n'])

    return self

test = CompiledTemplate(test, 'templates/test.html')
join_ = test._join; escape_ = test._escape

