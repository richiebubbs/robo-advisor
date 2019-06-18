# robo-advisor

This app exists in the remote repository: https://github.com/richiebubbs/robo-advisor

To begin, fork the repository.
Use GitHub desktop to clone the repository to your computer's desktop.
Navigate to the app through the command line by using 
```sh
cd ~/Desktop/robo-advisor
```

## Create and Activate a virtual environment:

In the command line prompt, enter:

```sh
conda create -n stocks-env python=3.7 # (first time only)
conda activate stocks-env
```

Also from the command line, install the required packages as follows:

```sh
pip install -r requirements.txt
pip install pytest # (only if you'll be writing tests)
```

To run the program from the command line:

```sh
python app/robo_advisor.py
```


