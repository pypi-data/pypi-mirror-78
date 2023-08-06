from htmlhelpers.htmlformat import format_phrase

def tag_series(tag_fn, text_list):
	tag_series_str = "".join([tag_fn(text) for text in text_list])
	return tag_series_str

def tag_phrase(tag_fn_list, inner_tags, formatting=False):
	'''
	Hierarchically structured html tags, returns a string,
	optionally formated with htmlformat
	

	'''
	tag_phrase_str = inner_tags
	for tag_fn in tag_fn_list[::-1]:
		tag_phrase_str = tag_fn(tag_phrase_str)
	if formatting:
		tag_phrase_str = format_phrase(tag_phrase_str)
	return tag_phrase_str
