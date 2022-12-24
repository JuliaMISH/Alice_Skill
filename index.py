from utils import *


# Основной обработчик
def handler(event, context):
    intents = event['request'].get('nlu', {}).get('intents')
    state = event.get('state').get(STATE_REQUEST_KEY, {})
    if event['session']['new']:
        return welcome_message(event)
    elif state.get('screen') == 'welcome_message':
        if ('welcome_test' in intents) or ('u_not' in intents):       #Ветка НЕ ЗНАЮ - идем в тест
            return welcome_test(event)
        elif ('start_prof_tour' in intents) or ('u_yes' in intents):  #Ветка ЗНАЮ - идем в тур по профессиям
            return start_tour(event)
        elif ('start_tour_with_prof' in intents):
            return start_tour_with_prof(event, intent_name="start_tour_with_prof")
            # return make_response('Speech about analyst')
        elif ('start_tour_with_prof_short' in intents):
            return start_tour_with_prof(event, intent_name='start_tour_with_prof_short')
        elif 'repeat_me' in intents and state.get('pre_intent') is None:
            return welcome_message(event)
        elif 'repeat_me' in intents and state.get('pre_intent') is not None:
            if 'start_tour_with_prof' in list(state.get('pre_intent').keys()): # данная ветка необходима для обработки повторного повтора
                intent_name_key = 'start_tour_with_prof'
            else:
                intent_name_key = 'start_tour_with_prof_short'
            event['request']['nlu']['intents'].update(state.get('pre_intent'))
            return start_tour_with_prof(event, intent_name=intent_name_key)
        # обработка помощи
        elif 'help_me' in intents:
            return fallback_help_me(event)
        elif 'want_test' in intents:
            return welcome_test(event)
        elif 'start_tour' in intents:
            return start_tour(event)
        elif 'what_do_you_know' in intents or 'what_do_you_know_long' in intents :
            return what_do_you_know(event)
        else:
            return fallback(event)
    # Перемещаемся в Тест
    elif state.get('screen') == 'start_test':
        if 'u_yes' in intents:
            return test_q1(event)
        elif 'u_not' in intents:
            return start_tour(event)
        elif 'u_stop' in intents:
            return goodbye(event)
        elif 'repeat_me' in intents:
            return welcome_test(event)
       # обработка помощи
        elif 'help_me' in intents:
            return fallback_help_me(event)
        elif 'want_test' in intents:
            return welcome_test(event)
        elif 'start_tour' in intents:
            return start_tour(event)
        else:
            return fallback_yes_no(event)
    # Развилка - Аналитик или Тестировщик с Разработчик
    elif state.get('screen') == 'test_q1':
        if 'u_yes' in intents:
    # ветка Аналитик
            return test_q2(event)
        elif 'u_not' in intents:
            # Уходим в ветку Юли
            return test_q2_1(event)
        elif 'u_stop' in intents:
            return goodbye(event)
        elif 'repeat_me' in intents:
            return test_q1(event)
       # обработка помощи
        elif 'help_me' in intents:
            return fallback_help_me(event)
        elif 'want_test' in intents:
            return welcome_test(event)
        elif 'start_tour' in intents:
            return start_tour(event)
        else:
            return fallback_yes_no(event)
    elif state.get('screen') == 'test_q2':
        if 'u_stop' in intents:
            return goodbye(event)
        elif 'repeat_me' in intents:
            return test_q2(event)
        # обработка помощи
        elif 'help_me' in intents:
            return fallback_help_me(event)
        elif 'want_test' in intents:
            return welcome_test(event)
        elif 'start_tour' in intents:
            return start_tour(event)
        else:
            return test_q3(event)
    elif state.get('screen') == 'test_q3':
        if 'u_stop' in intents:
            return goodbye(event)
        elif 'repeat_me' in intents:
            return test_q3(event)
        # обработка помощи
        elif 'help_me' in intents:
            return fallback_help_me(event)
        elif 'want_test' in intents:
            return welcome_test(event)
        elif 'start_tour' in intents:
            return start_tour(event)
        else:
            return test_q4(event)
    elif state.get('screen') == 'test_q4':
        if 'u_yes' in intents:
            return test_q5(event)
        elif 'u_not' in intents:
            return test_q4_1(event)
        elif 'u_stop' in intents:
            return goodbye(event)
        elif 'repeat_me' in intents:
            return test_q4(event)
        # обработка помощи
        elif 'help_me' in intents:
            return fallback_help_me(event)
        elif 'want_test' in intents:
            return welcome_test(event)
        elif 'start_tour' in intents:
            return start_tour(event)
        else:
            return fallback_yes_no(event)
    elif state.get('screen') == 'test_q5':
        if 'u_yes' in intents:
            return test_q6(event)
        elif 'u_not' in intents:
            return start_tour(event)
        elif 'u_stop' in intents:
            return goodbye(event)
        elif 'repeat_me' in intents:
            return test_q5(event)
        # обработка помощи
        elif 'help_me' in intents:
            return fallback_help_me(event)
        elif 'want_test' in intents:
            return welcome_test(event)
        elif 'start_tour' in intents:
            return start_tour(event)
        else:
            return fallback_yes_no(event)
    elif state.get('screen') == 'test_q6':
        if 'u_yes' in intents:
            return test_q7(event)
        elif 'u_not' in intents:
            return start_tour(event)
        elif 'u_stop' in intents:
            return goodbye(event)
        elif 'repeat_me' in intents:
            return test_q6(event)
        # обработка помощи
        elif 'help_me' in intents:
            return fallback_help_me(event)
        elif 'want_test' in intents:
            return welcome_test(event)
        elif 'start_tour' in intents:
            return start_tour(event)
        else:
            return fallback_yes_no(event)
    elif state.get('screen') == 'test_q7':
        if 'u_yes' in intents:
            return test_q8(event)
        elif 'u_not' in intents:
            return start_tour(event)
        elif 'u_stop' in intents:
            return goodbye(event)
        elif 'repeat_me' in intents:
            return test_q7(event)
        # обработка помощи
        elif 'help_me' in intents:
            return fallback_help_me(event)
        elif 'want_test' in intents:
            return welcome_test(event)
        elif 'start_tour' in intents:
            return start_tour(event)
        else:
            return fallback_yes_no(event)
    elif state.get('screen') == 'test_q8':
        if 'u_yes' in intents:
            return welcome_test(event)
        elif 'u_not' in intents:
            return start_tour(event)
        elif 'u_stop' in intents:
            return goodbye(event)
        elif 'link_to_course_accurate' in intents:
             return handler_curses(event)
        elif 'repeat_me' in intents:
            return test_q8(event)
        # обработка помощи
        elif 'help_me' in intents:
            return fallback_help_me(event)
        elif 'want_test' in intents:
            return welcome_test(event)
        elif 'start_tour' in intents:
            return start_tour(event)
        else:
            return fallback(event)
    # ветка Тестировщик
    elif state.get('screen') == 'test_q4_1':
        if 'u_yes' in intents:
            return test_q4_2(event)
        elif 'u_not' in intents:
            # уходим в ветку Разработчик
            return test_q4_6(event)
        elif 'u_stop' in intents:
            return goodbye(event)
        elif 'repeat_me' in intents:
            return test_q4_1(event)
        # обработка помощи
        elif 'help_me' in intents:
            return fallback_help_me(event)
        elif 'want_test' in intents:
            return welcome_test(event)
        elif 'start_tour' in intents:
            return start_tour(event)
        else:
            return fallback_yes_no(event)
    elif state.get('screen') == 'test_q4_2':
        if 'u_yes' in intents:
            return test_q4_3(event)
        elif 'u_not' in intents:
            return start_tour(event)
        elif 'u_stop' in intents:
            return goodbye(event)
        elif 'repeat_me' in intents:
            return test_q4_2(event)
        # обработка помощи
        elif 'help_me' in intents:
            return fallback_help_me(event)
        elif 'want_test' in intents:
            return welcome_test(event)
        elif 'start_tour' in intents:
            return start_tour(event)
        else:
            return fallback_yes_no(event)
    elif state.get('screen') == 'test_q4_3':
        if 'u_yes' in intents:
            return test_q4_4(event)
        elif 'u_not' in intents:
            return start_tour(event)
        elif 'u_stop' in intents:
            return goodbye(event)
        elif 'repeat_me' in intents:
            return test_q4_3(event)
        # обработка помощи
        elif 'help_me' in intents:
            return fallback_help_me(event)
        elif 'want_test' in intents:
            return welcome_test(event)
        elif 'start_tour' in intents:
            return start_tour(event)
        else:
            return fallback_yes_no(event)
    elif state.get('screen') == 'test_q4_4':
        if 'u_yes' in intents:
            return test_q4_5(event)
        elif 'u_not' in intents:
            return start_tour(event)
        elif 'u_stop' in intents:
            return goodbye(event)
        elif 'repeat_me' in intents:
            return test_q4_4(event)
        # обработка помощи
        elif 'help_me' in intents:
            return fallback_help_me(event)
        elif 'want_test' in intents:
            return welcome_test(event)
        elif 'start_tour' in intents:
            return start_tour(event)
        else:
            return fallback_yes_no(event)
    elif state.get('screen') == 'test_q4_5':
        if 'u_yes' in intents:
            return welcome_test(event)
        elif 'u_not' in intents:
            return start_tour(event)
        elif 'u_stop' in intents:
            return goodbye(event)
        elif 'link_to_course_accurate' in intents:
             return handler_curses(event)
        elif 'repeat_me' in intents:
            return test_q4_5(event)
        # обработка помощи
        elif 'help_me' in intents:
            return fallback_help_me(event)
        elif 'want_test' in intents:
            return welcome_test(event)
        elif 'start_tour' in intents:
            return start_tour(event)
        else:
            return fallback(event)
    # ветка Разработчик
    elif state.get('screen') == 'test_q4_6':
        if 'u_yes' in intents:
            return test_q4_7(event)
        elif 'u_not' in intents:
            return start_tour(event)
        elif 'u_stop' in intents:
            return goodbye(event)
        elif 'repeat_me' in intents:
            return test_q4_6(event)
        # обработка помощи
        elif 'help_me' in intents:
            return fallback_help_me(event)
        elif 'want_test' in intents:
            return welcome_test(event)
        elif 'start_tour' in intents:
            return start_tour(event)
        else:
            return fallback_yes_no(event)
    elif state.get('screen') == 'test_q4_7':
        if 'u_yes' in intents:
            return test_q4_8(event)
        elif 'u_not' in intents:
            return start_tour(event)
        elif 'u_stop' in intents:
            return goodbye(event)
        elif 'repeat_me' in intents:
            return test_q4_7(event)
        # обработка помощи
        elif 'help_me' in intents:
            return fallback_help_me(event)
        elif 'want_test' in intents:
            return welcome_test(event)
        elif 'start_tour' in intents:
            return start_tour(event)
        else:
            return fallback_yes_no(event)
    elif state.get('screen') == 'test_q4_8':
        if 'u_yes' in intents:
            return test_q4_9(event)
        elif 'u_not' in intents:
            return start_tour(event)
        elif 'u_stop' in intents:
            return goodbye(event)
        elif 'repeat_me' in intents:
            return test_q4_8(event)
        # обработка помощи
        elif 'help_me' in intents:
            return fallback_help_me(event)
        elif 'want_test' in intents:
            return welcome_test(event)
        elif 'start_tour' in intents:
            return start_tour(event)
        else:
            return fallback_yes_no(event)
    elif state.get('screen') == 'test_q4_9':
        if 'u_yes' in intents:
            return welcome_test(event)
        elif 'u_not' in intents:
            return start_tour(event)
        elif 'u_stop' in intents:
            return goodbye(event)
        elif 'link_to_course_accurate' in intents:
             return handler_curses(event)
        elif 'repeat_me' in intents:
            return test_q4_9(event)
        # обработка помощи
        elif 'help_me' in intents:
            return fallback_help_me(event)
        elif 'want_test' in intents:
            return welcome_test(event)
        elif 'start_tour' in intents:
            return start_tour(event)
        else:
            return fallback(event)
    #*********КОД ЮЛИ******************
    elif state.get('screen') == 'test_q2_1':
        if 'u_yes' in intents:
            return test_q2_2(event)
        elif 'u_not' in intents:
            return test_q2_8(event)
        elif 'u_stop' in intents:
            return goodbye(event)
        elif 'repeat_me' in intents:
            return test_q2_1(event)
        # обработка помощи
        elif 'help_me' in intents:
            return fallback_help_me(event)
        elif 'want_test' in intents:
            return welcome_test(event)
        elif 'start_tour' in intents:
            return start_tour(event)
        else:
            return fallback_yes_no(event)
    elif state.get('screen') == 'test_q2_2':
        if 'u_stop' in intents:
            return goodbye(event)
        elif 'repeat_me' in intents:
            return test_q2_2(event)
        # обработка помощи
        elif 'help_me' in intents:
            return fallback_help_me(event)
        elif 'want_test' in intents:
            return welcome_test(event)
        elif 'start_tour' in intents:
            return start_tour(event)
        else:
            return test_q2_3(event)
    elif state.get('screen') == 'test_q2_3':
        if 'u_yes' in intents:
            return test_q2_4(event)
        elif 'u_not' in intents:
            return in_test_not_prof(event) #start_tour(event)
        elif 'u_stop' in intents:
            return goodbye(event)
        elif 'repeat_me' in intents:
            return test_q2_3(event)
        # обработка помощи
        elif 'help_me' in intents:
            return fallback_help_me(event)
        elif 'want_test' in intents:
            return welcome_test(event)
        elif 'start_tour' in intents:
            return start_tour(event)
        else:
            return fallback_yes_no(event)
    elif state.get('screen') == 'test_q2_4':
        if 'u_yes' in intents:
            return test_q2_5(event)
        elif 'u_not' in intents:
            return start_tour(event)
        elif 'u_stop' in intents:
            return goodbye(event)
        elif 'repeat_me' in intents:
            return test_q2_4(event)
        # обработка помощи
        elif 'help_me' in intents:
            return fallback_help_me(event)
        elif 'want_test' in intents:
            return welcome_test(event)
        elif 'start_tour' in intents:
            return start_tour(event)
        else:
            return fallback_yes_no(event)
    elif state.get('screen') == 'test_q2_5':
        if 'u_yes' in intents:
            return test_q2_6(event)
        elif 'u_not' in intents:
            return start_tour(event)
        elif 'u_stop' in intents:
            return goodbye(event)
        elif 'repeat_me' in intents:
            return test_q2_5(event)
        # обработка помощи
        elif 'help_me' in intents:
            return fallback_help_me(event)
        elif 'want_test' in intents:
            return welcome_test(event)
        elif 'start_tour' in intents:
            return start_tour(event)
        else:
            return fallback_yes_no(event)
    elif state.get('screen') == 'test_q2_6':
        if 'u_yes' in intents:
            return test_q2_7(event)
        elif 'u_not' in intents:
            return start_tour(event)
        elif 'u_stop' in intents:
            return goodbye(event)
        elif 'repeat_me' in intents:
            return test_q2_6(event)
        # обработка помощи
        elif 'help_me' in intents:
            return fallback_help_me(event)
        elif 'want_test' in intents:
            return welcome_test(event)
        elif 'start_tour' in intents:
            return start_tour(event)
        else:
            return fallback_yes_no(event)
    elif state.get('screen') == 'test_q2_7':
        if 'u_yes' in intents:
            return welcome_test(event)
        elif 'u_not' in intents:
            return start_tour(event)
        elif 'u_stop' in intents:
            return goodbye(event)
        elif 'repeat_me' in intents:
            return test_q2_7(event)
        elif 'link_to_course_accurate' in intents:
            return handler_curses(event)
        # обработка помощи
        elif 'help_me' in intents:
            return fallback_help_me(event)
        elif 'want_test' in intents:
            return welcome_test(event)
        elif 'start_tour' in intents:
            return start_tour(event)
        else:
            return fallback(event)
    elif state.get('screen') == 'test_q2_8':
        if 'u_yes' in intents:
            return test_q2_9(event)
        elif 'u_not' in intents:
            return in_test_not_prof(event) #start_tour(event)
        elif 'u_stop' in intents:
            return goodbye(event)
        elif 'repeat_me' in intents:
            return test_q2_8(event)
        # обработка помощи
        elif 'help_me' in intents:
            return fallback_help_me(event)
        elif 'want_test' in intents:
            return welcome_test(event)
        elif 'start_tour' in intents:
            return start_tour(event)
        else:
            return fallback_yes_no(event)
    elif state.get('screen') == 'test_q2_9':
        if 'u_yes' in intents:
            return test_q2_10(event)
        elif 'u_not' in intents:
            return in_test_not_prof(event) #start_tour(event)
        elif 'u_stop' in intents:
            return goodbye(event)
        elif 'repeat_me' in intents:
            return test_q2_9(event)
        # обработка помощи
        elif 'help_me' in intents:
            return fallback_help_me(event)
        elif 'want_test' in intents:
            return welcome_test(event)
        elif 'start_tour' in intents:
            return start_tour(event)
        else:
            return fallback_yes_no(event)
    elif state.get('screen') == 'test_q2_10':
        if 'u_yes' in intents:
            return test_q2_11(event)
        elif 'u_not' in intents:
            return start_tour(event)
        elif 'u_stop' in intents:
            return goodbye(event)
        elif 'repeat_me' in intents:
            return test_q2_10(event)
        # обработка помощи
        elif 'help_me' in intents:
            return fallback_help_me(event)
        elif 'want_test' in intents:
            return welcome_test(event)
        elif 'start_tour' in intents:
            return start_tour(event)
        else:
            return fallback_yes_no(event)
    elif state.get('screen') == 'test_q2_11':
        if 'u_yes' in intents:
            return test_q2_12(event)
        elif 'u_not' in intents:
            return start_tour(event)
        elif 'u_stop' in intents:
            return goodbye(event)
        elif 'repeat_me' in intents:
            return test_q2_11(event)
        # обработка помощи
        elif 'help_me' in intents:
            return fallback_help_me(event)
        elif 'want_test' in intents:
            return welcome_test(event)
        elif 'start_tour' in intents:
            return start_tour(event)
        else:
            return fallback_yes_no(event)
    elif state.get('screen') == 'test_q2_12':
        if 'u_yes' in intents:
            return test_q2_13(event)
        elif 'u_not' in intents:
            return start_tour(event)
        elif 'u_stop' in intents:
            return goodbye(event)
        elif 'repeat_me' in intents:
            return test_q2_12(event)
        # обработка помощи
        elif 'help_me' in intents:
            return fallback_help_me(event)
        elif 'want_test' in intents:
            return welcome_test(event)
        elif 'start_tour' in intents:
            return start_tour(event)
        else:
            return fallback_yes_no(event)
    elif state.get('screen') == 'test_q2_13':
        if 'u_yes' in intents:
            return welcome_test(event)
        elif 'u_not' in intents:
            return start_tour(event)
        elif 'u_stop' in intents:
            return goodbye(event)
        elif 'repeat_me' in intents:
            return test_q2_13(event)
        elif 'link_to_course_accurate' in intents:
             return handler_curses(event)
        # обработка помощи
        elif 'help_me' in intents:
            return fallback_help_me(event)
        elif 'want_test' in intents:
            return welcome_test(event)
        elif 'start_tour' in intents:
            return start_tour(event)
        else:
            return fallback(event)
    #*********КОНЕЦ КОДа ЮЛИ***********
    # Ветка ЗНАЮ
    # elif 'start_prof_tour' in intents:
    #     return start_tour(event)
    elif 'start_tour_with_prof' in intents:
        return start_tour_with_prof(event)
    elif state.get('screen') == 'start_tour'  and 'start_tour_with_prof_short' in intents:
        return start_tour_with_prof(event, intent_name='start_tour_with_prof_short')
    elif state.get('screen') == 'start_tour'  and 'repeat_me' in intents:
        # intent_name_key = list(state.get('pre_intent').keys())[0]
        if 'start_tour_with_prof' in list(state.get('pre_intent').keys()): # данная ветка необходима для обработки повторного повтора
            intent_name_key = 'start_tour_with_prof'
        else:
            intent_name_key = 'start_tour_with_prof_short'
        event['request']['nlu']['intents'].update(state.get('pre_intent'))
        return start_tour_with_prof(event, intent_name=intent_name_key)
    elif state.get('screen') == 'start_tour' and 'want_test' in intents:
        return welcome_test(event)
    elif state.get('screen') == 'start_tour' and 'u_not' in intents:
        return goodbye(event)
    # обработка помощи
    elif 'help_me' in intents:
        return fallback_help_me(event)
    elif 'want_test' in intents:
        return welcome_test(event)
    elif 'start_tour' in intents:
        return start_tour(event)
    # Сценарий о каких можешь рассказать
    elif 'what_do_you_know' in intents or 'what_do_you_know_long' in intents:
        return what_do_you_know(event)
    # Обработка неизвестных ответов и вопросов пользователя
    else:
        if 'u_stop' in intents:
            return goodbye(event)
        else:
            return fallback(event)