import re
import markdown as mkdn
from django.conf import settings
from django.core.cache import cache
from django.template.defaultfilters import striptags
from django.utils.safestring import mark_safe


def remove_unwanted_tags(text):
	TAG_RE = re.compile(r'</(?!a|br|p).*?>|<(?!/)(?!a|br|p).*?>')
	return TAG_RE.sub('', text)


def wikisafe_markdown(value):

	if not value:
		return

	value = remove_unwanted_tags(value)

	try:
		html = mark_safe(
			mkdn.markdown(
				value.replace('[[','LBRACK666').replace(']]','RBRACK666'),
				extensions=[
					'markdown.extensions.nl2br',
					'markdown.extensions.smart_strong'
				]
			).replace('LBRACK666','[[').replace('RBRACK666',']]')
		)
	except Exception as e:
		html = value

	return html
	# return remove_unwanted_tags(html)

class WikiException(Exception): # Raised when a particular string is not found in any of the models.
	pass

def wikify(match): # Excepts a regexp match
	wikis = [] # Here we store our wiki model info

	for i in settings.WIKISYNTAX:

		name = i[0]

		modstring = i[1]
		module = __import__(".".join(modstring.split(".")[:-1]))
		for count, string in enumerate(modstring.split('.')):
			if count == 0:
				continue

			module = getattr(module,string)

		module.name = name
		wikis.append(module())

	token, trail = match.groups() # we track the 'trail' because it may be a plural 's' or something useful

	if '=' in token:

		prefix = token.split('=',1)[0].lower().rstrip()
		name = token.split('=',1)[1].rstrip()

		if name.isdigit():
			return '{} '.format(name)


		for wiki in wikis:
			if prefix == wiki.name:
				if wiki.attempt(name,explicit=True):
					"""
					We still check attempt() because maybe
					work is done in attempt that render relies on,
					or maybe this is a false positive.
					"""
					return wiki.render(name,trail=trail,explicit=True)
				else:

					if prefix == 'a':
						return '<a href="https://www.discogs.com/search?q=%s&type=artist">%s</a>' % (name, name)

					if prefix == 'r':
						return '<a href="https://www.discogs.com/search?q=%s&type=release">%s</a>' % (name, name)

					if prefix == 'l':
						return '<a href="https://www.discogs.com/search?q=%s&type=label">%s</a>' % (name, name)

					return '* %s *' % name


	"""
	Now we're going to try a generic match across all our wiki objects.

	Example:

	[[Christopher Walken]]

	[[Studio 54]]
	[[Beverly Hills: 90210]] <-- notice ':' was confused earlier as a wiki prefix name

	[[Cat]]s <-- will try to match 'Cat' but will include the plural 

	[[Cats]] <-- will try to match 'Cats' then 'Cat'

	"""
	for wiki in wikis:
		if getattr(wiki,'prefix_only',None):
			continue

		if wiki.attempt(token):
			return wiki.render(token,trail=trail)

	"""
	We tried everything we could and didn't find anything.
	"""

	raise WikiException("No item found for '%s'"% (token))

class wikify_string(object):
	def __call__(self, string, fail_silently=True):
		self.fail_silently = fail_silently
		self.cache = {}
		self.set_cache = {}

		from wikisyntax import fix_unicode
		#WIKIBRACKETS = '\[\[([^\]]+?)\]\]'
		WIKIBRACKETS = '\[([^\]]+?)\]'
		if not string:
			return ''

		string = fix_unicode.fix_unicode(string)

		if getattr(settings,'WIKISYNTAX_DISABLE_CACHE',False) == False:
			keys = re.findall(WIKIBRACKETS, string)
			self.cache = cache.get_many([k.replace(' ','-').lower() for k in keys if len(k) < 251])

		content = re.sub('%s(.*?)' % WIKIBRACKETS,self.markup_to_links,string)
		cache.set_many(self.set_cache)
		return content

	def __new__(cls, string, **kwargs):
		obj = super(wikify_string, cls).__new__(cls)
		return obj(string, **kwargs)

	def markup_to_links(self,match):
		string = match.groups()[0].lower().replace(' ','-')

		if getattr(settings,'WIKISYNTAX_DISABLE_CACHE',False) == False:
			if string in self.cache:
				return self.cache[string]

			if string in self.set_cache:
				return self.set_cache[string] # Maybe they typed it twice?

		try:
			new_val = wikify(match)

			if getattr(settings,'WIKISYNTAX_DISABLE_CACHE',False) == False:
				self.set_cache[string] = new_val

			return new_val

		except WikiException:
			if not self.fail_silently:
				raise

			return string
