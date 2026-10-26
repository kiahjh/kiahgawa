local root = vim.fn.fnamemodify(debug.getinfo(1, "S").source:sub(2), ":p:h:h")
local dependency = vim.env.KIAHGAWA_KANAGAWA_DIR or (vim.fn.stdpath("data") .. "/lazy/kanagawa.nvim")
assert(vim.fn.isdirectory(dependency) == 1, "Set KIAHGAWA_KANAGAWA_DIR to a Kanagawa.nvim checkout")
vim.opt.rtp:prepend(root)
vim.opt.rtp:append(dependency)
vim.cmd.colorscheme("kiahgawa")
local p = require("kiahgawa").palette()
local oc = vim.json.decode(table.concat(vim.fn.readfile(root .. "/extras/opencode/kiahgawa.json"), "\n"))
local function color(group, attr)
  local value = vim.api.nvim_get_hl(0, { name = group, link = false })[attr]
  assert(value, group .. "." .. attr .. " is missing")
  return string.format("#%06x", value)
end
assert(vim.g.colors_name == "kiahgawa")
assert(color("Normal", "bg") == p.background)
assert(color("Normal", "fg") == p.foreground)
assert(color("Visual", "bg") == p.selection)
assert(color("Visual", "fg") == p.brightForeground)
assert(color("FloatBorder", "fg") == p.border)
for group, token in pairs({ Comment = "comment", Keyword = "keyword", Function = "function", String = "string", Number = "number", Type = "type", Operator = "operator", Delimiter = "punctuation" }) do
  assert(color(group, "fg") == oc.base.syntax[token], group .. " differs from OpenCode")
end
for i, value in ipairs(p.ansi) do
  assert(vim.g["terminal_color_" .. (i - 1)]:lower() == value, "ANSI mismatch " .. (i - 1))
end
local lualine = require("lualine.themes.kiahgawa")
assert(lualine.normal.a.bg == p.yellow)
assert(lualine.normal.c.fg == p.foreground)
assert(lualine.inactive.c.fg == p.muted)
print("Kiahgawa Neovim, lualine, OpenCode syntax and all 16 terminal colors match.")
