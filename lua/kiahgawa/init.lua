local M = {}
local options = { transparent = false, dim_inactive = false }

function M.setup(opts)
  options = vim.tbl_deep_extend("force", options, opts or {})
end

function M.palette()
  return vim.deepcopy(require("kiahgawa.palette"))
end

function M.load()
  local ok, kanagawa = pcall(require, "kanagawa")
  if not ok then
    error("Kiahgawa requires rebelot/kanagawa.nvim on Neovim's runtimepath")
  end
  local p = M.palette()
  vim.o.background = "dark"
  kanagawa.setup({
    theme = "dragon",
    background = { dark = "dragon", light = "dragon" },
    compile = false,
    transparent = options.transparent,
    dimInactive = options.dim_inactive,
    commentStyle = { italic = true },
    functionStyle = { italic = true },
    keywordStyle = { italic = false },
    colors = {
      palette = {
        dragonBlack0 = p.black, dragonBlack1 = p.inset, dragonBlack2 = p.panel,
        dragonBlack3 = p.background, dragonBlack4 = p.raised, dragonBlack5 = p.selection,
        dragonBlack6 = p.disabled, dragonWhite = p.foreground, dragonAsh = p.muted,
        dragonGray = p.subtle, dragonGray2 = p.subtle, dragonGray3 = p.muted,
        dragonBlue2 = p.blue, dragonBlue = p.blue, dragonViolet = p.purple,
        dragonRed = p.red, dragonGreen = p.brightGreen, dragonGreen2 = p.green,
        dragonAqua = p.cyan, dragonPink = p.purple, dragonYellow = p.yellow,
        dragonOrange = p.orange, dragonOrange2 = p.orange, dragonTeal = p.brightBlue,
        samuraiRed = p.error, roninYellow = p.warning,
      },
      theme = {
        dragon = {
          syn = {
            string = p.green, variable = p.foreground, number = p.purple,
            constant = p.orange, identifier = p.property, parameter = p.subtle,
            fun = p.blue, statement = p.keyword, keyword = p.keyword,
            operator = p.orange, preproc = p.red, type = p.cyan, regex = p.orange,
            deprecated = p.disabled, comment = p.muted, punct = p.cyan,
            special1 = p.brightBlue, special2 = p.keyword, special3 = p.brightRed,
          },
          vcs = { added = p.green, removed = p.red, changed = p.yellow },
          diag = { ok = p.green, error = p.error, warning = p.warning, info = p.blue, hint = p.cyan },
          diff = { add = p.diffAdded, delete = p.diffRemoved, change = p.panel, text = p.raised },
          ui = {
            fg = p.foreground, fg_dim = p.muted, fg_reverse = p.background,
            bg = p.background, bg_dim = p.inset, bg_m3 = p.black,
            bg_m2 = p.inset, bg_m1 = p.panel, bg_p1 = p.raised, bg_p2 = p.selection,
            bg_gutter = p.background, special = p.yellow, nontext = p.disabled,
            whitespace = p.disabled, bg_visual = p.selection, bg_search = p.search,
            float = { fg = p.foreground, bg = p.inset, fg_border = p.border, bg_border = p.inset },
            pmenu = {
              fg = p.foreground, fg_sel = p.brightForeground, bg = p.panel,
              bg_sel = p.selection, bg_sbar = p.panel, bg_thumb = p.scrollbar,
            },
          },
          term = p.ansi,
        },
      },
    },
    overrides = function()
      return {
        Boolean = { fg = p.warning, bold = true },
        CursorLine = { bg = p.panel },
        CursorLineNr = { fg = p.yellow, bold = true },
        FloatTitle = { fg = p.yellow, bg = p.inset, bold = true },
        TelescopeBorder = { fg = p.border, bg = p.background },
        TelescopeNormal = { fg = p.foreground, bg = p.background },
        TelescopePromptNormal = { fg = p.foreground, bg = p.panel },
        TelescopeResultsNormal = { fg = p.foreground, bg = p.background },
        TelescopeSelection = { fg = p.brightForeground, bg = p.selection },
        TelescopeSelectionCaret = { fg = p.yellow, bg = p.selection },
        StatusLine = { fg = p.foreground, bg = p.inset },
        StatusLineNC = { fg = p.muted, bg = p.background },
        Visual = { fg = p.brightForeground, bg = p.selection },
        VisualNOS = { fg = p.brightForeground, bg = p.selection },
        IblIndent = { fg = p.selection },
        IblScope = { fg = p.border },
        WhichKeyFloat = { bg = p.inset },
        WhichKeyBorder = { fg = p.border, bg = p.inset },
        NeoTreeNormal = { fg = p.foreground, bg = p.panel },
        NeoTreeNormalNC = { fg = p.muted, bg = p.panel },
        NeoTreeFloatBorder = { fg = p.border, bg = p.inset },
        NeoTreeTitleBar = { fg = p.background, bg = p.yellow, bold = true },
        BufferCurrent = { fg = p.foreground, bg = p.background, bold = true },
        BufferCurrentIndex = { fg = p.yellow, bg = p.background },
        BufferCurrentMod = { fg = p.yellow, bg = p.background },
        BufferCurrentSign = { fg = p.yellow, bg = p.background },
        BufferInactive = { fg = p.muted, bg = p.inset },
        BufferVisible = { fg = p.subtle, bg = p.inset },
        NoiceCmdlinePopup = { fg = p.foreground, bg = p.inset },
        NoiceCmdlinePopupBorder = { fg = p.yellow, bg = p.inset },
        NoiceCmdlineIcon = { fg = p.yellow },
      }
    end,
  })
  kanagawa.load("dragon")
  vim.g.colors_name = "kiahgawa"
end

return M
