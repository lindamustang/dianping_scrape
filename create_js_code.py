def create_js_code(url):
    js_code = 'setTimeout(() => {\nconsole.log("the code is working!!!");\nwindow.location = ' + url + '},10000);'
    return js_code

def js_code():
    with open('urls', 'r', newline='') as f:
        url = f.readline().replace('\n', '')
        url = '"' + '/shop/' + url + '"'
        all_lines = f.readlines()
    with open('urls', 'w', newline='') as fn:
        fn.writelines(all_lines)
    return_code = create_js_code(url)
    return return_code


