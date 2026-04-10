import requests, re, json

r2 = requests.get('http://localhost:8000/static/js/calculator.js')
js = r2.text

# Check if renderItems function looks correct
idx = js.find('function renderItems')
print('=== renderItems function ===')
print(js[idx:idx+400])

# Now check the REAL issue - does initAccordion run AFTER renderFurniture?
# Find both calls at the end
idx2 = js.rfind('renderFurniture()')
print('\n=== INIT SEQUENCE ===')
print(js[idx2:idx2+200])

# Check if there's an error in services-data that breaks early
# Check early return conditions
early_returns = [m.start() for m in re.finditer(r'if \(!servicesEl\)', js)]
print('\n=== Early returns ===')
for pos in early_returns:
    print(js[pos:pos+80])

# Check if isSingleService is correctly detected
idx3 = js.find("var isSingleService")
print('\n=== isSingleService ===')
print(js[idx3:idx3+200])

# THE KEY: Check if calc_type = 'furniture' makes activeCalcType = 'furniture'
idx4 = js.find("svc.calc_type === 'carpet'")
print('\n=== calc_type routing ===')
print(js[idx4-50:idx4+300])

# Check if furn-home display is set 
idx5 = js.find("fh.style.display")
if idx5 > 0:
    print('\n=== fh.style.display ===')
    print(js[idx5-50:idx5+200])
else:
    # Maybe it uses fh && fb
    idx5 = js.find("if (fh && fb)")
    if idx5 > 0:
        print('\n=== fh && fb ===')
        print(js[idx5-20:idx5+300])
    else:
        idx5 = js.find("if (fh &&")
        if idx5 > 0:
            print('\n=== fh block ===')
            print(js[idx5-20:idx5+300])
