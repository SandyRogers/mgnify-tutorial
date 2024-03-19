import base64
import sys
import ipywidgets as widgets
from typing import List
from IPython.display import display

def check_answer(answer: str, correct_answers_encoded=[""]):
    al = answer.lower()
    aa = al.encode("ascii")
    answer_b64 = base64.b64encode(aa)
    if answer_b64 in correct_answers_encoded:
        print("That's right!", file=sys.stdout)
    else:
        print("That doesn't look quite right...", file=sys.stdout)

def _encode_answer(answer: str):
    al = answer.lower()
    aa = al.encode("ascii")
    ab = base64.b64encode(aa)
    return ab

def _decode_answer(answer: str):
    aa = base64.b64decode(answer)
    return aa


def question(question: str, placeholder: str, banswers: List[str], options: List[str] = [], slug: str = "Your answer:"):
    output = widgets.Label(value='')

    if options:
        guess = widgets.Dropdown(
            value='',
            options=[''] + options,
            description=slug,
            disabled=False   
        )
    else:
        guess = widgets.Text(
            value='',
            placeholder=placeholder,
            description=slug,
            disabled=False   
        )
    
    def check_guess(change):
        if _encode_answer(change.new) in banswers:
            output.value = "That’s right!"
            output.style.text_color = 'green'
            output.style.font_weight = 'bold'
        else:
            output.value = "That doesn’t look quite right"
            output.style.text_color = 'orange'
    
    guess.observe(check_guess, names='value')

    display(
        widgets.Tab(
            children=[
                widgets.VBox([
                    widgets.HTML(value=question),
                    guess,
                    output
                ]),
                widgets.Accordion(
                    children=[
                        widgets.VBox(
                            [widgets.Label(value=_decode_answer(b)) for b in banswers]
                        )
                    ],
                    titles=['Tell me']
                )
            ],
            titles=["Quiz", "Answer"]
        )
    )

