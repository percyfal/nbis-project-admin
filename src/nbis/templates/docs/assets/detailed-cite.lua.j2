-- detailed-cite.lua
-- Use [!@key] or !@key for detailed citations

local refs = {}

-- Simple BibTeX parser
function parse_bibtex(content)
  local entries = {}

  for entry_type, key, body in content:gmatch("@(%w+)%s*{%s*([^,]+)%s*,(.-)%s*\n}") do
    local entry = {}

    local title = body:match("title%s*=%s*{(.-)}")
    if title then
      title = title:gsub("^{", ""):gsub("}$", "")
      entry.title = title
    end

    local journal = body:match("journal%s*=%s*{(.-)}")
    if journal then
      entry.journal = journal
    end

    entries[key] = entry
  end

  return entries
end

function Meta(meta)
  local bibfile = nil

  if meta.bibliography then
    if type(meta.bibliography) == "table" then
      if meta.bibliography[1] then
        bibfile = pandoc.utils.stringify(meta.bibliography[1])
      else
        bibfile = pandoc.utils.stringify(meta.bibliography)
      end
    else
      bibfile = pandoc.utils.stringify(meta.bibliography)
    end
  end

  if bibfile then
    local file = io.open(bibfile, "r")
    if file then
      local content = file:read("*all")
      file:close()
      refs = parse_bibtex(content)
    end
  end

  return meta
end

-- Handle [!@key] syntax (prefix inside brackets)
function Cite(el)
  local first_cite = el.citations[1]
  local prefix_text = ""

  if first_cite.prefix and #first_cite.prefix > 0 then
    prefix_text = pandoc.utils.stringify(first_cite.prefix)
  end

  if prefix_text:match("^!") then
    first_cite.prefix = pandoc.Inlines(prefix_text:sub(2))
    return pandoc.Span(el, {class = "detailed-cite", ["data-key"] = first_cite.id})
  end

  return el
end

-- Handle !@key syntax (! before citation)
function Inlines(el)
  local result = pandoc.Inlines({})
  local i = 1

  while i <= #el do
    local current = el[i]
    local next = el[i + 1]

    -- Check for Str ending with "!" followed by Cite
    if current.t == "Str" and next and next.t == "Cite" then
      local text = current.text

      if text:match("!$") then
        -- Remove trailing ! from Str
        local new_text = text:sub(1, -2)
        if new_text ~= "" then
          result:insert(pandoc.Str(new_text))
        end

        -- Mark the citation as detailed
        local key = next.citations[1].id
        result:insert(pandoc.Span(next, {class = "detailed-cite", ["data-key"] = key}))

        i = i + 2  -- Skip both elements
      else
        result:insert(current)
        i = i + 1
      end
    else
      result:insert(current)
      i = i + 1
    end
  end

  return result
end

-- Process marked citations
function Span(el)
  if el.classes:includes("detailed-cite") then
    local key = el.attributes["data-key"]
    local ref = refs[key]

    if ref then
      local result = pandoc.Inlines({})
      result:extend(el.content)

      if ref.title then
        result:insert(pandoc.Str(","))
        result:insert(pandoc.Space())
        result:insert(pandoc.Quoted("DoubleQuote", {pandoc.Str(ref.title)}))
      end

      if ref.journal then
        result:insert(pandoc.Str(","))
        result:insert(pandoc.Space())
        result:insert(pandoc.Emph({pandoc.Str(ref.journal)}))
      end

      return result
    end
  end

  return el
end

return {
  { Meta = Meta },
  { Inlines = Inlines, Cite = Cite },
  { Span = Span }
}
