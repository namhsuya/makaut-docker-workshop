# Base image
FROM continuumio/miniconda3
# Install required software
RUN apt-get update
# Install conda updates
RUN conda update conda && \
    conda update --all
# Create /data directory
RUN mkdir /data
# Copy the run_blast.sh script into the container
COPY env.yaml /data/env.yaml
# Install blast 
# RUN conda install -c conda-forge -c bioconda blast=2.2.31 -y
# RUN conda env create -n blast -f /data/env.yaml
# SHELL ["conda", "run", "-n", "blast", "/bin/bash", "-c"]
RUN conda env update -n base -f /data/env.yaml
# Copy the run_blast.sh script into the container
COPY run_blast.sh /data/
# Give execute permission to the script
RUN chmod +x /data/run_blast.sh
# Set the working directory to /data
WORKDIR /data
# Set the entrypoint
ENTRYPOINT ["/bin/bash", "/data/run_blast.sh"]