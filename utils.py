import datetime
import sys
import random

STATE_REQUEST_KEY = 'session'
STATE_RESPONSE_KEY = 'session_state'


# Вспомогательные функции
# узнаем имя функции для аналитики
def whoami():
    return sys._getframe(1).f_code.co_name


def make_response(text, tts=None, card=None, state=None, buttons=None, end_session=False, events=None):
    response = {
        'text': text,
        'tts': tts if tts is not None else text,
    }
    webhook_response = {
        'response': response,
        'version': '1.0',
    }
    if card is not None:
        response['card'] = card
    if buttons:
        response['buttons'] = buttons
    if state is not None:
        webhook_response[STATE_RESPONSE_KEY] = state
    if events is not None:
        webhook_response["analytics"] = events
    if end_session:
        response['end_session'] = end_session
        # webhook_response["analytics"]["events"]["value"]["end_session"] = state

    return webhook_response


def make_events(name, event):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    events = {
        'events': [
            {
                "name": name,
                "value": {
                    "user_id": event['session']['user_id'],
                    "user": event['state']['user'],
                    "session_id": event['session']['session_id'],
                    "timestamp": now,
                    "command": event['request']['command'],
                    "application_id": event['session']['application']['application_id'],
                    "application": event['state']['application'],
                    "client_id": event['meta']['client_id'],
                }
            }
        ]
    }
    return events


def button(title, payload=None, url=None, hide=False):
    button = {
        'title': title,
        'hide': hide,
    }
    if payload is not None:
        button['payload'] = payload
    if url is not None:
        button['url'] = url
    return button


def image_gallery(image_ids):
    items = [{'image_id': image_id} for image_id in image_ids]
    return {
        'type': 'ImageGallery',
        'items': items,
    }


def image_list(image_ids, image_titles=[], image_descriptions=[], footer_text='Footer text'):
    items = [{'image_id': image_id} for image_id in image_ids]
    if len(image_ids) != len(image_titles) or len(image_ids) != len(image_descriptions):
        i = 0
        while i < len(items):
            items[i]['title'] = 'Title ' + str(i)
            items[i]['description'] = 'Description' + str(i)
            i += 1
        else:
            i = 0
            while i < len(items):
                items[i]['title'] = image_titles[i]
                items[i]['description'] = image_descriptions[i]
                i += 1
    return {
        'type': 'ItemsList',
        'items': items,
        "footer": {
            "text": footer_text,
        }
    }


def image_card(image_id, title, description):
    return {
        'type': 'BigImage',
        'image_id': image_id,
        'title': title,
        'description': description,
    }


# Специфические обработки запросов Фэлбэки Курсы
def fallback(event):
    return make_response(
        'Извините, я Вас не поняла. Пожалуйста, попробуйте переформулировать.',
        state=event['state'][STATE_REQUEST_KEY],
        events=make_events(str(whoami()), event),
    )


def fallback_yes_no(event):
    term_1 = random.choice([
        "Похоже сегодня магнитные бури. Давайте по проще.",
        "У меня сегодня  болит голова. Давайте по проще.",
        "Вчера была вечеринка и я туго соображаю. Давайте по проще.",
        "Банальности. С ними скучно и без них не обойтись. Давайте попроще.",
        "Говорят: Будь проще, и люди к тебе потянутся.",
        "Слово — что камень: коли метнёт его рука, то уж потом назад не воротишь. Но мне непонятно что за камень.",
        "Ой. Я немного замечталась. И жду.",
        "Глухой и тишины не услышит, вот и я не услышала ваш ответ",
        "Если ты хочешь что-то изменить, перестаньте хотеть и начинайте менять. Поменяйте ответ.",
    ])
    text = f'{term_1} Ответьте на вопрос Да или Нет?'
    return make_response(
        text,
        state=event['state'][STATE_REQUEST_KEY],
        events=make_events(str(whoami()), event),
    )


def fallback_help_me(event):
    return make_response(
        'Могу предложить тест или рассказать про профессии',
        state=event['state'][STATE_REQUEST_KEY],
        events=make_events(str(whoami()), event),
    )


def handler_curses(event):
    text = ('Отличный выбор курса. Хотите пройти тест еще раз?')
    return make_response(
        text,
        state=event['state'][STATE_REQUEST_KEY],
        buttons=[
            button('Да', hide=True),
            button('Нет', hide=True),
            button('Стоп', hide=True),
        ],
        events=make_events(str(whoami()), event),
    )


