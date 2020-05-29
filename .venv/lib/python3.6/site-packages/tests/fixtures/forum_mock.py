import httpretty
import json


def register_uris():
    """
    Mocks for a fake Discourse API set of endpoints
    """

    # Index page with navigation, URL map and redirects
    httpretty.register_uri(
        httpretty.GET,
        "https://discourse.example.com/t/34.json",
        body=json.dumps(
            {
                "id": 34,
                "category_id": 2,
                "title": "An index page",
                "slug": "an-index-page",
                "post_stream": {
                    "posts": [
                        {
                            "id": 3434,
                            "cooked": (
                                "<p>Some homepage content</p>"
                                "<h1>Navigation</h1>"
                                "<ul>"
                                '<li><a href="/t/page-a/10">Page A</a></li>'
                                '<li><a href="/t/b-page/12">B page</a></li>'
                                "</ul>"
                                "<h1>URLs</h1>"
                                '<details open="">'
                                "<summary>Mapping table</summary>"
                                '<div class="md-table">'
                                "<table>"
                                "<thead><tr>"
                                "<th>Topic</th><th>Path</th></tr></thead>"
                                "<tbody><tr>"
                                '<td><a href="https://discourse.example.com/t/'
                                'page-a/10">Page A</a></td>'
                                "<td>/a</td>"
                                "</tr><tr>"
                                '<td><a href="https://discourse.example.com/t/'
                                'page-z/26">Page Z</a></td>'
                                "<td>/page-z</td>"
                                "</tr></tbody></table>"
                                "</div></details>"
                                "<h1>Redirects</h1>"
                                '<details open="">'
                                "<summary>Mapping table</summary>"
                                '<div class="md-table">'
                                "<table>"
                                "<thead><tr>"
                                "<th>Topic</th><th>Path</th></tr></thead>"
                                "<tbody>"
                                "<tr><td>/redir-a</td><td>/a</td></tr>"
                                "<tr>"
                                "  <td>/example/page</td>"
                                "  <td>https://example.com/page</td>"
                                "</tr>"
                                "</tr></tbody></table>"
                                "</div></details>"
                            ),
                            "updated_at": "2018-10-02T12:45:44.259Z",
                        }
                    ]
                },
            }
        ),
        content_type="application/json",
    )

    # Index page with navigation only
    httpretty.register_uri(
        httpretty.GET,
        "https://discourse.example.com/t/35.json",
        body=json.dumps(
            {
                "id": 35,
                "category_id": 2,
                "title": "An index page",
                "slug": "an-index-page",
                "post_stream": {
                    "posts": [
                        {
                            "id": 3435,
                            "cooked": (
                                "<p>Some homepage content</p>"
                                "<h1>Navigation</h1>"
                                "<ul>"
                                '<li><a href="/t/page-a/10">Page A</a></li>'
                                '<li><a href="/t/b-page/12">B page</a></li>'
                                "</ul>"
                            ),
                            "updated_at": "2018-10-02T12:45:44.259Z",
                        }
                    ]
                },
            }
        ),
        content_type="application/json",
    )

    # Index page with broken, clashing url map and redirects
    httpretty.register_uri(
        httpretty.GET,
        "https://discourse.example.com/t/36.json",
        body=json.dumps(
            {
                "id": 36,
                "category_id": 2,
                "title": "An index page",
                "slug": "an-index-page",
                "post_stream": {
                    "posts": [
                        {
                            "id": 3436,
                            "cooked": (
                                "<p>Some homepage content</p>"
                                "<h1>Navigation</h1>"
                                "<ul>"
                                '<li><a href="/t/page-a/10">Page A</a></li>'
                                '<li><a href="/t/b-page/12">B page</a></li>'
                                "</ul>"
                                "<h1>URLs</h1>"
                                '<details open="">'
                                "<summary>Mapping table</summary>"
                                '<div class="md-table">'
                                "<table>"
                                "<thead><tr>"
                                "<th>Topic</th><th>Path</th></tr></thead>"
                                "<tbody><tr>"
                                '<td><a href="https://discourse.example.com/t'
                                '/page-a/10">Page A</a></td>'
                                "<td>/a</td>"
                                "</tr><tr>"
                                '<td><a href="https://discourse.example.com/t'
                                '/page-z/26">Page Z</a></td>'
                                "<td>/page-z</td>"
                                "</tr></tbody></table>"
                                "</div></details>"
                                "<h1>Redirects</h1>"
                                '<details open="">'
                                "<summary>Mapping table</summary>"
                                '<div class="md-table">'
                                "<table>"
                                "<thead><tr>"
                                "<th>Path</th><th>Location</th></tr></thead>"
                                "<tbody>"
                                "<tr>"
                                "  <td>/a</td><td>/clashing-redirect</td>"
                                "</tr>"
                                "<tr>"
                                "  <td>invalid-path</td><td>/somewhere</td>"
                                "</tr>"
                                "<tr>"
                                "  <td>/invalid-location</td>"
                                "  <td>some-domain.com/fish</td>"
                                "</tr>"
                                "<tr>"
                                "  <td>/valid</td>"
                                "  <td>/target</td>"
                                "</tr>"
                                "</tbody></table>"
                                "</div></details>"
                            ),
                            "updated_at": "2018-10-02T12:45:44.259Z",
                        }
                    ]
                },
            }
        ),
        content_type="application/json",
    )

    # Basic topic page with minimal content
    httpretty.register_uri(
        httpretty.GET,
        "https://discourse.example.com/t/10.json",
        body=json.dumps(
            {
                "id": 10,
                "category_id": 2,
                "title": "Page A",
                "slug": "page-a",
                "post_stream": {
                    "posts": [
                        {
                            "id": 56,
                            "cooked": ("<p>Content of this page</p>"),
                            "updated_at": "2018-10-02T12:45:44.259Z",
                        }
                    ]
                },
            }
        ),
        content_type="application/json",
    )

    # Basic topic page with minimal content
    httpretty.register_uri(
        httpretty.GET,
        "https://discourse.example.com/t/42.json",
        body=json.dumps(
            {
                "id": 42,
                "category_id": 2,
                "title": "A page",
                "slug": "a-page",
                "post_stream": {
                    "posts": [
                        {
                            "id": 56,
                            "cooked": ("<p>Content of Page A</p>"),
                            "updated_at": "2018-10-02T12:45:44.259Z",
                        }
                    ]
                },
            }
        ),
        content_type="application/json",
    )

    # Topic with "note to editors"
    httpretty.register_uri(
        httpretty.GET,
        "https://discourse.example.com/t/47.json",
        body=json.dumps(
            {
                "id": 47,
                "category_id": 2,
                "title": "Note to editors",
                "slug": "note-to-editors",
                "post_stream": {
                    "posts": [
                        {
                            "id": 59,
                            "cooked": (
                                "<p>Above</p>"
                                '<aside class="quote no-group">'
                                "<blockquote>"
                                "<p>"
                                '<img title=":construction:" class="emoji">'
                                "<strong>NOTE TO EDITORS</strong>"
                                '<img title=":construction:" class="emoji">'
                                "</p>"
                                "<p> Note content </p>"
                                "<p> Note content line 2 </p>"
                                "</blockquote>"
                                "</aside>"
                                "<p>Below</p>"
                            ),
                            "updated_at": "2018-10-02T12:45:44.259Z",
                        }
                    ]
                },
            }
        ),
        content_type="application/json",
    )

    # Topic with emoji-based notification
    httpretty.register_uri(
        httpretty.GET,
        "https://discourse.example.com/t/49.json",
        body=json.dumps(
            {
                "id": 49,
                "category_id": 2,
                "title": "Notifications",
                "slug": "notifications",
                "post_stream": {
                    "posts": [
                        {
                            "id": 64,
                            "cooked": (
                                "<p>Before</p>"
                                "<blockquote>"
                                "<p>ⓘ A notification</p>"
                                "</blockquote>"
                                ""
                                "<blockquote>"
                                "<p>"
                                '<img src="https://forum.snapcraft.io/'
                                'images/emoji/emoji_one/warning.png?v=5" '
                                'title=":warning:" class="emoji" '
                                'alt=":warning:"> '
                                "A warning"
                                "</p>"
                                "</blockquote>"
                                ""
                                "<p>After</p>"
                            ),
                            "updated_at": "2018-10-02T12:45:44.259Z",
                        }
                    ]
                },
            }
        ),
        content_type="application/json",
    )

    httpretty.register_uri(
        httpretty.GET,
        "https://discourse.example.com/t/50.json",
        body=json.dumps(
            {
                "id": 50,
                "category_id": 3,
                "title": "B page",
                "slug": "b-page",
                "post_stream": {
                    "posts": [
                        {
                            "id": 40,
                            "cooked": ("<p>Content of Page B</p>"),
                            "updated_at": "2018-10-02T12:45:44.259Z",
                        }
                    ]
                },
            }
        ),
        content_type="application/json",
    )

    httpretty.register_uri(
        httpretty.GET,
        "https://discourse.example.com/t/99.json",
        status=404,
        content_type="application/json",
    )

    httpretty.register_uri(
        httpretty.GET,
        "https://discourse.example.com/c/2.json",
        body=json.dumps(
            {
                "topic_list": {
                    "per_page": 3,
                    "topics": [
                        {
                            "id": 3434,
                            "slug": "super-fancy",
                            "fancy_title": "Super fancy",
                        }
                    ],
                }
            }
        ),
    )
