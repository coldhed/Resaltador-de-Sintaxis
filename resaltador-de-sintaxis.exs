# Module for highlighting Python syntax
#

# Mariel Gomez, A01275607
# Santiago Rodríguez, A01025232

defmodule SyntaxHighlighter do
  def highlight(inFile, outFile \\ "highlight.html") do
    data =
      inFile
      |> File.stream!()
      |> Enum.map(&line(&1))
      |> Enum.join("")

    prefix = ~s[<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Highlighted Syntax</title>
</head>

<body>
    <pre>
]

    suffix = ~s[    </pre>
</body>

</html>]
    File.write(outFile, "#{prefix}#{data}#{suffix}")
  end

  # line takes a string and returns a parsed html string
  def line(string), do: doLine(string, "")

  defp doLine("", parsedLine), do: parsedLine

  defp doLine(string, parsedLine) do
    {newString, parsedToken} = token(string)

    doLine(newString, "#{parsedLine}#{parsedToken}")
  end

  # highlight token takes a string, and searches for the first token in the string, removes it, and parses it
  def token(string),
    do:
      doToken(string, [
        # whitespace
        [~r|^(\s+)|, fn token -> token end],
        # string with double quote
        [~r{^([f]?\"(?:\\\"|.)*?\")}, fn token -> ~s|<span class="string">#{token}</span>| end],
        # string with single quote
        [~r{^([f]?\'(?:\\\'|.)*?\')}, fn token -> ~s|<span class="string">#{token}</span>| end],
        # comment
        [~r|^(#.*)|, fn token -> ~s|<span class="comment">#{token}</span>| end],
        # reserved keyworkds
        [
          ~r{^(and|as|assert|break|class|continue|def|del|elif|else|except|False|finally|for|from|global|if|import|in|is|lambda|None|nonlocal|not|or|pass|raise|return|True|try|while|with|yield)(?:\s|$)},
          fn token -> ~s|<span class="reserved_words">#{token}</span>| end
        ],
        # operators
        [
          ~r{^(\+|-|\*|\/|%|\**|\/\/|=|\+=|-=|\*=|\/=|%=|\/\/=|\*\*=|&=|\|=|\^=|>>=|<<=|==|!=|>|<|<=|>=|&|\||~|<<|>>)(?:\s|$)},
          fn token -> ~s|<span class="smooth_operator">#{token}</span>| end
        ],
        # floats and ints, with or without sign, and e notation numbers
        [
          ~r"^([-+]?\d+(?:\.\d+)?(?:e[-+]?\d+)?)(?:\s|$|\,|\)|\]|\}|\:|>|<)",
          fn token -> ~s|<span class="number">#{token}</span>| end
        ],
        # function
        [
          ~r|^([A-Za-z_ñÑ]{1}[A-Za-z_ñÑ\d]*)\(|,
          fn token -> ~s|<span class="func_name">#{token}</span>| end
        ],
        # variable
        [
          ~r"^([A-Za-z_ñÑ]{1}[A-Za-z_ñÑ\d]*)(?:\s|$|\,|\)|\]|\}|\:|>|<)",
          fn token -> ~s|<span class="variable">#{token}</span>| end
        ],
        # parenthesis
        [~r{^([\(\)]+)}, fn token -> ~s|<span class="paren">#{token}</span>| end],
        # brackets
        [~r{^([\[\]]+)}, fn token -> ~s|<span class="brackets">#{token}</span>| end],
        # keys
        [~r|^([\{\}]+)|, fn token -> ~s|<span class="keys">#{token}</span>| end],
        # punctuation
        [~r{^(\.|;|:|,)}, fn token -> ~s|<span class="punctuation">#{token}</span>| end],
        # base case
        [~r|^(.{1})|, fn token -> token end]
      ])

  defp doToken(_, []), do: raise("Reached the end of the recursion. Shouldn't be here!")

  defp doToken(string, [[regex, parserFunc] | tail]) do
    if Regex.match?(regex, string) do
      [_, group] = Regex.run(regex, string)

      {String.replace_leading(string, group, ""), parserFunc.(group)}
    else
      doToken(string, tail)
    end
  end
end
