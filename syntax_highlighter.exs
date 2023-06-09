# Module for highlighting Python syntax
#

# Mariel Gomez, A01275607
# Santiago Rodríguez, A01025232

defmodule SyntaxHighlighter do
  def highlightDirectory(dir) do
    Path.wildcard("#{dir}/*.py")
    |> Enum.map(&Task.async(fn -> highlight(&1) end))
    |> Enum.map(&Task.await(&1))
  end

  def highlight(inFile, outDirectory \\ "output_files/") do
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
    <link rel="stylesheet" href="highlight.css">
</head>

<body>
    <pre>
]

    suffix = ~s[    </pre>
</body>

</html>]
    [_, fileName] = Regex.run(~r|([a-zA-ZñÑ_\d]+).py|, inFile)
    File.write("#{outDirectory}#{fileName}.html", "#{prefix}#{data}#{suffix}")
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
        [~r|^(\s+)|, ""], # whitespace
        [~r{^([f]?\"(?:\\\"|.)*?\")}, "string"], # string with double quote
        [~r{^([f]?\'(?:\\\'|.)*?\')}, "string"], # string with single quote
        [~r|^(#.*)|, "comment"], # comment
        [~r{^(and|as|assert|break|class|continue|def|del|elif|else|except|False|finally|for|from|global|if|import|in|is|lambda|None|nonlocal|not|or|pass|raise|return|True|try|while|with|yield)(?:\s|$)}, "reserved_words"], # reserved keyworkds
        [~r[^(\+|-|\*|\/|%|\*\*|\/\/|=|\+=|-=|\*=|\/=|%=|\/\/=|\*\*=|&=|\|=|\^=|>>=|<<=|==|!=|>|<|<=|>=|&|\||~|<<|>>){1}], "smooth_operator"], # operators
        [~r"^([-+]?\d+(?:\.\d+)?(?:e[-+]?\d+)?)", "number"], # floats and ints, with or without sign, and e notation numbers
        [~r|^([A-Za-z_ñÑ]{1}[A-Za-z_ñÑ\d]*)\(|, "func_name"], # function
        [~r"^([A-Za-z_ñÑ]{1}[A-Za-z_ñÑ\d]*)", "variable"], # variable
        [~r{^([\(\)]+)}, "paren"], # parenthesis
        [~r{^([\[\]]+)}, "brackets"], # brackets
        [~r|^([\{\}]+)|, "keys"], # keys
        [~r{^(\.|;|:|,)}, "punctuation"], # punctuation
        [~r|^(.{1})|, ""] # base case
      ])

  defp doToken(_, []), do: raise("Reached the end of the recursion. Shouldn't be here!")

  defp doToken(string, [[regex, htmlClass] | tail]) do
    if Regex.match?(regex, string) do
      [_, group] = Regex.run(regex, string)

      {String.slice(string, String.length(group)..-1), ~s|<span class="#{htmlClass}">#{group}</span>|}
    else
      doToken(string, tail)
    end
  end
end
