# Instruction on Running the Model


## Run the Model Using Docker
### Prerequisite
-  Ensure Git and Docker are installed on your system.


### Steps

1. **Clone the Repository:**

   - In your terminal/command prompt, navigate to the directory where you want to clone the repository:

        ```bash
        cd /path/to/your/desired/directory
        ```

   - Clone the repository in the desired directory:

        ```bash
        git clone https://github.com/clementlemon02/Competitive-Pricing-Analysis.git
        ```

   - After cloning, navigate into the cloned repository directory:

        ```bash
        cd Competitive-Pricing-Analysis
        ```

2. **Set up Environment Variables:**

   - Copy the `.env.example` file in the backend directory and rename it to `.env`.
   - Configure the environment variables in the `.env` file as per your requirements.

3. **Build Docker Images:**

   - Navigate to the root directory of the cloned repository.
   - Change directory to the root directory of the cloned repository where your `docker-compose.yml` file is located.
   - Run the following command to build Docker images:

        ```bash
        docker-compose build
        ```

4. **Verification:**

    - You can verify that the images are successfully built by running:

        ```bash
        docker images
        ```

5. **Start Docker Containers:**

   - Ensure you are still in the root directory of your cloned repository where your `docker-compose.yml` file is located.
   - Start the Docker Containers:

        ```bash
        docker-compose up
        ```

6. **Access the Application:**

   Once the containers are up and running, you can access the application in your web browser using the URLs specified in the application’s documentation or configuration.

   - Backend API: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
   - Frontend Dashboard: [http://127.0.0.1:8050/pricing-simulation](http://127.0.0.1:8050/pricing-simulation)

7. **Data Visualization and Pricing Simulation:**

   Once you have accessed the frontend dashboard using the specified URL, you can proceed to view the different pages of the application, including "Introduction", "Data Visualization" and "Pricing Simulation".

8. **Stop Docker Containers:**

   - To stop the application, ensure you are in the same directory where the `docker-compose.yml` file is located, typically the root directory of your cloned repository.
   - Run the following command in terminal/command prompt:

   ```bash
   docker-compose down
   ```

9. **Verification:**

   You can verify that the containers are stopped and removed by running:

   ```bash
   docker ps -a
   ```

   After running `docker-compose down`, you should not see any containers related to the application in the list.

### Additional notes:

- Running `docker-compose down` does not remove the Docker images that were built earlier. If you want to remove the images as well, you can use the `docker-compose down --rmi all` command. However, be cautious as this will remove all Docker images associated with your project.
- After stopping the containers, you can start them again using `docker-compose up` whenever you want to run your application.




##
Alternatively, we also suggest another way to run the model. If you have python installed on your system, you can create a virtual environment in the root directory using `venv` or `virtualenv`. Then, activate the environment and install dependencies from `requirements.txt`. Next, configure environment variables by copying `.env.example` to `.env` in the backend directory and adjust values as needed. Finally, execute `run.py` to start the backend server and frontend webpage, accessing the application through specified URLs in a web browser.

Remarks: If you're using macOS, you might need to make a minor adjustment in `run.py`. For more information, please consult the instructions provided within the `run.py` file.