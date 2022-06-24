from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

df_posts = pd.read_csv('IMKT.csv')
df_posts = df_posts.rename(columns={'date_MSK': 'date'})
df_comments = pd.read_csv('IMKT-comments.csv')
df_members = pd.read_csv('IMKT-members.csv')

df_posts_and_comments = df_posts.merge(df_comments, how='left', on='id')
df_posts_and_comments = df_posts_and_comments.rename(columns={'likes_x': 'posts_likes',
                                                              'likes_y': 'comments_likes'})
df_posts_and_comments.loc[(df_posts_and_comments['comments'] > 0) &
                          (df_posts_and_comments['text'].isna()), 'comments'] = 0

# GLOBAL DESIGN SETTINGS
CHARTS_TEMPLATE = go.layout.Template(
    layout=dict(
        font=dict(family='Century Gothic',
                  size=14)
    )
)

# TAB1 CONTENT - CHARTS


tab1_content = [
    # Filter and main graph
    dbc.Row([html.H5('Динамика количества просмотров постов',
                     style={'textAlign': 'center',
                            'marginTop': '5px'}),
             dcc.Dropdown(['Все посты', 'Посты с комментариями', 'Посты без комментариев'],
                          'Все посты',
                          id='dropdown-for-post',
                          style={'width': '300px',
                                 'margin-left': '10px'}),
             dcc.Graph(id='views-chart',
                       style={'margin-bottom': '30px'})
             ]
            ),
    # Subplot and post's comments
    dbc.Row([
        dbc.Col(html.H6('Наведите курсор на график для подробной информации',
                        id='inner-chart',
                        style={'margin-left': '10px'})),
        dbc.Col(dbc.Tabs([dbc.Tab(dcc.Markdown(id='text-post',
                                               style={'width': '100%',
                                                      'height': '160px',
                                                      'overflow': 'scroll',
                                                      'padding': '5px 5px 5px 5px'
                                                      }
                                               ), label='Описание поста'),
                          dbc.Tab([dcc.Markdown(id='comment'),
                                   dcc.Markdown(id='likes')],
                                  label='Топ комментарий'),
                          dbc.Tab(dcc.Markdown(id='comments'), label='Все комментарии')
                          ])
                )
    ])
]

# CONTENT FOR TAB2 - CARDS

# first card
first_post_date = 'Первый пост: ' + '.'.join(df_posts.date.iloc[-1][:10].split('-')[::-1])
count_post = df_posts.id.count()
mean_week_post = 'Постов в неделю ≈ ' + str(
    df_posts.id.count() / ((df_posts.date_UNIX.iloc[0] - df_posts.date_UNIX.iloc[-1])
                           / 60 / 60 / 168))[:4]
# second card
mean_likes_post = 'Среднее число лайков ≈ ' + str(df_posts.likes.mean())[:4]
all_likes_post = str(df_posts.likes.sum()) + ' 💙'
most_likely_post = 'Топ пост по лайкам (' + str(df_posts.iloc[df_posts['likes'].idxmax()].likes) + ')'
most_likely_post_link = 'https://vk.com/wall-206944280_' + str(df_posts.iloc[df_posts['likes'].idxmax()].id)

# third card
mean_repost_post = 'Среднее число репостов ≈ ' + str(df_posts.reposts.mean())[:4]
all_repost_post = str(df_posts.reposts.sum()) + ' 🔁'
most_repost_post = 'Топ пост по репостам (' + str(df_posts.iloc[df_posts['reposts'].idxmax()].reposts) + ')'
most_repost_post_link = 'https://vk.com/wall-206944280_' + str(df_posts.iloc[df_posts['reposts'].idxmax()].id)

# fourth card
mean_comments_post = 'Среднее число комментариев ≈ ' + str(df_posts.comments.mean())[:4]
all_comments_post = str(df_posts.comments.sum()) + ' 💬'
most_comments_post = 'Топ пост по комментариям (' + str(df_posts.iloc[df_posts['comments'].idxmax()].comments) + ')'
most_comments_post_link = 'https://vk.com/wall-206944280_' + str(df_posts.iloc[df_posts['comments'].idxmax()].id)

# fifth card
count_members = df_members.id.count()
sex = 'М - ' + str(df_members.sex.value_counts(normalize=True).iloc[0] * 100)[:4] + '%' + \
      ' Ж - ' + str(df_members.sex.value_counts(normalize=True).iloc[1] * 100)[:4] + '%'

# sixth card
top_com = df_members[df_members.iloc[:, 0] == df_comments.groupby(by='from_id', as_index=False) \
    .agg({'text': 'count'}) \
    .sort_values(by='text', ascending=False) \
    .iloc[0][0]]
top_commentator = 'Топ комментатор - ' + ' '.join(top_com.iloc[:, [1, 2]].values[0]) + ' (' + \
                  str(df_comments.groupby(by='from_id', as_index=False) \
                      .agg({'text': 'count'}) \
                      .sort_values(by='text', ascending=False) \
                      .iloc[0, 1]) + ')'
