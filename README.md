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

#### What types of tokens does it detect?
It parses and maintains whitespace, as well as detecting the following tokens:
 - **Strings**: It considers string with single or double quote, as well as not ending strings when quotes are escaped.
 - **Comments**: If a # character is found, the rest of the line is a comment.
 - **Reserved Keywords**: The regex checks for all of the reserved keywords in Python.
 - **Operators**: This is defined by listing all of the possible operators. 
 - **Numbers**: It looks for floats and ints, with or without sign, and also takes into account E-notation.
 - **Functions**: It looks for a valid function name (considering the chars it can start with, and the chars it can contain), followed by an opening parenthesis. 
 - **Variables**: It can start with either an upper-case or lower-case letter, or an underscore.
 - **Parenthesis, brackets, and keys**: It looks for either opening or closing parenthesis, brackets, and keys, but doesn't check if they add up.
 - **Punctuation**: This includes a point, a semicolon, a colon, or a comma.