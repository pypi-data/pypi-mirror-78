JQUERY_JS = "admin/js/vendor/jquery/jquery.js"
JQUERY_INIT_JS = "admin/js/jquery.init.js"

def jquery_plugins(jslist):
    return [JQUERY_JS] + jslist + [JQUERY_INIT_JS]

