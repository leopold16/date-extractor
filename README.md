# Image Analysis with OpenAI GPT-4 Vision

This project is a web application that allows users to input natural language and receive extracted tasks, dates, and subtasks from the OpenAI GPT-4 model. The application extracts dates and their contexts and lets user download a calendar file.

## Features

- **Date Extraction**: The application uses OpenAI's GPT-4 model to analyze natural text and extract dates with their context.
- **.ics Download**: The user receives .ics file to download, currently working on integration with google calendar.

## Technologies Used

- **Flask**: A lightweight WSGI web application framework in Python.
- **OpenAI API**: Utilized for image analysis and data extraction.
- **HTML/CSS/JavaScript**: For the front-end interface.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Create a `.env` file in the root directory.
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key
     ```

5. **Run the application**:
   ```bash
   flask run
   ```

6. **Access the application**:
   - Open your web browser and go to `http://127.0.0.1:5000`.

## Usage

- Navigate to the home page.
- Upload an image using the provided form.
- Wait for the analysis to complete and view the extracted dates and contexts.

## Error Handling

- The application returns JSON error messages for any issues encountered during file upload or processing.
- Ensure that the server is running and the OpenAI API key is valid.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