def in_test_not_prof(event):
    text = (
        'Поздравляю! Вы очень разносторонний человек. '
        'Тест закончился, а я похоже не смогла подобрать Вам профессию. '
        'Могу предложить пройти тест или рассказать про профессии. '
    )
    return make_response(
        text,
        state=event['state'][STATE_REQUEST_KEY],
        buttons=[
            button('Пройти тест', hide=True),
            button('Расскажи про профессии', hide=True),
        ],
        events=make_events(str(whoami()), event),
    )


def goodbye(event):
    return make_response(
        'Было приятно поболтать! До новых встреч!',
        state=event['state'][STATE_REQUEST_KEY],
        events=make_events(str(whoami()), event),
        end_session=True
    )


# НАЧАЛО диалога
def welcome_message(event):
    text = ('Добро пожаловать, тут я помогу вам найти для себя новую профессию. '
            'Расскажу о самых интересных и востребованных АйТи профессиях. '
            'Вы знаете какое направление вас интересует?')
    return make_response(
        text,
        state={
            'screen': 'welcome_message',
        },
        buttons=[
            button('Знаю', hide=True),
            button('Не знаю', hide=True),
        ],
        events=make_events(str(whoami()), event)
    )


# Рассказ о профессиях ( и Сценарий нет)
def start_tour(event):
    text = ('Сфера АйТи очень огромна, в ней есть множество различных профессий. '
            'Здесь я расскажу вам о профессиях, но вы по-прежнему можете пройти тест, если скажете: "Хочу тест." '
            'О какой специальности рассказать подробнее?')
    return make_response(
        text,
        state={
            'screen': 'start_tour',
        },
        buttons=[
            button('Аналитик'),
            button('Тестировщик'),
            button('Разработчик'),
            button('Проджект менеджер'),
            button('Дизайнер'),
            button('Хочу пройти тест', hide=True),
            button('Стоп', hide=True),
        ],
        events=make_events(str(whoami()), event),
    )


def get_analyst(event):
    tts = ('Аналитик sil<[1000]> Аналитик - это специалист, который занимается выявлением'
           'бизнес-проблем, выяснению потребностей заинтересованных сторон,'
           'обоснованию решений и обеспечению проведения изменений в организации.'
           'Здесь я рассказываю вам о профессиях, но вы по прежнему можете пройти тест, если скажете: "Хочу тест."'
           'О какой специальности рассказать еще?'
           )
    state = event['state'][STATE_REQUEST_KEY]
    state['pre_intent'] = event['request']['nlu']['intents']

    return make_response(
        text=('О какой специальности рассказать еще?'),
        tts=tts,
        card=image_gallery(image_ids=[
            '213044/63a681ed14b11c5a07f8',
            '1030494/365630c9031fddf7b64f',
        ]),
        buttons=[
            button('Аналитик'),
            button('Тестировщик'),
            button('Разработчик'),
            button('Проджект менеджер'),
            button('Дизайнер'),
            button('Хочу пройти тест', hide=True),
            button('Стоп', hide=True),
        ],
        state=state,
        events=make_events(str(whoami()), event),
    )


def get_tester(event):
    tts = ('Тестировщик sil<[1000]>. Тестировщик - это тоже специалист в АйТИ без программирования, '
           'он проверяет мобильные и веб-приложения, проверяет сервисы и проектирует тесты, '
           'а главное — помогает бизнесу развиваться, а пользователям решать задачи. Тестировщику нужно '
           'уметь работать с браузерами, понимать, чем они отличаются друг от друга. '
           'А ещё быть внимательным и усидчивым, чтобы проверять продукт несколько раз и не упускать ошибки. '
           'Здесь я рассказываю вам о профессиях, но вы по прежнему можете пройти тест, если скажете: "Хочу тест."'
           'О какой специальности рассказать еще?'
           )
    state = event['state'][STATE_REQUEST_KEY]
    state['pre_intent'] = event['request']['nlu']['intents']

    return make_response(
        text=('О какой специальности рассказать еще?'),
        tts=tts,
        card=image_gallery(image_ids=[
            '965417/da3995836be573c5105c',
            '937455/821e4711579405cb303c',
        ]),
        buttons=[
            button('Аналитик'),
            button('Тестировщик'),
            button('Разработчик'),
            button('Проджект менеджер'),
            button('Дизайнер'),
            button('Хочу пройти тест', hide=True),
            button('Стоп', hide=True),
        ],
        state=state,
        events=make_events(str(whoami()), event)
    )


