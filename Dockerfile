    # Step 1: Use a lightweight Python base
    FROM python:3.12-slim

    # Step 2: Set the folder where our app lives inside the "box"
    WORKDIR /app

    # Step 3: Copy the list of tools needed
    COPY app/requirements.txt .

    # Step 4: Install the tools (no-cache-dir keeps the box small)
    RUN pip install --no-cache-dir -r requirements.txt

    # Step 5: Copy your "Engine" (the scraper script) into the box
    # Make sure your script is named 'scraper.py'
    COPY app/ .

    # Tell Python that /app is a place to look for modules
    ENV PYTHONPATH=/app

    # Step 6: The "Start Button"
    # This tells Docker to run your script when the container turns on
    CMD ["python", "scraper.py"]