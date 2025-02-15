import flet
import random
from time import time, sleep
import asyncio

RNG_NUMS_FROM = 1
RNG_NUMS_TO = 99
RNG_OPERATIONS = '+-'
TIMER_PRECISION = 1     # number of decimal places in timer


def get_math_question() -> str:
    rng_nums = [random.randint(RNG_NUMS_FROM, RNG_NUMS_TO) for _ in range(4)]
    rng_oper = [random.choice(RNG_OPERATIONS) for _ in range(3)]
    question = f'{rng_nums[0]} {rng_oper[0]} {rng_nums[1]} {rng_oper[1]} {rng_nums[2]} {rng_oper[2]} {rng_nums[3]}'

    return question


def main(page: flet.Page):
    time_start = 0
    stop_timer = True

    async def live_timer():
        while not stop_timer:
            if checkbox_show_live_timer.value:
                text_field_timer.value = round(time() - time_start, TIMER_PRECISION)
                text_field_timer.update()
            elif text_field_timer.value:
                text_field_timer.value = ''
                text_field_timer.update()
            # sleep(0.1)
            await asyncio.sleep(0.1)

            # костыль, чтобы этот цикл останавливался при закрытии формы, а не крутился до бесконечности
            # (нужно сменить значение текстового поля; в if-е это и так происходит):
            # text_field_timer.value = ' '
            # upd: перевёл функцию live_timer() на async-вариант - заработало без костыля.

    # def stop_live_timer_on_close_program(e):
    #     print('---')
    #     nonlocal stop_timer
    #     stop_timer = True

    def question_or_answer_to_text_field(e):
        nonlocal time_start, stop_timer

        if text_field_answer.value != '' or text_field_question.value == '':
            text_field_question.value = get_math_question()
            # text_field_question.update()

            text_field_answer.value = ''
            text_field_answer.hint_text = ''
            # text_field_answer.update()

            page.update()

            stop_timer = False
            time_start = time()
            # live_timer()
            page.run_task(live_timer)
        else:
            stop_timer = True

            answer = eval(text_field_question.value)
            text_field_answer.value = answer
            # text_field_answer.update()

            time_stop = time()
            time_total = time_stop - time_start
            text_field_timer.value = round(time_total, TIMER_PRECISION)
            # text_field_timer.update()

            page.update()

    # def on_window_event(e):
    #     print('----')
    #     if e.data == 'close':
    #         nonlocal stop_timer
    #         stop_timer = True
    #         print('--------')
    #         page.window.destroy()
    #         # page.window.close()

    page.window.alignment = flet.alignment.center
    page.window.height = 490
    page.window.width = 550
    page.horizontal_alignment = flet.CrossAxisAlignment.STRETCH

    # Пробовал назначить функцию присвоения "stop_timer = True" на события page.on_close, page.on_disconnect -
    # не помогло: on_close - вообще не то (происходит через 60 мин после закрытия страницы),
    # on_disconnect - хоть и при закрытии приложения но в функцию не заходит.
    # page.on_disconnect = stop_live_timer_on_close_program

    # Пробовал выставить "prevent_close = True", чтобы при закрытии программы она не закрывалась,
    # а позволяла поставить "stop_timer = True", а затем закрываем её вручную через page.window.destroy(),
    # но этот destroy() очень медленно отрабатывает: секунд 6 окно висит только на нём, это позор какой-то.
    # А page.window.close() не закрывает.
    # page.window.prevent_close = True  # чтобы перед закрытием успеть завершить цикл показа таймера
    # page.window.on_event = on_window_event

    text_field_question = flet.TextField(
        text_align=flet.TextAlign.CENTER,
        hint_text='Press the GO button to see the math question.',
        hint_style=flet.TextStyle(size=18),
        border_color=flet.Colors.BLUE_500,
        read_only=True,
        text_size=48,
        content_padding=flet.padding.symmetric(vertical=48)
    )
    text_field_answer = flet.TextField(
        text_align=flet.TextAlign.CENTER,
        hint_text='Press the GO button again to see the answer. Then again. ',
        hint_style=flet.TextStyle(size=18),
        border_color=flet.Colors.BLUE_500,
        read_only=True,
        text_size=48,
        # content_padding=10
    )
    checkbox_show_live_timer = flet.Checkbox(
        label='Показывать ход таймера',
        value=True
    )
    text_field_timer = flet.TextField(
        text_align=flet.TextAlign.CENTER,
        hint_text='',
        border_color=flet.Colors.BLUE_500,
        read_only=True,
        text_size=18,
        # content_padding=10
    )
    button_go = flet.ElevatedButton(
        text='GO !',
        on_click=question_or_answer_to_text_field,
        style=flet.ButtonStyle(text_style=flet.TextStyle(size=60)),
        height=100
    )

    page.add(
        text_field_question,
        text_field_answer,
        flet.Row([checkbox_show_live_timer, text_field_timer]),
        button_go
    )


if __name__ == '__main__':
    flet.app(target=main)
