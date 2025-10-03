from shiny import App, module, reactive, render, ui
from art_parser import *

# ============================================================
# Counter module
# ============================================================
@module.ui
def counter_ui(label: str = "Increment counter") -> ui.TagChild:
    return ui.card(
        ui.tags.style(
        """
        .shiny-text-output {
            font-size:20px
            }
        """
    ),
        ui.h2(label, style = "font-size:80px;"),
        ui.input_action_button(id="button0", label='Previous', style = "font-size:20px;"),
        ui.input_action_button(id="button", label='Next', style = "font-size:20px;"),
        ui.output_code(id="out"),
        ui.output_ui("text"),
        #ui.p()
        ui.input_action_button(id="button2", label='Summary', style = "font-size:20px;"),
        ui.output_code(id = "summary"),
        ui.input_action_button(id="button3", label='Save', style = "font-size:20px;")
    )


@module.server
def counter_server1(input, output, session, starting_value: int = 0):
    count: reactive.value[int] = reactive.value(starting_value)
    message: reactive.value[str] = reactive.value("")   
    dict = habr_parser()
    
    @reactive.effect
    @reactive.event(input.button)
    def _():
        count.set(count()+1)
    
    @reactive.effect
    @reactive.event(input.button0)
    def __():
        count.set(count()-1)
    @render.code
    def out()-> str:
       #url.set(dict[list(dict.keys())[count()]])
       return f"{list(dict.keys())[count()]}, {count()+1}%%{len(dict.keys())}"# dict[list(dict.keys())[count()]]
   
    @render.ui
    def text():
        return ui.tags.a("click here", href=dict[list(dict.keys())[count()]], target='_blank')
     
    
    @reactive.effect
    @reactive.event(input.button2)
    def ___():
        #response = get_token(auth)
        #if response != 1:
        #    giga_token = response.json()['access_token']
            
        #loader = WebBaseLoader(dict[list(dict.keys())[count()]])
        #docs = loader.load()
        #answer = get_chat_completion(giga_token, 'Дай краткое содержание текста:' + docs[0].page_content[:int(len(docs[0].page_content))])
        #context = ""
        #if answer.json().get('choices')[0].get('finish_reason') != "stop":
        #    delimeter = 0.9
        #    while answer.json().get('choices')[0].get('finish_reason') != "stop":
        #        answer = get_chat_completion(giga_token, 'Дай краткое содержание текста:' + docs[0].page_content[:int(len(docs[0].page_content)*delimeter)])
        #        delimeter -=0.1
        #    context = "cropped_context____"
        
        #message.set(context+answer.json()['choices'][0]['message']['content'])
        message.set('bruh')
        
    @reactive.effect
    @reactive.event(input.button3)
    def ____():
        f = open('HABR.json', encoding="utf8")
        data = json.load(f)
        try:
            data[list(dict.keys())[count()]] = dict[list(dict.keys())[count()]]
        except:
            print('Not_saved')
        with open("HABR.json", "w", encoding='utf-8') as f: 
            json.dump(data, f, indent=4, ensure_ascii=False)
    
    @render.code
    def summary():
         
         return message()


@module.server
def counter_server2(input, output, session, starting_value: int = 0):
    count: reactive.value[int] = reactive.value(starting_value)

    @reactive.effect
    @reactive.event(input.button)
    def _():
        count.set(count() + 1)
    @reactive.event(input.button0)
    def _():
        count.set(count() - 1)

    @render.code
    def out() -> str:
        return f"iriska count is {count()}"


# =============================================================================
# App that uses module
# =============================================================================

app_ui = ui.page_fluid(
    
    counter_ui("counter1", "HABR PARSER"),
    
    #ui.tags.a("Click here",href=url,target='_blank'),
    #ui.p(),
    #ui.HTML(f'<a href="{url}" target="_blank">Click here</a>'),
    
    #counter_ui("counter2", "ARXIV PARSER"),
)


def server(input, output, session):
    counter_server1("counter1")
    #counter_server2("counter2")

app = App(app_ui, server)
