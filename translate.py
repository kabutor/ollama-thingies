#from ollama import chat
#from ollama import ChatResponse
import ollama
import srt
import os, sys
import argparse

DEBUG=False

"""
You are a professional English (en) to Spanish (es) translator. Your goal is to accurately convey the meaning and nuances of the original English text while adhering to Spanish grammar, vocabulary, and cultural sensitivities.
Produce only the Spanish translation, without any additional explanations or commentary. Please translate the following English text into Spanish:
"""

def trans_line(texto, cont):
    
    #client = ollama.Client( host='http://192.168.1.111:11434' )
    client = ollama.Client( host='http://127.0.0.1:11434' )

    #texto = "Creating your own translation model with Ollama is surprisingly easy"
    frase = """You are a professional English (en) to Spanish (es) language translator. Your goal is to accurately convey the meaning and nuances of the original English text while adhering to Spanish grammar, vocabulary, and cultural sensitivities.
Produce only the Spanish translation, without any additional explanations or commentary.\n
    Rules:\n
    - Translate the input text accurately.\n
    - Preserve the original meaning, tone, and intent.\n
    - Do NOT explain the translation.\n
    - Do NOT add examples or notes.\n
    - Maintain formatting, punctuation, and line breaks.\n
    - If the input is ambiguous, choose the most natural translation.\n
    - If the input is already in the target language, return it as-is, except when the input text is provided in <CONTEXT> tags, you never return that inputted text, is only to have as conversational context.\n
    - If you don't know how to translate or got stuck, just return the original text.\n
    - When possible try to keep the lenght of the text as close as the original text.\n
    - If XML Tags are present on the original text, those will be preserved in the same place in the translated text\n"""
    
    # if there is context and enables 1==1 :D
    if len(cont)>0 and 1==1:
        frase += """This are the previously translated sentences of the current conversation, take this lines in consideration to improve the translation, but you will not return this lines, only the new one translated, this is used only to improve the translation adding context to the conversation.: \n <CONTEXT>""" 
        for c in cont:
            frase += c + "\n"
        frase += "</CONTEXT>"

    frase += """Translate the given text exactly as requested by the user to spanish: \n""" + texto + "\n" 
    if DEBUG:
        print("\n ", frase)
        print("\t\t " , texto)
    # you can use also translategemma:12b 
    response: ollama.ChatResponse = client.chat(model='translategemma:4b', 
        messages=[
      {
        'role': 'system',
        'content': frase, 
      }],
       think= False)

    if DEBUG:
        #print(response['message']['content'])
        print(response.message.content)
    # or access fields directly from the response object
    return(response.message.content)

def write_sub(f_name, content):
    f = open( f_name[:-3] + "ES.srt" , "x")
    f.write(srt.compose(content))
    f.close()


def read_sub(file_name):
    if os.path.isfile(file_name[:-3] + "ES.srt"):
        print("Destination file already exist")
        sys.exit()
    f = open( file_name ,"r" )
    subs = list(srt.parse(f))
    context = []
    for l in range(len(subs)):
        last_line = trans_line(subs[l].content, context)
        subs[l].content = (last_line)
        # append last line to context
        context.append(last_line)
        # number of lines to take for context, hardcoded to 5
        if len(context) > 5:
            context.pop(0)
        if DEBUG:
            print("\n *********************")
            print("c: " ,context)
            print(l)
        else:
            # TODO: change this 
            print(l)
    f.close()
    write_sub(file_name, subs)


parser = argparse.ArgumentParser()
parser.add_argument('path', type=str,
                    help="file with the subtitles")
args = parser.parse_args() 

read_sub(args.path)
