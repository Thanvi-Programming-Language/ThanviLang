from thanvi.runtime import run

def handler(request):
    try:
        source = request.get_json().get("code", "")
        run(source)
        return {
            "statusCode": 200,
            "body": "Thanvi code executed successfully"
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": str(e)
        }
