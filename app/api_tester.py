import requests
from h2o_wave import ui, app, main, Q

resp = ''
url = ''
meta_theme = 'h2o-light'
toggled = False
message_bar_visibility = False
message_bar_type = 'info'
message_bar_text = ''
request_body = ''
request_method = ''
request_headers = {'Content-type': 'application/json'}


@app('/api')
async def serve(q: Q):
    global request_body, request_headers, request_method, meta_theme, toggled, resp

    if q.args.body:
        q.page['form'] = body()
    elif q.args.headers:
        q.page['form'] = headers()
    elif q.args.ok:
        request_method = q.args.method
        request_body = q.args.text
        api_test(q, request_method)
    elif q.args.send:
        request_method = q.args.method
        resp = send(q.args.url, request_method)
        api_test(q, request_method)
    elif q.args.addHeader:
        key = q.args.key
        val = q.args.val
        if key == '' or val == '':
            show_dialog(q)
        else:
            request_headers[key] = val
            q.page['form'] = headers()
    elif q.args.empty_headers:
        q.page['meta'].dialog = None
        q.page['form'] = headers()
    elif q.args.delHeader:
        request_headers = delete_header(q.args.delId, request_headers)
        q.page['form'] = headers()
    elif q.args.toggle:
        toggled = True
        toggle_theme(q, 'h2o-dark')
    else:
        request_method = q.args.method
        meta_theme = 'h2o-light'
        toggled = False
        api_test(q, request_method)
    await q.page.save()


def update_status_code(response):
    global message_bar_text, message_bar_type, message_bar_visibility
    message_bar_visibility = True

    if str(response.status_code)[0] == '2':
        message_bar_type = 'success'
    else:
        message_bar_type = 'error'

    message_bar_text = str(response.status_code) + ' ' + response.reason
    return message_bar_text, message_bar_type, message_bar_visibility


def delete_header(idx, rh):
    try:
        keys = list(rh.keys())
        idx = int(idx) - 1
        del rh[keys[idx]]
    except IndexError:
        headers()
    except ValueError:
        headers()
    return rh


def send(method_url, method):
    global resp, url, request_body, request_headers, message_bar_text, message_bar_type, message_bar_visibility
    request_headers['Content-type'] = 'application/json'
    url = method_url
    response = ''
    try:
        if method == 'GET':
            response = requests.get(url, headers=request_headers)

            resp = str(response.json())
        elif method == 'POST':
            response = requests.post(url, request_body, headers=request_headers)

            resp = str(response.json())
        elif method == 'PUT':
            response = requests.put(url, request_body, headers=request_headers)

            resp = str(response.json())
        elif method == 'DELETE':
            response = requests.delete(url, request_body, headers=request_headers)

            resp = str(response.json())

        message_bar_text, message_bar_type, message_bar_visibility = update_status_code(response)
    except:
        message_bar_text, message_bar_type, message_bar_visibility = "Time Limit Exceeded", "error", True

    return resp


def api_test(q: Q, req_method):
    toggle_theme(q, meta_theme)
    q.page['form'] = ui.form_card(
        box='1 2 5 5',
        items=[
            ui.inline(
                items=[
                    ui.dropdown(name='method', label='Method', value=req_method or '', choices=[
                        ui.choice(name=x, label=x) for x in ['GET', 'POST', 'PUT', 'DELETE']
                    ], width='100px'),
                    ui.textbox(name='url', label='URL', width='600px', value=url),
                ]
            ),
            ui.button(name='send', label='Send', primary=True, caption=''),
            ui.separator(),
            ui.buttons(items=[
                ui.button(name='body', label='Body'),
                ui.button(name='headers', label='Headers')
            ]),
            ui.separator(),
            ui.message_bar(type=message_bar_type, text=message_bar_text, visible=message_bar_visibility),
            ui.textbox(name='response', label='Response', multiline=True, value=resp, trigger=True, readonly=True,
                       height='120px')
        ]
    )

    q.page['header'] = ui.header_card(
        box='1 1 5 1',
        title='API Tester',
        subtitle='Simple. Elegent. Efficient.',
        icon='Globe',
        items=[
            ui.toggle(name='toggle', trigger=True, label='Dark Mode', value=toggled),
            ui.image(title='wave', path='https://wave.h2o.ai/img/h2o-logo.svg', width='50px')
        ]
    )

    q.page['footer'] = ui.footer_card(box='1 7 5 1', caption='Made with 💛 by Sakuna Jayasundara.')


def body():
    global request_body
    return ui.form_card(box='1 2 5 5', items=[
        ui.text_l('Request body'),
        ui.textbox(name='text', label='Enter the request body', multiline=True, value=request_body, height='300px'),
        ui.buttons([
            ui.button(name='ok', label='OK', primary=True),
            ui.button(name='api_test', label='Back'),
        ]),
    ])


def headers():
    global request_body, request_headers
    return ui.form_card(box='1 2 5 5', items=[
        ui.text_l('Request headers'),
        ui.inline(items=[
            ui.textbox(name='key', placeholder='Key', width='300px'),
            ui.textbox(name='val', placeholder='Value', width='300px'),
            ui.button(name='addHeader', label='Add', icon='Add', primary=True)
        ]),
        ui.table(name='table', columns=[
            ui.table_column(name='id', label='ID'),
            ui.table_column(name='col1', label='Key'),
            ui.table_column(name='col2', label='Value'),
        ], rows=[ui.table_row(name='row1', cells=[str(i + 1), k, v]) for i, (k, v) in
                 enumerate(request_headers.items())]),
        ui.inline([
            ui.textbox(name='delId', placeholder='ID', width='100px', value="1"),
            ui.button(name='delHeader', label='Delete'),
            ui.button(name='ok', label='OK', primary=True),
        ]),

    ])


def show_dialog(q: Q):
    q.page['meta'].dialog = ui.dialog(title='Error', items=[
        ui.text('Key and Value pair both should be filled!'),
        ui.buttons([ui.button(name='empty_headers', label='OK', primary=True)])
    ])


def toggle_theme(q: Q, theme):
    global meta_theme
    meta_theme = theme
    q.page['meta'] = ui.meta_card(box='1 2 5 5', theme=theme)
