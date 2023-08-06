from aiohttp_graphql import GraphQLView as BaseGraphQLView
from graphene_file_upload.utils import add_file_to_operations
from graphql_server import load_json_body


class GraphQLView(BaseGraphQLView):

    def place_files_in_operations(self, operations, files_map, data):
        path_to_key_iter = (
            (value.split('.'), key)
            for (key, values) in files_map.items()
            for value in values
        )
        # Since add_files_to_operations returns a new dict/list, first define
        # output to be operations itself
        output = operations
        for path, key in path_to_key_iter:
            file_obj = data[key]
            output = add_file_to_operations(output, file_obj, path)
        return output

    async def parse_body(self, request):
        if request.content_type == 'application/graphql':
            r_text = await request.text()
            return {'query': r_text}

        elif request.content_type == 'application/json':
            text = await request.text()
            return load_json_body(text)

        elif request.content_type == 'multipart/form-data':
            data = await request.post()
            operations = load_json_body(data.get('operations', {}))
            files_map = load_json_body(data.get('map', {}))
            return self.place_files_in_operations(
                operations,
                files_map,
                data
            )
        elif request.content_type in (
                'application/x-www-form-urlencoded',
                'multipart/form-data',
        ):
            return dict(await request.post())

        return {}
