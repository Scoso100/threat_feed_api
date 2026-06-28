from rest_framework.negotiation import BaseContentNegotiation


class JsonOnlyContentNegotiation(BaseContentNegotiation):
    def select_parser(self, request, parsers):
        return parsers[0]

    def select_renderer(self, request, renderers, format_suffix):
        renderer = renderers[0]
        return renderer, renderer.media_type
