import mimetypes
import zipfile

NOT_FOUND = {"statusCode": 404, "body": "Not Found"}
TEXT_TYPES = [".css", "html", ".js", ".json", ".map", ".svg", ".txt"]


def to_bundle_path(path: str):
    if path.endswith("/"):
        path = path + "index.html"

    while path.startswith("/"):
        path = path[1:]

    return path


def mime_header(name):
    mimetypes.init()
    mime_type, _ = mimetypes.guess_type(name)
    if not mime_type:
        mime_type = "application/octet-stream"

    return {"Content-Type": mime_type}


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    path = event.get("path")
    if not path:
        return NOT_FOUND

    bundle = zipfile.ZipFile("html-bundle.zip", mode="r")
    bundle_path = to_bundle_path(path)
    if bundle_path not in bundle.namelist():
        return NOT_FOUND

    headers = mime_header(bundle_path)
    to_base64 = not any([bundle_path.endswith(ext) for ext in TEXT_TYPES])

    return {
        "statusCode": 200,
        "headers": headers,
        "body": bundle.read(bundle_path).decode("utf-8"),
        "isBase64Encoded": to_base64,
    }