top_lk = df_members[df_members.iloc[:, 0] == df_comments.groupby(by='from_id', as_index=False) \
    .agg({'likes': 'sum'}) \
    .sort_values(by='likes', ascending=False) \
    .iloc[0][0]]
top_like = 'Топ получатель лайков - ' + ' '.join(top_lk.iloc[:, [1, 2]].values[0]) + ' (' + \
           str(df_comments.groupby(by='from_id', as_index=False) \
               .agg({'likes': 'sum'}) \
               .sort_values(by='likes', ascending=False) \
               .iloc[0, 1]) + ')'
time_continue = 'За период: ' + str((
                                                df_posts_and_comments.date_UNIX.max() - df_posts_and_comments.date_UNIX.min()) / 60 / 60 / 24 / 29.3)[
    0] + ' мес. ' + str(
    ((df_posts_and_comments.date_UNIX.max() - df_posts_and_comments.date_UNIX.min()) / 60 / 60 / 24 / 29.3 - 9) * 29.3)[
                    :2] + ' дн.'
# seventh card
top_comment_like = dcc.Markdown(df_comments.sort_values(by='likes', ascending=False).iloc[0, 3],
                                style={'width': '100%',
                                       'height': '88px',
                                       'overflow': 'scroll',
                                       'padding': '5px 5px 5px 5px'
                                       }
                                )
top_comment_like_likes = str(df_comments.sort_values(by='likes', ascending=False).iloc[0, 2]) + ' 💙'

# eighth card
mean_views_post = 'Среднее количество просмотров ≈ ' + str(df_posts.views.mean())[:3]
all_views_post = df_posts.views.sum()
likes_to_views = 'Лайки / просмотры ≈ ' + str(
    ((sum(df_posts.likes * df_posts.views)) / df_posts.views.sum()) ** (-1) * 100)[:3] + '%'

# TAB2 CONTENT - CARDS


tab2_content = [
    dbc.Row([
        dbc.Col([
            # first card
            dbc.Card([
                dbc.CardHeader(first_post_date),
                dbc.CardBody([
                    html.P('Всего постов:', className="card-title"),
                    html.H4(count_post, className="card-text")
                ]),
                dbc.CardFooter(mean_week_post)
            ], color='primary', outline=True
            )
        ], width={'size': 3}),
        dbc.Col([
            # second card
            dbc.Card([
                dbc.CardHeader(mean_likes_post),
                dbc.CardBody([
                    html.P('Всего лайков поставлено:', className="card-title"),
                    html.H4(all_likes_post, className="card-text")
                ]),
                dbc.CardFooter(html.A(most_likely_post, className="card-title", href=most_likely_post_link)),
            ], color='primary', outline=True
            )
        ], width={'size': 3}),
        dbc.Col([
            # third card
            dbc.Card([
                dbc.CardHeader(mean_repost_post),
                dbc.CardBody([
                    html.P('Всего репостов сделано:', className="card-title"),
                    html.H4(all_repost_post, className="card-text")
                ]),
                dbc.CardFooter(html.A(most_repost_post, className="card-title", href=most_repost_post_link)),
            ], color='primary', outline=True
            )
        ], width={'size': 3}),
        dbc.Col([
            # fourth card
            dbc.Card([
                dbc.CardHeader(mean_comments_post),
                dbc.CardBody([
                    html.P('Всего оставлено комментариев:', className="card-title"),
                    html.H4(all_comments_post, className="card-text")
                ]),
                dbc.CardFooter(html.A(most_comments_post, className="card-title", href=most_comments_post_link)),
            ], color='primary', outline=True
            )
        ], width={'size': 3}),
    ], style={'margin-left': '3px',
              'margin-right': '3px',
              'margin-top': '10px'}
    ),
    dbc.Row([
        dbc.Col([
            # fifth card
            dbc.Card([
                dbc.CardHeader('Город базирования - Владивосток'),
                dbc.CardBody([
                    html.P('Количество подписчиков:', className="card-title"),
                    html.H4(count_members, className="card-text")
                ], style={'height': '120px'}),
                dbc.CardFooter(sex),
            ], color='primary', outline=True
            )
        ], width={'size': 3}),
        dbc.Col([
            # sixth card
            dbc.Card([
                dbc.CardHeader('Самые активные участники:'),
                dbc.CardBody([
                    html.P(top_commentator, className='card-text'),
                    html.P(top_like, className='card-text')
                ], style={'height': '120px'}),
                dbc.CardFooter(time_continue),
            ], color='primary', outline=True
            )
        ], width={'size': 4}),
        dbc.Col([
            # seventh card
            dbc.Card([
                dbc.CardHeader('Топ комментарий по лайкам:'),
                dbc.CardBody([
                    html.P(top_comment_like, className='card-text'),
                ]),
                dbc.CardFooter(top_comment_like_likes)
            ], color='primary', outline=True
            )
        ], width={'size': 5})
    ], style={'margin-left': '3px',
              'margin-right': '3px',
              'margin-top': '10px'}
    ),
    dbc.Row([
        dbc.Col([
            # eighth card
            dbc.Card([
                dbc.CardHeader(mean_views_post),
                dbc.CardBody([
                    html.P('Всего просмотров:', className="card-title"),
                    html.H3(all_views_post, className="card-text")
                ]),
                dbc.CardFooter(likes_to_views)
            ], color="success", outline=True),

        ], width={'size': 3}),
        dbc.Col([
            # tenth card
            dbc.Card([
                dbc.CardImg(src=app.get_asset_url('images/logo.png'), style={'width': '930px', })
            ], color="primary", outline=True),
        ], width={'size': 8}, style={'margin-left': '119px'})
    ], style={'margin-left': '3px',
              'margin-right': '3px',
              'margin-top': '10px'}
    )

]

