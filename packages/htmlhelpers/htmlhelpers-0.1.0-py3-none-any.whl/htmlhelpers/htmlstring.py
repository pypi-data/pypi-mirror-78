"""
Build string html elements.

The name of the function coorilates with the name of the html element
such that `element_name(text)`, where `text` is a string, returns
the f-string `f"<element_name>{text}</element_name>"` 

EXCEPT FOR `<del></del>`, in which
case the function is called `delete(text)`.
"""

def a(text, attr_str=""):                                              
    return f'<a{"" if attr_str == "" else " "}{attr_str}>{text}</a>'

def abbr(text, attr_str=""):                                              
    return f'<abbr{"" if attr_str == "" else " "}{attr_str}>{text}</abbr>'

def acronym(text, attr_str=""):                                     
    return f'<acronym{"" if attr_str == "" else " "}{attr_str}>{text}</acronym>'

def address(text, attr_str=""):
    return f'<address{"" if attr_str == "" else " "}{attr_str}>{text}</address>'

def area(text, attr_str=""):
    return f'<area{"" if attr_str == "" else " "}{attr_str}>{text}</area>'

def b(text, attr_str=""):
    return f'<b{"" if attr_str == "" else " "}{attr_str}>{text}</b>'

def base(text, attr_str=""):
    return f'<base{"" if attr_str == "" else " "}{attr_str}>{text}</base>'

def bdo(text, attr_str=""):
    return f'<bdo{"" if attr_str == "" else " "}{attr_str}>{text}</bdo>'

def big(text, attr_str=""):
    return f'<big{"" if attr_str == "" else " "}{attr_str}>{text}</big>'

def blockquote(text, attr_str=""):
    return f'<blockquote{"" if attr_str == "" else " "}{attr_str}>{text}</blockquote>'

def body(text, attr_str=""):
    return f'<body{"" if attr_str == "" else " "}{attr_str}>{text}</body>'

def br(text, attr_str=""):
    return f'<br{"" if attr_str == "" else " "}{attr_str}>{text}</br>'

def button(text, attr_str=""):
    return f'<button{"" if attr_str == "" else " "}{attr_str}>{text}</button>'

def caption(text, attr_str=""):
    return f'<caption{"" if attr_str == "" else " "}{attr_str}>{text}</caption>'

def cite(text, attr_str=""):
    return f'<cite{"" if attr_str == "" else " "}{attr_str}>{text}</cite>'

def code(text, attr_str=""):
    return f'<code{"" if attr_str == "" else " "}{attr_str}>{text}</code>'

def col(text, attr_str=""):
    return f'<col{"" if attr_str == "" else " "}{attr_str}>{text}</col>'

def colgroup(text, attr_str=""):
    return f'<colgroup{"" if attr_str == "" else " "}{attr_str}>{text}</colgroup>'

def dd(text, attr_str=""):
    return f'<dd{"" if attr_str == "" else " "}{attr_str}>{text}</dd>'

def delete(text, attr_str=""):
    return f'<del{"" if attr_str == "" else " "}{attr_str}>{text}</del>'

def dfn(text, attr_str=""):
    return f'<dfn{"" if attr_str == "" else " "}{attr_str}>{text}</dfn>'

def div(text, attr_str=""):
    return f'<div{"" if attr_str == "" else " "}{attr_str}>{text}</div>'

def dl(text, attr_str=""):
    return f'<dl{"" if attr_str == "" else " "}{attr_str}>{text}</dl>'

def DOCTYPE(text, attr_str=""):
    return f'<DOCTYPE{"" if attr_str == "" else " "}{attr_str}>{text}</DOCTYPE>'

def dt(text, attr_str=""):
    return f'<dt{"" if attr_str == "" else " "}{attr_str}>{text}</dt>'

def em(text, attr_str=""):
    return f'<em{"" if attr_str == "" else " "}{attr_str}>{text}</em>'

def fieldset(text, attr_str=""):
    return f'<fieldset{"" if attr_str == "" else " "}{attr_str}>{text}</fieldset>'

def form(text, attr_str=""):
    return f'<form{"" if attr_str == "" else " "}{attr_str}>{text}</form>'

def h1(text, attr_str=""):
    return f'<h1{"" if attr_str == "" else " "}{attr_str}>{text}</h1>'

def h2(text, attr_str=""):
    return f'<h2{"" if attr_str == "" else " "}{attr_str}>{text}</h2>'

def h3(text, attr_str=""):
    return f'<h3{"" if attr_str == "" else " "}{attr_str}>{text}</h3>'

def h4(text, attr_str=""):
    return f'<h4{"" if attr_str == "" else " "}{attr_str}>{text}</h4>'

def h5(text, attr_str=""):
    return f'<h5{"" if attr_str == "" else " "}{attr_str}>{text}</h5>'

def h6(text, attr_str=""):
    return f'<h6{"" if attr_str == "" else " "}{attr_str}>{text}</h6>'

def head(text, attr_str=""):
    return f'<head{"" if attr_str == "" else " "}{attr_str}>{text}</head>'

def html(text, attr_str=""):
    return f'<html{"" if attr_str == "" else " "}{attr_str}>{text}</html>'

def hr(text, attr_str=""):
    return f'<hr{"" if attr_str == "" else " "}{attr_str}>{text}</hr>'

