# 2605_DS5111_jzt6rv

## Project Core Objective
This pipeline extracts raw YouTube video transcripts, enriches them via the
Gemini API (stripping timestamps, extracting technical terms and book
references), and validates every output record against a strict JSON schema
contract before it's considered pipeline-ready.

## Bootstrapping Instructions

Run this complete sequence to rebuild the stack from a fresh VM:

```bash
# 1. Clone the repository
git clone git@github.com:tgschindler1/2605_DS5111_jzt6rv.git
cd DS_5111_26Su

# 2. Build the local virtual environment
make env

# 3. Install project dependencies into that environment
make update

# 4. Create your local .env file (see table below) at the repo root
nano .env

# 5. Verify everything is working (see Verification Steps below)
make lint
make test
```

## 3. Environment Configuration Variables

Create a `.env` file at the repo root.
 
| Variable                | Required | Purpose                                                                 |
|--------------------------|----------|--------------------------------------------------------------------------|
| `GEMINI_API_KEY`         | Yes      | Authenticates requests to the Gemini API in `bin/enrich_transcripts.py`. Pipeline exits immediately if missing. |
| `WEBSHARE_USER`          | No       | Webshare proxy username. If unset (with `WEBSHARE_PASSWORD`), extraction falls back to direct local IP routing. |
| `WEBSHARE_PASSWORD`      | No       | Webshare proxy password. Must be set together with `WEBSHARE_USER` to activate proxy routing. |

## 4. Verification Steps
 
After bootstrapping, confirm the environment is correctly configured:
 
**Run the linter** 
```bash
make lint
```
 
**Run the full test suite** (includes parametrized cases, OS/environment
skips, and known-gap `xfail` markers):
```bash
make test
```
 
**Run the pipeline end-to-end against mock data**:
```bash
make test_enrich
```
 


## VM Set Up

Instructions for running python virtual environment on a AWS virtual machine.

### Step 1: Automating init of VM and setup of virtual environment

We will be automating the sequence to recreate VM and setting up github credentials.

Run:

```bash
nano init.sh
```

Edit file with:

```bash
#!/usr/bin/bash
sudo apt update
sudo apt install make -y
sudo apt install python3.14-venv -y
sudo apt install tree
```

Make file executable with:
```bash
chmod +x init.sh
```

Then create ```bash init_git_creds.sh``` and edit with the following

```bash
!#/usr/bin/bash

USER=<your github email>
NAME=<your github user name>

git config --global --list

git config --global user.email ${USER} 
git config --global user.name  ${NAME} 

git config --global --list
```

Make file executable with: ```bash chmod +x init_git_creds.sh```


### Step 2: Clone Git Repo and run VM Init Scripts

Test that your github key by running the following:

```bash
ssh -T git@github.com
```
You should recieve a note that you have been successfully authenticated.

Clone your repo by running the following:

```bash
git clone git@github.com:<YOUR_USERNAME>/<YOUR_REPOSITORY>.git
cd <YOUR_REPOSITORY>
```

Move init scripts into a new folder 'scripts' in your cloned directory and then run:

```bash
bash scripts/init.sh
bash scripts/init_git_creds.sh
tree
```

If successful, command will echo your github credentials and show the directory tree.

### Step 3: Create Python Virtual Environment

In the root of your cloned repo, create a new file called ```bash makefile```:

```bash
default:
    @cat makefile

env:
    python3 -m venv env; . env/bin/activate; pip install --upgrade pip

update:  env
    . env/bin/activate; pip install -r requirements.txt
```

In the same root, create ```bash requirements.txt```:

``` bash
pandas
numpy
```

Run:
``` bash
make update
```

And then verify with:
```bash
. env/bin/activate
pip list
```

### Step 4: Commit and Push Changes to Your Repo

Run:
```bash
git add .
git commit -m "message"
git push
```

Verify that your commit is done and everything is up to date with:

```bash
git log
git status
```


