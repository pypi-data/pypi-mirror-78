from flask import request, url_for, render_template, Blueprint
from flask_api import FlaskAPI, status, exceptions
from flask_api.renderers import HTMLRenderer
from flask_api.decorators import set_renderers
from config import Config



app = FlaskAPI(__name__)
app.config.from_object(Config)

from socfaker import SocFaker

socfaker = SocFaker()

theme = Blueprint(
    'flask-api', __name__,
    url_prefix='/',
    template_folder='templates', static_folder='static'
)

app = FlaskAPI(__name__)
app.blueprints['flask-api'] = theme

@app.route("/", methods=['GET', 'POST'])
def index():
	return { 'value': 'Welcome to the SocFaker API!'}


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route("/site-map")
def site_map():
    links = []
    route_dict = {}
    product_dict = {}
    vuln_dict = {}
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            #if url.startswith('/products'):
            if url.startswith('/products/elastic/document'):
                if 'elastic' not in product_dict:
                    product_dict['elastic'] = []
                product_dict['elastic'].append({
                    'name': url.split('/products/elastic/document/fields')[1].replace('/',''),
                    'url': url
                })
            elif url.startswith('/products/azure/vm/details'):
                if 'azure' not in product_dict:
                    product_dict['azure'] = {}
                if 'details' not in product_dict['azure']:
                    product_dict['azure']['details'] = []
                product_dict['azure']['details'].append({
                    'name': url.split('/products/azure/vm/details')[1].replace('/',''),
                    'url': url
                })
            elif url.startswith('/products/azure/vm/metrics'):
                if 'azure' not in product_dict:
                    product_dict['azure'] = {}
                if 'metrics' not in product_dict['azure']:
                    product_dict['azure']['metrics'] = []
                product_dict['azure']['details'].append({
                    'name': url.split('/products/azure/vm/metrics')[1].replace('/',''),
                    'url': url
                })
            elif url.startswith('/products/azure/vm/topolgy'):
                if 'azure' not in product_dict:
                    product_dict['azure'] = {}
                if 'topology' not in product_dict['azure']:
                    product_dict['azure']['topology'] = []
                product_dict['azure']['topology'].append({
                    'name': url.split('/products/azure/vm/topology')[1].replace('/',''),
                    'url': url
                })
            elif url.startswith('/vulnerability/host'):
                if 'host' not in vuln_dict:
                    vuln_dict['host'] = []
                vuln_dict['host'].append({
                    'name': url.split('/vulnerability/host')[1].replace('/',''),
                    'url': url
                })
            elif url.startswith('/vulnerability/scan'):
                if 'scan' not in vuln_dict:
                    vuln_dict['scan'] = []
                vuln_dict['scan'].append({
                    'name': url.split('/vulnerability/scan')[1].replace('/',''),
                    'url': url
                })
            else:
                if url.lstrip('/').split('/')[0] not in route_dict:
                    route_dict[url.lstrip('/').split('/')[0]] = []
                route_dict[url.lstrip('/').split('/')[0]].append(url)
            #url = url_for(rule.endpoint, **(rule.defaults or {}))

            #print(dir(rule))
            #links.append((url, rule.endpoint))
  #  return { 'headers':  links }
    return render_template("site-map.html", route_dict=route_dict, product_dict=product_dict, vuln_dict=vuln_dict)















if __name__ == "__main__":
    app.run(port=7001, host=('0.0.0.0'), debug=True)