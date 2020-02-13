from django.http import HttpResponse


def index(request):
    # get all games in this upcoming season's schedule that are today and tomorrow



    text = """
    <h3>Welcome.</h3>
    <table width="50%" border="1">
    <tr>
        <td>aaa</td>
        <td>bbb</td>
    </tr>
    <tr>
        <td>ccc</td>
        <td>ddd</td>
    </tr>
    </table>
    """
    return HttpResponse(text)