def get_developer(event):
    tts = ('Разработчик sil<[1000]>. Разработчик – широкий термин для группы специалистов, работа которых направлена '
           'на создание мобильных и компьютерных приложений, игр, баз данных и прочего '
           'программного обеспечения самых различных устройств. Разработчики в своей '
           'деятельности умело совмещают творческий подход и строгий язык программирования.'
           'Здесь я рассказываю вам о профессиях, но вы по прежнему можете пройти тест, если скажете: "Хочу тест."'
           'О какой специальности рассказать еще?'
           )
    state = event['state'][STATE_REQUEST_KEY]
    state['pre_intent'] = event['request']['nlu']['intents']

    return make_response(
        text=('О какой специальности рассказать еще?'),
        tts=tts,
        card=image_gallery(image_ids=[
            '937455/90cd65c968df16b271ca',
            '1030494/93da29e28371b4fbf420',
            '937455/ff7df0037cec56949e7a',
        ]),
        buttons=[
            button('Аналитик'),
            button('Тестировщик'),
            button('Разработчик'),
            button('Проджект менеджер'),
            button('Дизайнер'),
            button('Хочу пройти тест', hide=True),
            button('Стоп', hide=True),
        ],
        state=state,
        events=make_events(str(whoami()), event),
    )


def get_project_manager(event):
    tts = ('Проджект менеджер или Руководитель проектов sil<[1000]>. '
           'Проджект менеджер - это специалист, который управляет проектами. Проекты могут быть из любой сферы: '
           'АйТИ, маркетинг, строительство, музыкальные, кино-, промышленные, '
           'сельскохозяйственные и пр. Любое дело, в котором занято больше одного человека, '
           '— это уже проект. Значит, нужен человек, который организует процесс и доведет его до финала. '
           'Здесь я рассказываю вам о профессиях, но вы по прежнему можете пройти тест, если скажете: "Хочу тест."'
           'О какой специальности рассказать еще?'
           )
    state = event['state'][STATE_REQUEST_KEY]
    state['pre_intent'] = event['request']['nlu']['intents']

    return make_response(
        text=('О какой специальности рассказать еще?'),
        tts=tts,
        card=image_gallery(image_ids=[
            '1030494/b0939295fbd1180e31c1',
            '1540737/4d2224260af3239055f2',
        ]),
        buttons=[
            button('Аналитик'),
            button('Тестировщик'),
            button('Разработчик'),
            button('Проджект менеджер'),
            button('Дизайнер'),
            button('Хочу пройти тест', hide=True),
            button('Стоп', hide=True),
        ],
        state=state,
        events=make_events(str(whoami()), event),
    )


def get_designer(event):
    tts = ('Дизайнер sil<[1000]>. '
           'Дизайнер - это человек, который работает над внешним видом сайта. Он выбирает, '
           'какие элементы будут представлены на странице и в каком порядке они '
           'будут отражаться на мониторах пользователей. Например, он решает, '
           'что будет, если навести курсор мыши на определенный блок и в какой '
           'последовательности будет отображаться информация при прокрутке страницы '
           'вниз.  Веб-дизайнер думает о цветах, композиции и простоте использования '
           'сайта для пользователя.'
           'Здесь я рассказываю вам о профессиях, но вы по прежнему можете пройти тест, если скажете: "Хочу тест."'
           'О какой специальности рассказать еще?'
           )
    state = event['state'][STATE_REQUEST_KEY]
    state['pre_intent'] = event['request']['nlu']['intents']

    return make_response(
        text=('О какой специальности рассказать еще?'),
        tts=tts,
        card=image_gallery(image_ids=[
            '1030494/2692022cbb88a5122999',
            '213044/47829b15ed70bb8d13ea',
        ]),
        buttons=[
            button('Аналитик'),
            button('Тестировщик'),
            button('Разработчик'),
            button('Проджект менеджер'),
            button('Дизайнер'),
            button('Хочу пройти тест', hide=True),
            button('Стоп', hide=True),
        ],
        state=state,
        events=make_events(str(whoami()), event),
    )


def fallback_no_prof(event):
    text = (
        'Этой профессии пока нет в этом навыке, но скоро обязательно появится. '
        'Хотите пройти тест или рассказать еще о како-то профессии? '
    )
    return make_response(
        text,
        state=event['state'][STATE_REQUEST_KEY],
        events=make_events(str(whoami()), event),
    )


