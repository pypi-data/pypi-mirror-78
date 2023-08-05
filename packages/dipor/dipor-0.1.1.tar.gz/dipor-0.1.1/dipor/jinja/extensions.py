import jinja2
from jinja2 import nodes
from jinja2.ext import Extension

class RoutesExtension(Extension):
    tags = {"route"}

    def __init__(self, environment):
        super(RoutesExtension, self).__init__(environment)

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        args = [parser.parse_expression()]
        if parser.stream.skip_if("comma"):
            args.append(parser.parse_expression)
        else:
            args.append(nodes.Const(None))
        node = self.call_method('_generate_routes', args, lineno=lineno)
        return nodes.CallBlock(node, [], [], [], lineno=lineno)

    def _generate_routes(self, routes, current, caller):
        routes2html = self.__generate_routes(routes, current)
        return jinja2.Markup(routes2html)

    
    def __generate_routes(self, routes, current=None, html='<ul>', is_subpath=False):
        if not current:
            for k, v in routes.items():
                if not v[1]:
                    html += f"<li><a href='{v[0]}'>"+k+"</a></li>"
                else:
                    html += f"<li><a href='{v[0]}'>"+k+"<ul>"
                    html = self.__generate_routes(v[1], current, html, is_subpath=True)
            if is_subpath:
                html += "</ul></li>"
                return html

            return html+"</ul>"