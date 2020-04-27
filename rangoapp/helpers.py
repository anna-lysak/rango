from datetime import datetime
from rango import settings
import requests


def visitor_cookie_handler(request, response):
    # Get the number of visits to the site.
    # We use the COOKIES.get() function to obtain the visits cookie.
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesn't exist, then the default value of 1 is used.
    visits = int(request.COOKIES.get('visits', '1'))
    last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')
    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # Update the last visit cookie now that we have updated the count
        response.set_cookie('last_visit', str(datetime.now()))
    else:
        # Set the last visit cookie
        response.set_cookie('last_visit', last_visit_cookie)
    # Update/set the visits cookie
    response.set_cookie('visits', visits)


def visitor_session_handler(request):
    # Get the number of visits to the site.
    # We use the COOKIES.get() function to obtain the visits cookie.
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesn't exist, then the default value of 1 is used.
    visits = int(request.session.get('visits', '1'))
    last_visit_cookie = request.session.get('last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')
    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # Update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        # Set the last visit cookie
        request.session['last_visit'] = last_visit_cookie
    # Update/set the visits cookie
    request.session['visits'] = visits


def get_category_list(search_str, max_results=0):
    """
    Returns list of categories that contain query string
    :param search_str - query string
    :param max_results - maximum amount of results
    :return categories list
    """
    from rangoapp.models import Category

    cat_list = []
    if search_str:
        cat_list = Category.objects.filter(name__icontains=search_str)
    if max_results > 0:
        if len(cat_list) > max_results:
            cat_list = cat_list[:max_results]
    return cat_list


def get_google_results(search_str, start=1):
    """
    Returns Google search results for the given query
    :param search_str - query string
    :param start - start number of the results (used for pagination)
    :return pages list from Google search
    """
    results = []
    if search_str:
        # don't call google search as start number exceeds maximum number of results (100) returned by Google
        if start >= 100:
            return []

        # Google returns 10 results maximum for 1 call (num value).
        url = settings.GOOGLE_SEARCH_URL.format(gapi_key=settings.GOOGLE_API_KEY,
                                                gse=settings.GOOGLE_SEARCH_ENGINE_ID,
                                                query=search_str,
                                                lang='en',
                                                start=start,
                                                num=10)
        print(url)
        response = requests.get(url)
        if response.status_code == 200:
            ret_json = response.json()
            if 'items' in ret_json:
                for item in ret_json['items']:
                    results.append({
                        'title': item['title'],
                        'link': item['link'],
                        'snippet': item['snippet']
                    })

        else:
            print(response.json())

        if not results:
            for i in range(10):
                results.append({
                    'title': 'Fake',
                    'link': 'http://fake_page.com',
                    'snippet': 'This is fake result'
                })
    return results


if __name__ == '__main__':
    print(get_google_results('python', start=11))