def start_tour_with_prof(event, intent_name='start_tour_with_prof'):
    intent = event['request']['nlu']['intents'][intent_name]
    prof = intent['slots']['prof']['value']
    if prof == 'analyst':
        return get_analyst(event)
    elif prof == 'tester':
        return get_tester(event)
    elif prof == 'developer':
        return get_developer(event)
    elif prof == 'project_manager':
        return get_project_manager(event)
    elif prof == 'designer':
        return get_designer(event)
    else:
        return fallback_no_prof(event)


def what_do_you_know(event):
    return make_response(
        'Я постоянно развиваюсь, и знаю о многих профессиях. Например, о самых востребованных на сегодня: Аналитик, Тестировщик, Разработчик, и многих других.',
        state=event['state'][STATE_REQUEST_KEY],
        events=make_events(str(whoami()), event),
    )

    # term_1 = random.choice(["Аналитик", "Тестировщик", "Разработчик", "Проджект менеджер", "Дизайнер"])
    # text = f'Я постоянно развиваюсь, на сегодяшний день я знаю о пяти профессиях. Например, рассказать про {term_1}?'
    # return make_response(text, state={
    #     'screen': 'what_do_you_know', 'prof': ''
    # }, buttons=[
    #     button('Да', hide=True),
    #     button('Нет', hide=True),
    #     button('Стоп', hide=True),
    # ])


# Тест
def welcome_test(event):
    text = ('Я могу вам предложить пройти небольшой тест, который поможет Вам определиться. '
            'Запускаем?')
    return make_response(
        text,
        state={
            'screen': 'start_test',
        },
        buttons=[
            button('Да', hide=True),
            button('Нет', hide=True),
            button('Стоп', hide=True),
        ],
        events=make_events(str(whoami()), event),
    )


def test_q1(event):
    text = ('Получаете ли вы удовольствие, решая различные головоломки?')
    return make_response(
        text,
        state={
            'screen': 'test_q1',
        },
        buttons=[
            button('Да', hide=True),
            button('Нет', hide=True),
            button('Стоп', hide=True),
        ],
        events=make_events(str(whoami()), event),
    )


def test_q2(event):
    text = ('Выберите суперсилу: становиться невидимым или уметь летать?')
    return make_response(
        text,
        state={
            'screen': 'test_q2',
        },
        buttons=[
            button('Становиться невидимым', hide=True),
            button('Уметь летать', hide=True),
            button('Стоп', hide=True),
        ],
        events=make_events(str(whoami()), event),
    )


def test_q3(event):
    text = ('За какую зарплату вы готовы мыть все окна в Москве, больше или меньше 100 тысяч рублей?')
    return make_response(text, state={
        'screen': 'test_q3',
    }, buttons=[
        button('Меньше ста тысяч рублей', hide=True),
        button('Больше ста тысяч рублей', hide=True),
        button('Стоп', hide=True),
    ], events=make_events(str(whoami()), event),
                         )


# развилка на Аналитика и Тестировщика с Разработчиком
def test_q4(event):
    text = ('Нравится ли вам общаться с людьми?')
    return make_response(text, state={
        'screen': 'test_q4',
    }, buttons=[
        button('Да', hide=True),
        button('Нет', hide=True),
        button('Стоп', hide=True),
    ], events=make_events(str(whoami()), event),
                         )


# ветка Аналитик
def test_q5(event):
    text = ('Поздравляю! Вам подойдет профессия Аналитика! Хотите узнать больше о профессии?')
    return make_response(
        text,
        state={
            'screen': 'test_q5',
        },
        buttons=[
            button('Да', hide=True),
            button('Нет', hide=True),
            button('Стоп', hide=True),
        ],
        events=make_events(str(whoami()), event),
    )


def test_q6(event):
    text = ('Это специалист, который занимается выявлением бизнес-проблем, '
            'выяснением потребностей заинтересованных сторон, обоснованием решений '
            'и обеспечением проведения изменений в организации. Вам нравится ?'
            )

    tts = (
        ' Аналитик sil<[1000]>. Аналитик - это специалист, который занимается выявлением бизнес-проблем, выяснением потребностей '
        'заинтересованных сторон, обоснованием решений и обеспечением проведения изменений в '
        'организации. Вам нравится ?'
        )
    return make_response(
        text='',
        tts=tts,
        card=image_card(
            image_id='1030494/b670b9ab66cb03bf63b0',
            title='Так выглядит Аналитик',
            description=text,
        ),
        state={
            'screen': 'test_q6',
        },
        buttons=[
            button('Да', hide=True),
            button('Нет', hide=True),
            button('Стоп', hide=True),
        ],
        events=make_events(str(whoami()), event),
    )


