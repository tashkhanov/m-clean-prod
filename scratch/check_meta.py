import urllib.request

r = urllib.request.urlopen('http://127.0.0.1:8000/services/chistka-bilyardnogo-stola/')
html = r.read().decode('utf-8')

idx = html.find('<title>')
end = html.find('</title>')
print('TITLE:', html[idx:end+8])

idx2 = html.find('name="description"')
print('DESC:', html[idx2:idx2+300])

idx3 = html.find('aria-label')
if idx3 > -1:
    print('ARIA:', html[idx3:idx3+100])
else:
    print('ARIA: not found')
