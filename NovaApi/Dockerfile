FROM python:3.8
RUN pip3 install pipenv
COPY . .
RUN pipenv install
EXPOSE 8000
CMD ["pipenv", "run", "start"]