def test_q7(event):
    text = ('Вам интересно узнать, какие курсы можно пройти, чтобы освоить эту профессию?')
    return make_response(text, state={
        'screen': 'test_q7',
    }, buttons=[
        button('Да', hide=True),
        button('Нет', hide=True),
        button('Стоп', hide=True),
    ], events=make_events(str(whoami()), event),
                         )


def test_q8(event):
    text = ('Для того чтобы стать грамотным и востребованным специалистом можно пройти курсы перечисленные ниже. '
            'Вы сможете самостоятельно найти их в поиске позже или пройти по ссылкам ниже. '
            'Хотите пройти тест еще раз? '
            )
    tts = ('Для того чтобы стать грамотным и востребованным специалистом Вы можете пройти следующие курсы:'
           'Курс "Профессия Бизнес-аналитик" Школа Skill Box;'
           'Курс "Бизнес-аналитик базовый курс" Школа Нетология;'
           'Вы можете самостоятельно найти их в поиске позже или пройти по ссылкам, если проходите тест на смартфоне. '
           'Хотите пройти тест еще раз?'
           )
    return make_response(
        text,
        tts=tts,
        state={
            'screen': 'test_q8',
        },
        buttons=[
            button('Курс "Профессия Бизнес-аналитик" Школа Skill Box',
                   url='https://skillbox.ru/course/profession-business-analyst-cv/'),
            button('Курс "Бизнес-аналитик базовый курс" Школа Нетология',
                   url='https://netology.ru/programs/business-analytics-online'),
            button('Да', hide=True),
            button('Нет', hide=True),
            button('Стоп', hide=True),
        ],
        events=make_events(str(whoami()), event),
    )


def test_q4_1(event):
    text = ('Разбирали и ломали ли Вы в детстве игрушки?')
    return make_response(text, state={
        'screen': 'test_q4_1',
    }, buttons=[
        button('Да', hide=True),
        button('Нет', hide=True),
        button('Стоп', hide=True),
    ], events=make_events(str(whoami()), event),
                         )


# обработка ветки Тестировщик
def test_q4_2(event):
    text = ('Поздравляю! Вам подойдет профессия тестировщик! '
            'Хотите узнать больше о профессии? ')
    return make_response(text, state={
        'screen': 'test_q4_2',
    }, buttons=[
        button('Да', hide=True),
        button('Нет', hide=True),
        button('Стоп', hide=True),
    ], events=make_events(str(whoami()), event),
                         )


def test_q4_3(event):
    text = ('Это тоже специалист в АйТИ без программирования, он проверяет мобильные '
            'и веб-приложения, проверяет сервисы и проектирует тесты, а главное — помогает '
            'бизнесу развиваться, а пользователям решать задачи. Тестировщику нужно '
            'уметь работать с браузерами, понимать, чем они отличаются друг от друга. '
            'А ещё быть внимательным и усидчивым, чтобы проверять продукт несколько раз '
            'и не упускать ошибки. Вам нравится?'
            )
    tts = ('Тестировщик sil<[1000]>. Тестировщик - это тоже специалист в АйТИ без программирования, '
           'он проверяет мобильные и веб-приложения, проверяет сервисы и проектирует тесты, '
           'а главное — помогает бизнесу развиваться, а пользователям решать задачи. Тестировщику нужно '
           'уметь работать с браузерами, понимать, чем они отличаются друг от друга. '
           'А ещё быть внимательным и усидчивым, чтобы проверять продукт несколько раз '
           'и не упускать ошибки. Вам нравится?'
           )
    return make_response(
        text='',
        tts=tts,
        card=image_card(
            image_id='1540737/55a35da6645c941cecaf',
            title='Так выглядит Тестировщик',
            description=text,
        ),
        state={
            'screen': 'test_q4_3',
        },
        buttons=[
            button('Да', hide=True),
            button('Нет', hide=True),
            button('Стоп', hide=True),
        ],
        events=make_events(str(whoami()), event),
    )


def test_q4_4(event):
    text = ('Вам интересно узнать, какие курсы можно пройти, чтобы освоить эту профессию?')
    return make_response(text, state={
        'screen': 'test_q4_4',
    }, buttons=[
        button('Да', hide=True),
        button('Нет', hide=True),
        button('Стоп', hide=True),
    ], events=make_events(str(whoami()), event),
                         )


