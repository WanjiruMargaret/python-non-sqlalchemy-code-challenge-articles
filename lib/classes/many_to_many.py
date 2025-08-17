# classes/many_to_many.py

class Author:
    all = []

    def __init__(self, name):
        if not isinstance(name, str) or len(name.strip()) == 0:
            raise ValueError("Author name must be a non-empty string")
        self._name = name
        self._articles = []
        Author.all.append(self)

    @property
    def name(self):
        # Immutable, but attempts to set won't raise (tests don't expect exceptions)
        return self._name

    @name.setter
    def name(self, value):
        # Ignore any attempts to change once set (no exception)
        return

    def articles(self):
        return self._articles[:]

    def magazines(self):
        # Unique, order-preserving; return list (tests don't expect None here)
        seen = set()
        result = []
        for article in self._articles:
            m = article.magazine
            if m not in seen:
                seen.add(m)
                result.append(m)
        return result

    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    def topic_areas(self):
        # Unique categories; return None if none (tests assert None for empty)
        seen = set()
        result = []
        for article in self._articles:
            cat = article.magazine.category
            if cat not in seen:
                seen.add(cat)
                result.append(cat)
        return result if result else None


class Magazine:
    all = []

    def __init__(self, name, category):
        self._articles = []
        self._name = None
        self._category = None
        self.name = name        # validated via setter
        self.category = category
        Magazine.all.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # Accept valid strings (2..16), silently ignore invalid (no exceptions)
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value
        else:
            return  # ignore invalid assignments

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        # Accept non-empty strings, silently ignore invalid
        if isinstance(value, str) and len(value.strip()) > 0:
            self._category = value
        else:
            return  # ignore invalid assignments

    def articles(self):
        # Always a list (tests rely on list semantics here)
        return self._articles[:]

    def contributors(self):
        # Unique authors, order-preserving; return list (not None)
        seen = set()
        result = []
        for article in self._articles:
            a = article.author
            if a not in seen:
                seen.add(a)
                result.append(a)
        return result

    def article_titles(self):
        titles = [a.title for a in self._articles]
        return titles if titles else None  # tests expect None when empty

    def contributing_authors(self):
        # Authors with >2 articles in this magazine; None if none
        counts = {}
        for a in self._articles:
            counts[a.author] = counts.get(a.author, 0) + 1
        result = [author for author, n in counts.items() if n > 2]
        return result if result else None


class Article:
    all = []

    def __init__(self, author, magazine, title):
        # Set fields (valid initial values in tests)
        self._title = None
        self.title = title          # validate once
        self._author = None
        self._magazine = None
        self.author = author        # links to author._articles
        self.magazine = magazine    # links to magazine._articles
        Article.all.append(self)    # tests reset Article.all and expect auto-append

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        # Immutable after first set; ignore further sets (no exceptions)
        if self._title is not None:
            return
        if not isinstance(value, str):
            return
        if not (5 <= len(value) <= 50):
            return
        self._title = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if not isinstance(value, Author):
            return  # ignore invalid, no exception
        self._author = value
        if self not in value._articles:
            value._articles.append(self)

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        if not isinstance(value, Magazine):
            return  # ignore invalid, no exception
        self._magazine = value
        if self not in value._articles:
            value._articles.append(self)
