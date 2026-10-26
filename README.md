# Kiahgawa

A warmer, clearer cousin of **Kanagawa Dragon**, with one shared palette for
OpenCode V2, Rex, and Neovim. Early development.

- Dragon's warm charcoal surfaces, with slightly darker terminal panes.
- Brighter foregrounds, comments, secondary labels, and borders.
- Muted moss, dusty blue, mauve, and terracotta, with a warm gold focus accent.
- The same 16 ANSI colors in Rex and Neovim terminals.

## Contents

```text
palette/kiahgawa.json             Canonical source of all colors
colors/kiahgawa.lua               Neovim colorscheme entrypoint
lua/kiahgawa/                     Neovim integration + generated palette
lua/lualine/themes/kiahgawa.lua   Matching statusline theme
extras/opencode/kiahgawa.json    Complete native OpenCode V2 theme
extras/rex/kiahgawa              Ghostty-format Rex theme
scripts/generate.py             Standard-library-only asset generator
tests/                          Consistency, contrast, and Neovim checks
wallpapers/                     Reserved; no images included
```

Generated ports are committed so installation does not require Python or a
build step. No files in this repository depend on a particular home directory
or on someone's dotfiles.

## Install

### OpenCode V2

Copy `extras/opencode/kiahgawa.json` into `~/.config/opencode/themes/`, then
select **kiahgawa** with `/themes`, or merge this into `cli.json`:

```json
{
  "$schema": "https://opencode.ai/v2/cli.json",
  "theme": { "name": "kiahgawa", "mode": "dark" }
}
```

This is a native theme file, not an executable OpenCode plugin.

### Rex

Import `extras/rex/kiahgawa` through Rex's theme settings, or use the CLI:

```sh
rex do client.theme.import path="/absolute/path/to/kiahgawa/extras/rex/kiahgawa"
```

CLI application requires Remote Control enabled in Rex. Select a client with
`rex -C CLIENT do ...` if several apps are connected. Reimport after updates;
Rex stores its own copy of the imported theme.

### Neovim

The initial Neovim integration builds on `rebelot/kanagawa.nvim`, which must be
installed as a dependency. With lazy.nvim:

```lua
{
  "kiahjh/kiahgawa",
  lazy = false,
  priority = 1000,
  dependencies = { "rebelot/kanagawa.nvim" },
  config = function()
    require("kiahgawa").setup({ dim_inactive = true }) -- optional
    vim.cmd.colorscheme("kiahgawa")
  end,
}
```

For lualine, use `options = { theme = "kiahgawa" }`. Optional theme settings
are `transparent` and `dim_inactive`, both false by default. The palette is
available through `require("kiahgawa").palette()`.

For local development, replace `"kiahjh/kiahgawa"` with
`dir = "/absolute/path/to/kiahgawa", name = "kiahgawa"` in that plugin spec.

## Develop

Change `palette/kiahgawa.json`, then regenerate and test:

```sh
python3 scripts/generate.py --write
python3 scripts/generate.py --check
python3 -m unittest discover -s tests -v
nvim --headless -u NONE -i NONE -n -l tests/neovim.lua
```

The Neovim test uses Kanagawa from the default lazy.nvim installation, or the
path in `KIAHGAWA_KANAGAWA_DIR`. The Python checks need no external packages.
CI checks generation, token completeness, references, shared colors, and
contrast floors. Those checks do not replace visual evaluation of every UI.

## Design and contrast

The base background remains `#181616`; Rex's terminal background is `#141313`.
Main text is `#d5d8d0`, and muted text/comments are `#9da69f`. Muted text is
approximately 7.2:1 against the base and 4.7:1 against the highest neutral
surface. Distinct application surfaces are intentional; colors are shared
by semantic role rather than forcing every UI element to look identical.

## Licensing

Code and palette: MIT. See `LICENSE` and the upstream attributions in `NOTICE`.
The palette is inspired by Tommaso Laurenzi's Kanagawa.nvim and Ethan Gilmore's
Zed port. Wallpaper licensing is separate; see `wallpapers/README.md`.