def test_q4_5(event):
    text = ('Для того чтобы стать грамотным и востребованным специалистом можно пройти курсы перечисленные ниже. '
            'Вы сможете самостоятельно найти их в поиске позже или пройти по ссылкам ниже. '
            'Хотите пройти тест еще раз? '
            )
    tts = ('Для того чтобы стать грамотным и востребованным специалистом Вы можете пройти следующие курсы:'
           'Курс "Тестировщик на Python" Школа Skill Factory; '
           'Курс «Инженер по тестированию» Школа Yandex; '
           'Вы можете самостоятельно найти их в поиске позже или пройти по ссылкам, если проходите тест на смартфоне. '
           'Хотите пройти тест еще раз?'
           )
    return make_response(
        text,
        tts=tts,
        state={
            'screen': 'test_q4_5',
        },
        buttons=[
            button('Курс "Тестировщик на Python" Школа Skill Factory',
                   url='https://skillfactory.ru/qa-engineer-python-testirovshchik-programmnogo-obespecheniya'),
            button('Курс "Инженер по тестированию" Школа Yandex', url='https://skillbox.ru/course/profession-test/'),
            button('Да', hide=True),
            button('Нет', hide=True),
            button('Стоп', hide=True),
        ],
        events=make_events(str(whoami()), event),
    )


# обработка ветки Разработчик
def test_q4_6(event):
    text = ('Поздравляю! Вам подойдет профессия разработчик! '
            'Хотите узнать больше о профессии? ')
    return make_response(text, state={
        'screen': 'test_q4_6',
    }, buttons=[
        button('Да', hide=True),
        button('Нет', hide=True),
        button('Стоп', hide=True),
    ], events=make_events(str(whoami()), event),
                         )


def test_q4_7(event):
    text = ('Разработчик. Разработчик – широкий термин для группы специалистов, работа которых направлена '
            'на создание мобильных и компьютерных приложений, игр, баз данных и прочего '
            'программного обеспечения самых различных устройств. Разработчики в своей '
            'деятельности умело совмещают творческий подход и строгий язык программирования.'
            'Вам нравится?'
            )
    tts = ('Разработчик sil<[1000]>. Разработчик – широкий термин для группы специалистов, работа которых направлена '
           'на создание мобильных и компьютерных приложений, игр, баз данных и прочего '
           'программного обеспечения самых различных устройств. Разработчики в своей '
           'деятельности умело совмещают творческий подход и строгий язык программирования.'
           'Вам нравится?'
           )
    return make_response(
        text='',
        tts=tts,
        card=image_card(
            image_id='1030494/8bad0d6b6752762c446b',
            title='Так выглядит Разработчик',
            description=text,
        ),
        state={
            'screen': 'test_q4_7',
        },
        buttons=[
            button('Да', hide=True),
            button('Нет', hide=True),
            button('Стоп', hide=True),
        ],
        events=make_events(str(whoami()), event),
    )


def test_q4_8(event):
    text = ('Вам интересно узнать, какие курсы можно пройти, чтобы освоить эту профессию?')
    return make_response(text, state={
        'screen': 'test_q4_8',
    }, buttons=[
        button('Да', hide=True),
        button('Нет', hide=True),
        button('Стоп', hide=True),
    ], events=make_events(str(whoami()), event),
                         )


def test_q4_9(event):
    text = ('Для того чтобы стать грамотным и востребованным специалистом можно пройти курсы перечисленные ниже. '
            'Вы сможете самостоятельно найти их в поиске позже или пройти по ссылкам ниже. '
            'Хотите пройти тест еще раз? '
            )
    tts = ('Для того чтобы стать грамотным и востребованным специалистом Вы можете пройти следующие курсы:'
           'Курс "Веб-разработчик с нуля". Школа Школа Скил фэктори; '
           'Курс "Разработчик C++" Школа Яндекс; '
           'Вы можете самостоятельно найти их в поиске позже или пройти по ссылкам, если проходите тест на смартфоне. '
           'Хотите пройти тест еще раз? '
           )
    return make_response(
        text,
        tts=tts,
        state={
            'screen': 'test_q4_9',
        },
        buttons=[
            button('Курс "Веб-разработчик с нуля". Школа Школа Скил фэктори',
                   url='https://skillfactory.ru/python-fullstack-web-developer'),
            button('Курс «Разработчик C++» Школа Яндекс',
                   url='https://skillbox.ru/course/profession-fullstack-python/'),
            button('Да', hide=True),
            button('Нет', hide=True),
            button('Стоп', hide=True),
        ],
        events=make_events(str(whoami()), event),
    )


