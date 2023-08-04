# Base image with Python and ReportLab
FROM python:3

# Install required system packages
RUN apt-get update

# Create app directory
RUN mkdir /app

# Install required Python packages
RUN pip install matplotlib_venn pandas reportlab

# Copy the Python script into the container
ADD summarize.py /app/summarize.py

# Set the working directory
WORKDIR /data

# Set the entrypoint to run the Python script
# CMD ["/bin/bash"]
ENTRYPOINT ["python", "/app/summarize.py"]