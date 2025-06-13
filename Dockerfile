#------------FOR AWS--------------
#FROM public.ecr.aws/lambda/python:3.9

#COPY requirements.txt .
#RUN pip install -r requirements.txt

#COPY app/ app/
#COPY aws_lambda_handler.py .

#CMD ["aws_lambda_handler.handler"]

#------------------------

FROM python:latest

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app
EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]