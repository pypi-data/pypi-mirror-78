# TEA - Translation Engine Architect

A command line tool to create translation engine.


## Install
First install [pipx](https://github.com/pipxproject/pipx) then:

```
pipx install pangeamt-tea
```

## Usage 

### Step 1: Create a new project

```
tea new --customer customer --srcLang es --tgtLang en --flavor automotion --version 0.0.1
```

This command will create the project directory structure:


```
├── customer_es_en_automotion_0.0.1
│   ├── config.yml
│   └── data
```

Then enter in the directory

```
cd customer_es_en_automotion_0.0.1
```

### Step 2: Configuration

#### Tokenizer

A tokenizer can be applied to source and target

```
tea tokenizer --src mecab  --tgt moses
```

To list all available tokenizer:

```
tea tokenizer --list 
```

#### Truecaser

```
tea truecaser --src --tgt
```

#### BPE
```
tea bpe -s -t
```

#### Processors
```
tea config processors -s "{processors}"
```
being processors a list of preprocesses and postprocesses.


### Step 3:
Copy some multilingual ressources (.tmx, bilingual files, .af ) into the 'data' directory

### Step 4: Run

Clean the data passing the normalizers and validators:
```
tea workflow clean -n {clean_th} -d
```
being clean_th the number of threads.

Preprocess the data (split data in train, dev or test, tokenization, BPE):
```
tea workflow prepare -n {prepare_th} -s 3
```
being prepare_th the number of threads.

Training model
```
tea workflow train --gpu 0
```
Evaluate model
```
tea workflow eval --step {step} --src file.src --ref file.tgt --log file.log --out file.out --gpu 0
```
