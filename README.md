# facial-identity-storage

<!-- TODO: project description -->

## Quickstart
We recommend using a virtual environment (venv) for this project with Python 3.10.12.

1. Create a virtual environment:
    ```bash
    python3 -m venv myenv
    ```

1. Activate the virtual environment:
    - For Linux/Mac:
      ```bash
      source myenv/bin/activate
      ```
    - For Windows:
      ```bash
      myenv\Scripts\activate
      ```

1. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
1. Generating facial images

   To generate facial images with watermarks indicating that the images were generated by 
   AI, run the Facial_image_generation.ipynb notebook in Google Colab and make the 
   following cells. Note that the images are saved in the current folder, and in order to 
   run the last cell responsible for adding watermarks, it is necessary to add the 
   Arial.ttf file included in the repository to the current folder on Google Colab.
    Final photos both with and without watermarks and all documents were placed in the 
   photos folder.

1. To run the program you need docker-compose. If you don't have docker, install it:
    ```bash
    sudo snap install docker
    ```
    When you have docker, you can set up the database in second terminal:
    ```bash
    sudo docker compose up
    ```

1. Run the program with the desired options:
    ```bash
    python3 main.py --help
    ```

## Authors
- [Michał Rutkowski](https://github.com/P4ndaM1x)
- [Weronika Wronka](https://github.com/WronkaWeronika)
- [Eryk Zarębski](https://github.com/erzar0)
- [Zuzanna Sulima](https://github.com/Pazuzik)
- [Bartłomiej Wypart](https://github.com/dintees)
- [Damian Łyszczarz](https://github.com/damian95a)
- [Adam Jędrychowski](https://github.com/AdamJedrychowski)
- [Tomasz Kozieł](https://github.com/tomekkoziel)
- [Michał Rogowski](https://github.com/mrogowski01)
