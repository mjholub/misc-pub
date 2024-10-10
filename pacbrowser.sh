#!/usr/bin/bash
# Licensed under GPL v3. Copyright (c) 2024 M. Hołub
# This script should be on the receiving end of a pipe from `pacman -Q` or `paru -Q` or similar.

awk '
    BEGIN { RS="\n\n"; FS="\n"; ORS="\n" }
    {
        printf "{"
        for (i=1; i<=NF; i++) {
            split($i, a, ":")
            gsub(/^[ \t]+|[ \t]+$/, "", a[1])
            gsub(/^[ \t]+|[ \t]+$/, "", a[2])
            if (a[2] != "" && a[2] != "None") {
                gsub(/"/, "\\\"", a[2])
                printf "%s\"%s\":\"%s\"", (i>1 ? "," : ""), a[1], a[2]
            }
        }
        printf "}\n"
    }
' | fzf --ansi --preview 'echo {} | jq -r "
    def color_key:
        if .key == \"Name\" then \"\u001b[32m\" # Green
        elif .key == \"Version\" then \"\u001b[34m\" # Blue
        elif .key == \"Description\" then \"\u001b[33m\" # Yellow
        else \"\u001b[36m\" # Cyan
        end;
    to_entries |
    map(\"\(color_key)\(.key)\u001b[0m: \(.value)\") |
    .[]
"'
