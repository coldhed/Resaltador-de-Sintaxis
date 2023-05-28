# Syntax Highlighter
By Mariel Gómez and Santiago Rodríguez

---
A Python syntax highlighter, built in Elixir. 

### How to use?

```elixir
SyntaxHighlighter.highlight("test.py")
```
Which will output the highlighted syntax to highlight.html. To specify the output file, you can use:
```elixir
SyntaxHighlighter.highlight("test.py", "output.html")
```

### How does it work?
For all of the lines of the Python file, it uses recursion to search with Regex for the first token from that line, it parses it, and shortens the line by that token until the line is empty and completely parsed. Hence, the algorithm has a time complexity of **O(n)**, where n is the number of tokens of the Python file. This is because  the number of possible tokens to look for in Python is constant, and we search with Regex at the beginning of the line, so the parsing of each token is constant.