# *********КОД ЮЛИ******************
def test_q2_1(event):
    text = ('Готовы ли вы лидировать в команде?')
    return make_response(text, state={
        'screen': 'test_q2_1',
    }, buttons=[
        button('Да', hide=True),
        button('Нет', hide=True),
        button('Стоп', hide=True),
    ], events=make_events(str(whoami()), event),
                         )


def test_q2_2(event):
    text = ('Если бы вы стали деревом, то каким?')
    return make_response(text, state={
        'screen': 'test_q2_2',
    }, buttons=[
        button('Дуб', hide=True),
        button('Береза', hide=True),
        button('Стоп', hide=True),
    ], events=make_events(str(whoami()), event),
                         )


def test_q2_3(event):
    text = ('Нравится ли вам планировать свой день?')
    return make_response(text, state={
        'screen': 'test_q2_3',
    }, buttons=[
        button('Да', hide=True),
        button('Нет', hide=True),
        button('Стоп', hide=True),
    ], events=make_events(str(whoami()), event),
                         )


def test_q2_4(event):
    text = ('Поздравляю! Вам подойдет профессия Проджект-менеджера! Хотите узнать больше о профессии?')
    return make_response(text, state={
        'screen': 'test_q2_4',
    }, buttons=[
        button('Да', hide=True),
        button('Нет', hide=True),
        button('Стоп', hide=True),
    ], events=make_events(str(whoami()), event),
                         )


def test_q2_5(event):
    text = ('Проджект менеджер - это специалист, который управляет проектами. Проекты могут быть из любой сферы: '
            'АйТи, маркетинг, строительство, музыкальные, кино-, промышленные, сельскохозяйственные '
            'и пр. Любое дело, в котором занято больше одного человека, — это уже проект. Значит, '
            'нужен человек, который организует процесс и доведет его до финала. Вам нравится ?'
            )
    tts = ('Проджект менеджер или Руководитель проектов sil<[1000]>. '
           'Проджект менеджер - это специалист, который управляет проектами. Проекты могут быть из любой сферы: '
           'АйТи, маркетинг, строительство, музыкальные, кино-, промышленные, сельскохозяйственные '
           'и пр. Любое дело, в котором занято больше одного человека, — это уже проект. Значит, '
           'нужен человек, который организует процесс и доведет его до финала. Вам нравится ?'
           )
    return make_response(
        text='',
        tts=tts,
        card=image_card(
            image_id='937455/272ac9342cd8d3b8095f',
            title='Так выглядит Проджект менеджер',
            description=text,
        ),
        state={
            'screen': 'test_q2_5',
        },
        buttons=[
            button('Да', hide=True),
            button('Нет', hide=True),
            button('Стоп', hide=True),
        ],
        events=make_events(str(whoami()), event),
    )


def test_q2_6(event):
    text = ('Вам интересно узнать, какие курсы можно пройти, чтобы освоить эту профессию?')
    return make_response(text, state={
        'screen': 'test_q2_6',
    }, buttons=[
        button('Да', hide=True),
        button('Нет', hide=True),
        button('Стоп', hide=True),
    ], events=make_events(str(whoami()), event),
                         )


def test_q2_7(event):
    text = ('Для того чтобы стать грамотным и востребованным специалистом можно пройти курсы перечисленные ниже. '
            'Вы сможете самостоятельно найти их в поиске позже или пройти по ссылкам ниже. '
            'Хотите пройти тест еще раз? '
            )
    tts = ('Для того чтобы стать грамотным и востребованным специалистом Вы можете пройти следующие курсы:'
           'Курс "Профессия Project Manager в IT" Школа Skill Factory; '
           'Курс "Менеджер проектов" Школа Yandex; '
           'Вы можете самостоятельно найти их в поиске позже или пройти по ссылкам, если проходите тест на смартфоне. '
           'Хотите пройти тест еще раз? '
           )
    return make_response(
        text,
        tts=tts,
        state={
            'screen': 'test_q2_7',
        },
        buttons=[
            button('Курс "Профессия Project Manager в IT" Школа Skill Factory',
                   url='https://skillfactory.ru/project-manager'),
            button('Курс "Менеджер проектов" Школа Yandex', url='https://practicum.yandex.ru/project-manager/'),
            button('Да', hide=True),
            button('Нет', hide=True),
            button('Стоп', hide=True),
        ],
        events=make_events(str(whoami()), event),
    )


