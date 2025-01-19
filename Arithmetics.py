import flet
import random
from time import time

RNG_NUMS_FROM = 1
RNG_NUMS_TO = 99
RNG_OPERATIONS = '+-'


def get_math_question() -> str:
    rng_nums = [random.randint(RNG_NUMS_FROM, RNG_NUMS_TO) for _ in range(4)]
    rng_oper = [random.choice(RNG_OPERATIONS) for _ in range(3)]
    question = f'{rng_nums[0]} {rng_oper[0]} {rng_nums[1]} {rng_oper[1]} {rng_nums[2]} {rng_oper[2]} {rng_nums[3]}'

    return question


def main(page: flet.Page):
    time_start = 0

    def question_or_answer_to_text_field(e):
        nonlocal time_start

        if text_field_answer.value != '' or text_field_question.value == '':
            text_field_question.value = get_math_question()
            # text_field_question.update()

            text_field_answer.value = ''
            text_field_answer.hint_text = ''
            # text_field_answer.update()

            time_start = time()
            text_field_timer.value = ''

            page.update()
        else:
            answer = eval(text_field_question.value)
            text_field_answer.value = answer
            # text_field_answer.update()

            time_stop = time()
            time_total = time_stop - time_start
            text_field_timer.value = round(time_total, 2)
            # text_field_timer.update()

            page.update()

    page.window.alignment = flet.alignment.center
    page.window.height = 490
    page.window.width = 550
    page.horizontal_alignment = flet.CrossAxisAlignment.STRETCH

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

    page.add(text_field_question, text_field_answer, text_field_timer, button_go)


if __name__ == '__main__':
    flet.app(target=main)
