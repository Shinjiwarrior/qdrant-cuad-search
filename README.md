# Qdrant CUAD Search 🚀

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-brightgreen.svg)
![Release](https://img.shields.io/badge/release-v1.0.0-orange.svg)

Welcome to the **Qdrant CUAD Search** repository! This project offers a professional platform for searching commercial contracts, leveraging the power of Qdrant vector search and the CUAD dataset. 

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Releases](#releases)

## Introduction

The **Qdrant CUAD Search** platform allows users to efficiently search through a collection of real contracts. With 510 contracts and over 13,000 expert-labeled clauses, this tool provides semantic search capabilities and utilizes a coarse-to-fine retrieval pipeline. This enables users to find relevant clauses quickly and accurately.

## Features

- **Comprehensive Dataset**: Access to 510 real contracts.
- **Expert-Labeled Clauses**: Over 13,000 clauses labeled by experts for better accuracy.
- **Semantic Search**: Leverage vector search for understanding context.
- **Coarse-to-Fine Retrieval**: Efficiently narrow down search results.
- **User-Friendly Interface**: Built with React and TypeScript for a smooth experience.

## Technologies Used

- **AI**: For semantic search and understanding user queries.
- **Qdrant**: The vector search engine powering the backend.
- **FastAPI**: For building the backend services.
- **React**: For the frontend interface.
- **TypeScript**: For type safety and better development experience.
- **CUAD Dataset**: A valuable resource for contract clauses.

## Getting Started

To get started with **Qdrant CUAD Search**, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Shinjiwarrior/qdrant-cuad-search.git
   cd qdrant-cuad-search
   ```

2. **Install Dependencies**:
   Ensure you have Python and Node.js installed. Then, install the required packages:
   ```bash
   # For backend
   cd backend
   pip install -r requirements.txt

   # For frontend
   cd frontend
   npm install
   ```

3. **Set Up the Environment**:
   Create a `.env` file in the backend directory and set the necessary environment variables.

4. **Run the Application**:
   Start the backend server:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
   Then, start the frontend:
   ```bash
   cd frontend
   npm start
   ```

Now, you can access the application at `http://localhost:3000`.

## Usage

To use the **Qdrant CUAD Search** platform, follow these steps:

1. **Navigate to the Search Page**: Open the application in your web browser.
2. **Enter Your Query**: Type in the clause or contract-related question you have.
3. **Review Results**: The application will display relevant contracts and clauses based on your query.
4. **Refine Your Search**: Use the filters available to narrow down your results further.

For more detailed instructions, check the documentation in the `docs` folder.

## Contributing

We welcome contributions to enhance the **Qdrant CUAD Search** platform. If you want to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push to your forked repository.
5. Open a pull request.

Please ensure your code follows the existing style and includes appropriate tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or feedback, please contact the maintainer at [your-email@example.com].

## Releases

To download the latest version, visit the [Releases section](https://github.com/Shinjiwarrior/qdrant-cuad-search/releases). Here, you can find the latest files that need to be downloaded and executed.

For any updates, please check the [Releases section](https://github.com/Shinjiwarrior/qdrant-cuad-search/releases) regularly.

---

Thank you for your interest in **Qdrant CUAD Search**! We hope you find this tool useful for your contract search needs.