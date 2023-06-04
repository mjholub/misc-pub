function apktui
    doas apk update
    apk search | sed -E 's/-[0-9].*$//' | fzf -m | xargs -I {} doas apk add {}
end
