set CONDA_ENV=SeleniumBot
call conda activate %CONDA_ENV%
python "D:\Github\muxite.github.io\scarlet_rat_v0.py"
call conda deactivate
timeout /t 2 /nobreak
cd D:\Github\muxite.github.io
git add --all
git commit -m "autoCommit %date:~-4%%date:~3,2%%date:~0,2%.%time:~0,2%%time:~3,2%%time:~6,2%"
git push
exit 0
