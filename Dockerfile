FROM python:latest

RUN mkdir /sih
WORKDIR /sih

# Upgrade pip and install requirements
COPY requirements.txt requirements.txt
RUN pip install -U pip
RUN pip install -r requirements.txt

# Copy app code and set working directory
COPY . .

# Expose port you want your app on
EXPOSE 8501

CMD streamlit run 01_🌎_Home.py