function apktui
    set options Upgrade Install Remove Search
    set choice (echo $options | tr ' ' '\n' | fzf --no-hscroll --prompt "apk: " --preview "doas apk info {}" --preview-window down:3:wrap)
    switch $choice
        case Upgrade
            doas apk upgrade --simulate | $PAGER
            read -p "Do you want to upgrade? [y/N] " confirm
            if test $confirm = y
                doas apk upgrade
            end
        case Install
            doas apk update
            apk search | sed -E 's/-[0-9].*$//' | fzf -m --preview 'sh -c "apk info -s {} && apk info -r {}"' | xargs -I {} doas apk add {}
        case Remove
            apk list --installed | sed -E 's/(.*?)-[0-9].*?/\\1/' | fzf -m --preview 'sh -c "apk info -s {} && apk info -r {}"' | xargs -I {} doas apk del {}
        case Search
            read -p "Enter the package name to search: " pkg
            apk info $pkg
        case '*'
            echo "Invalid option"
            apktui
    end
end
