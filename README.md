# Textract PE

## Getting Started

### Create python environment

```python
python -m venv env
```

### Install dependencies 

```powershell
pip install -r requirements.txt
```

## Running the code

The code is expected to be run in the same directory as the amazon textract output i.e. in a directory that contains a `analyzeDocResponse.json` and some number of `table-<int>.csv` files. Additionally, the directory should also contain the source pdf file as this is required to extract images of the tables (for ensuring accuracy). 

Try AWS Textract at [AWS Textract](https://aws.amazon.com/textract/) to better understand the Textract output format.



