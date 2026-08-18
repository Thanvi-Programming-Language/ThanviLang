from thanvi.runtime import run

def handler(request):
    try:
        data = request.get_json()
        source = data.get("code", "")

        result = run(source)

        return {
            "statusCode": 200,
            "body": str(result)
        }

    except Exception as e:
        return {
            "statusCode": 400,
            "body": str(e)
        }