# LAYOUT


app.layout = html.Content([
    dbc.Row([
        dbc.Col(
            html.Img(src=app.get_asset_url('images/label-2.png'),
                     style={'width': '100px',
                            'margin-left': '5px',
                            'margin-top': '0px'}),
            width={'size': 1}
        ),
        dbc.Col(html.H1('Анализ постов группы vk.com/imct_fefu'),
                style={'marginTop': '25px',
                       'textAlign': 'left',
                       'margin-bottom': '1px',
                       'margin-left': '1px'},
                width={'size': 8}),
        dbc.Col([html.Div([
            html.P('Developed by', style={'color': 'white'}),
            html.A('Andrey Gulyaev', href='https://github.com/gulyaevAA?tab=repositories',
                   style={'color': 'white'})
        ])
        ],
            style={'textAlign': 'right',
                   'marginTop': '10px',
                   'margin-left': '110px'},
            width={'size': 2})
    ],
        className='app-header'

    ),
    dbc.Tabs([
        dbc.Tab(tab1_content, label='Обзор'),
        dbc.Tab(html.Div(tab2_content), label='Карточки')
    ], style={'margin-left': '10px',
              'margin-top': '5px'})
])


# CALLBACKS


@app.callback(
    Output('views-chart', 'figure'),
    Input('dropdown-for-post', 'value'))
def update_main_graph(value):
    if value == 'Все посты':
        fig = px.line(df_posts_and_comments, x='date', y='views', markers=True)
    elif value == 'Посты с комментариями':
        dff = df_posts_and_comments[df_posts_and_comments['comments'] > 0]
        fig = px.line(dff, x='date', y='views', markers=True)
    elif value == 'Посты без комментариев':
        dff = df_posts_and_comments[df_posts_and_comments['comments'] == 0]
        fig = px.line(dff, x='date', y='views', markers=True)
    fig.update_layout(template=CHARTS_TEMPLATE, height=350)
    return fig


@app.callback(
    Output('inner-chart', 'children'),
    Input('views-chart', 'hoverData'))
def update_graph_bar(hoverData):
    date_time = 0
    if len(hoverData['points'][0]['x']) == 16:
        date_time = hoverData['points'][0]['x'] + ':00'
    else:
        date_time = hoverData['points'][0]['x']
    dff = df_posts[df_posts['date'] == date_time]
    fig = go.Figure([go.Bar(x=['likes', 'reposts', 'comments'],
                            y=dff.iloc[:, [3, 5, 6]].values[0],
                            text=dff.iloc[:, [3, 5, 6]].values[0])
                     ])
    fig.update_layout(template=CHARTS_TEMPLATE, height=240)
    html1 = [html.H5('Лайки, репосты и комментарии поста',
                     style={'textAlign': 'center'}),
             dcc.Graph(figure=fig)]
    return html1


@app.callback(
    Output('text-post', 'children'),
    Output('comment', 'children'),
    Output('likes', 'children'),
    Output('comments', 'children'),
    Input('views-chart', 'hoverData'))
def update_comment(hoverData):
    comment = ''
    top_comment = ''
    likes = ''
    all_comments = []
    text = ''
    if len(hoverData['points'][0]['x']) == 16:
        date_time = hoverData['points'][0]['x'] + ':00'
    else:
        date_time = hoverData['points'][0]['x']
    dff = df_posts_and_comments[df_posts_and_comments['date'] == date_time]. \
        sort_values(by='comments_likes', ascending=False)

    if pd.isna(dff.text.iloc[0]):
        comment = 'Комментариев нет'
        likes = '0'
        all_comments.append('Комментариев нет')
    elif dff.comments_likes.max() == 0:
        comment = 'Лайков на комментарии нет'
        likes = '0'
        for n, text in enumerate(dff['text']):
            text = str(n + 1) + '. ' + text
            all_comments.append(text)
    else:
        comment = '"' + dff.text.iloc[0] + '"'
        likes = int(dff.comments_likes.iloc[0])
        for n, text in enumerate(dff['text']):
            text = str(n + 1) + '. ' + text
            all_comments.append(text)

    top_comment = comment
    all_comments = '''  
'''.join(all_comments)
    like = '*Лайков* 💙 ' + '*' + str(likes) + '*'
    text_post = dff["describe"].values[0][:670]

    return text_post, top_comment, like, all_comments


if __name__ == "__main__":
    app.run_server(debug=True)