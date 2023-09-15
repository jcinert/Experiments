# Environmnent
conda env list
conda env remove --name CryptoBot
conda env remove --prefix "<path>\env"
conda env update --prefix ./CryptoBot/env --file environment.yml  --prune
conda env update --prefix ./CryptoBot/env --file environment.yml  --prune --force-reinstall
conda env create --file environment.yml --prefix ./CryptoBot/env

# Git
git remote -v
git config --global user.name "<name>"
git config --global user.email "<email>"
git config http.sslVerify "false"
git config --global --list 
git status
git add .
git commit -m "message"
git commit -m "message" --no-verify
git push