def test_q2_8(event):
    text = ('Рисуете ли вы в воображении места, куда хотите отправиться?')
    return make_response(text, state={
        'screen': 'test_q2_8',
    }, buttons=[
        button('Да', hide=True),
        button('Нет', hide=True),
        button('Стоп', hide=True),
    ], events=make_events(str(whoami()), event),
                         )


def test_q2_9(event):
    text = ('Хотели бы вы научиться создавать красивый дизайн?')
    return make_response(text, state={
        'screen': 'test_q2_9',
    }, buttons=[
        button('Да', hide=True),
        button('Нет', hide=True),
        button('Стоп', hide=True),
    ], events=make_events(str(whoami()), event),
                         )


def test_q2_10(event):
    text = ('Поздравляю! Вам подойдет профессия Веб-дизайнер! '
            'Хотите узнать больше о профессии? ')
    return make_response(text, state={
        'screen': 'test_q2_10',
    }, buttons=[
        button('Да', hide=True),
        button('Нет', hide=True),
        button('Стоп', hide=True),
    ], events=make_events(str(whoami()), event),
                         )


def test_q2_11(event):
    text = ('Дизайнер. '
            'Это человек, который работает над внешним видом сайта. Он выбирает, '
            'какие элементы будут представлены на странице и в каком порядке они '
            'будут отражаться на мониторах пользователей. Например, он решает, '
            'что будет, если навести курсор мыши на определенный блок и в какой '
            'последовательности будет отображаться информация при прокрутке '
            'страницы вниз.  Веб-дизайнер думает о цветах, композиции и простоте '
            'использования сайта для пользователя. '
            'Вам нравится?'
            )
    tts = ('Дизайнер sil<[1000]>. '
           'Это человек, который работает над внешним видом сайта. Он выбирает, '
           'какие элементы будут представлены на странице и в каком порядке они '
           'будут отражаться на мониторах пользователей. Например, он решает, '
           'что будет, если навести курсор мыши на определенный блок и в какой '
           'последовательности будет отображаться информация при прокрутке '
           'страницы вниз.  Веб-дизайнер думает о цветах, композиции и простоте '
           'использования сайта для пользователя. '
           'Вам нравится?'
           )
    return make_response(
        text='',
        tts=tts,
        card=image_card(
            image_id='1030494/271f106942eb800d4cc5',
            title='Так выглядит Дизайнер',
            description=text,
        ),
        state={
            'screen': 'test_q2_11',
        },
        buttons=[
            button('Да', hide=True),
            button('Нет', hide=True),
            button('Стоп', hide=True),
        ],
        events=make_events(str(whoami()), event),
    )


def test_q2_12(event):
    text = ('Вам интересно узнать, какие курсы можно пройти, чтобы освоить эту профессию?')
    return make_response(text, state={
        'screen': 'test_q2_12',
    }, buttons=[
        button('Да', hide=True),
        button('Нет', hide=True),
        button('Стоп', hide=True),
    ], events=make_events(str(whoami()), event),
                         )


def test_q2_13(event):
    text = ('Для того чтобы стать грамотным и востребованным специалистом можно пройти курсы перечисленные ниже. '
            'Вы сможете самостоятельно найти их в поиске позже или пройти по ссылкам ниже. '
            'Хотите пройти тест еще раз? '
            )
    tts = ('Для того чтобы стать грамотным и востребованным специалистом Вы можете пройти следующие курсы:'
           'Курс "Профессия веб-дизайнер" Школа Skill Factory; '
           'Курс "Дизайнер интерфейсов" Школа Yandex; '
           'Вы можете самостоятельно найти их в поиске позже или пройти по ссылкам, если проходите тест на смартфоне. '
           'Хотите пройти тест еще раз? '
           )
    return make_response(
        text,
        tts=tts,
        state={
            'screen': 'test_q2_13',
        },
        buttons=[
            button('Курс "Профессия веб-дизайнер" Школа Skill Factory',
                   url='https://contented.ru/edu/web-designer?utm_source=skillfactory'),
            button('Курс "Дизайнер интерфейсов" Школа Yandex',
                   url='https://skillbox.ru/course/profession-webdesigner/'),
            button('Да', hide=True),
            button('Нет', hide=True),
            button('Стоп', hide=True),
        ],
        events=make_events(str(whoami()), event),
    )