def i(text, attr_str=""):
    return f'<i{"" if attr_str == "" else " "}{attr_str}>{text}</i>'

def img(text, attr_str=""):
    return f'<img{"" if attr_str == "" else " "}{attr_str}>{text}</img>'

def input(text, attr_str=""):
    return f'<input{"" if attr_str == "" else " "}{attr_str}>{text}</input>'

def ins(text, attr_str=""):
    return f'<ins{"" if attr_str == "" else " "}{attr_str}>{text}</ins>'

def kbd(text, attr_str=""):
    return f'<kbd{"" if attr_str == "" else " "}{attr_str}>{text}</kbd>'

def label(text, attr_str=""):
    return f'<label{"" if attr_str == "" else " "}{attr_str}>{text}</label>'

def legend(text, attr_str=""):
    return f'<legend{"" if attr_str == "" else " "}{attr_str}>{text}</legend>'

def li(text, attr_str=""):
    return f'<li{"" if attr_str == "" else " "}{attr_str}>{text}</li>'

def link(text, attr_str=""):
    return f'<link{"" if attr_str == "" else " "}{attr_str}>{text}</link>'

def map(text, attr_str=""):
    return f'<map{"" if attr_str == "" else " "}{attr_str}>{text}</map>'

def meta(text, attr_str=""):
    return f'<meta{"" if attr_str == "" else " "}{attr_str}>{text}</meta>'

def noscript(text, attr_str=""):
    return f'<noscript{"" if attr_str == "" else " "}{attr_str}>{text}</noscript>'

def object(text, attr_str=""):
    return f'<object{"" if attr_str == "" else " "}{attr_str}>{text}</object>'

def ol(text, attr_str=""):
    return f'<ol{"" if attr_str == "" else " "}{attr_str}>{text}</ol>'

def optgroup(text, attr_str=""):
    return f'<optgroup{"" if attr_str == "" else " "}{attr_str}>{text}</optgroup>'

def option(text, attr_str=""):
    return f'<option{"" if attr_str == "" else " "}{attr_str}>{text}</option>'

def p(text, attr_str=""):
    return f'<p{"" if attr_str == "" else " "}{attr_str}>{text}</p>'

def param(text, attr_str=""):
    return f'<param{"" if attr_str == "" else " "}{attr_str}>{text}</param>'

def pre(text, attr_str=""):
    return f'<pre{"" if attr_str == "" else " "}{attr_str}>{text}</pre>'

def q(text, attr_str=""):
    return f'<q{"" if attr_str == "" else " "}{attr_str}>{text}</q>'

def samp(text, attr_str=""):
    return f'<samp{"" if attr_str == "" else " "}{attr_str}>{text}</samp>'

def script(text, attr_str=""):
    return f'<script{"" if attr_str == "" else " "}{attr_str}>{text}</script>'

def select(text, attr_str=""):
    return f'<select{"" if attr_str == "" else " "}{attr_str}>{text}</select>'

def small(text, attr_str=""):
    return f'<small{"" if attr_str == "" else " "}{attr_str}>{text}</small>'

def span(text, attr_str=""):
    return f'<span{"" if attr_str == "" else " "}{attr_str}>{text}</span>'

def strong(text, attr_str=""):
    return f'<strong{"" if attr_str == "" else " "}{attr_str}>{text}</strong>'

def style(text, attr_str=""):
    return f'<style{"" if attr_str == "" else " "}{attr_str}>{text}</style>'

def sub(text, attr_str=""):
    return f'<sub{"" if attr_str == "" else " "}{attr_str}>{text}</sub>'

def sup(text, attr_str=""):
    return f'<sup{"" if attr_str == "" else " "}{attr_str}>{text}</sup>'

def table(text, attr_str=""):
    return f'<table{"" if attr_str == "" else " "}{attr_str}>{text}</table>'

def tbody(text, attr_str=""):
    return f'<tbody{"" if attr_str == "" else " "}{attr_str}>{text}</tbody>'

def td(text, attr_str=""):
    return f'<td{"" if attr_str == "" else " "}{attr_str}>{text}</td>'

def textarea(text, attr_str=""):
    return f'<textarea{"" if attr_str == "" else " "}{attr_str}>{text}</textarea>'

def tfoot(text, attr_str=""):
    return f'<tfoot{"" if attr_str == "" else " "}{attr_str}>{text}</tfoot>'

def th(text, attr_str=""):
    return f'<th{"" if attr_str == "" else " "}{attr_str}>{text}</th>'

def thead(text, attr_str=""):
    return f'<thead{"" if attr_str == "" else " "}{attr_str}>{text}</thead>'

def title(text, attr_str=""):
    return f'<title{"" if attr_str == "" else " "}{attr_str}>{text}</title>'

def tr(text, attr_str=""):
    return f'<tr{"" if attr_str == "" else " "}{attr_str}>{text}</tr>'

def tt(text, attr_str=""):
    return f'<tt{"" if attr_str == "" else " "}{attr_str}>{text}</tt>'

def ul(text, attr_str=""):
    return f'<ul{"" if attr_str == "" else " "}{attr_str}>{text}</ul>'

def var(text, attr_str=""):
    return f'<var{"" if attr_str == "" else " "}{attr_str}>{text}</var>'