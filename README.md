# 🏭 Siemens PLC QA Dashboard

A modern, web-based Q 26A assistant for Siemens PLC systems. Accessible from any device, anywhere in the world.

![Dashboard Preview](https://img.shields.io/badge/Status-Production%20Ready-green)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Flask](https://img.shields.io/badge/Flask-2.3+-blue)
![Mobile Friendly](https://img.shields.io/badge/Mobile-Friendly-green)

## 🌟 Features

- **💬 Interactive Chat Interface** - Ask questions about Siemens PLCs
- **📱 Mobile Responsive** - Works perfectly on phones, tablets, and desktops
- **🌐 Global Access** - Deploy once, access from anywhere
- **⚡ Fast Response** - Built-in knowledge base with instant answers
- **🔒 Secure** - Rate limiting, CORS protection, input validation
- **📊 System Monitoring** - Basic system information and health checks
- **💾 Session History** - Keep track of your questions and answers

## 🚀 Live Demo

🌐 **[Access Live Dashboard](https://your-app-name.railway.app)** *(Will be updated after deployment)*

## 📸 Screenshots

### Desktop View
- Clean, professional interface
- Real-time chat functionality
- Example questions for quick start

### Mobile View
- Optimized for touch devices
- Responsive design
- Full feature parity with desktop

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Railway/Render/Heroku

# Siemens PLC Question-Answering Assistant

A comprehensive AI-powered assistant for Siemens PLC topics using LangChain and free resources. This tool helps engineers, technicians, and students get instant answers to questions about Siemens PLCs, TIA Portal, PROFINET, and industrial automation.

## 🚀 Features

- **Free & Open Source**: Built entirely using free resources and open-source tools
- **Comprehensive Coverage**: S7-1500, S7-1200, TIA Portal, PROFINET, Safety functions
- **Multiple Interfaces**: Web dashboard, Streamlit app, and command-line interface
- **RAG-Powered**: Uses Retrieval-Augmented Generation for accurate answers
- **Local Processing**: Runs entirely on your machine, no external API required
- **Extensible**: Easy to add more data sources and customize

## 📋 Topics Covered

- **PLC Programming**: LAD, FBD, STL, SCL, GRAPH
- **Hardware Configuration**: I/O modules, CPU selection, system setup
- **Communication**: PROFINET, Ethernet, serial interfaces
- **Safety Functions**: Safety Integrated, SIL levels, emergency stops
- **Troubleshooting**: Common issues and diagnostic procedures
- **Best Practices**: Programming standards and optimization

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- 4GB+ RAM recommended

### Setup

1. **Clone or download this project**
   ```bash
   cd python_project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables (optional)**
   ```bash
   cp .env.example .env
   # Edit .env file to add API keys if you want to use OpenAI embeddings
   ```

## 🎯 Usage

### Cross-Device Web Dashboard (Recommended)

**Access from any device on your network!**

1. **Start the dashboard**
   ```bash
   python start_dashboard.py
   ```
   
2. **Access from any device**
   - **Desktop/Laptop**: http://localhost:5000
   - **Mobile/Tablet**: http://YOUR_IP:5000 (shown in terminal)
   - **Other computers**: Use the network IP address

3. **Features**
   - 📱 **Mobile-responsive design**
   - 💬 **Real-time chat interface**
   - 📚 **Organized example questions**
   - 📊 **System monitoring**
   - 🗂️ **Session history**
   - 🔗 **Source references**

### Web Interface (Streamlit)

1. **Start the web application**
   ```bash
   streamlit run plc_qa_assistant.py
   ```

2. **Initialize the assistant**
   - Click "Initialize Assistant" in the sidebar
   - Wait for documents to load and process
   - The assistant will be ready for questions

3. **Ask questions**
   - Type your PLC-related question
   - Click "Get Answer"
   - View the answer and relevant sources

### Command Line Interface

1. **Initialize the assistant**
   ```bash
   python cli_assistant.py --init
   ```

2. **Ask a single question**
   ```bash
   python cli_assistant.py --question "What is the difference between S7-1500 and S7-1200?"
   ```

3. **Interactive mode**
   ```bash
   python cli_assistant.py --interactive
   ```

## 📝 Example Questions

Here are some example questions you can ask:

- "What is the difference between S7-1500 and S7-1200?"
- "How do I configure PROFINET communication?"
- "What programming languages are supported in TIA Portal?"
- "How do I troubleshoot communication errors?"
- "What are the safety functions in Siemens PLCs?"
- "How do data blocks work in Siemens PLCs?"
- "How to configure a safety function in TIA Portal?"
- "What is the scan cycle in PLC programming?"
- "How to set up remote I/O modules?"

## 🔧 Configuration

### Data Sources

The assistant uses multiple free data sources:

1. **Built-in Knowledge Base**: Curated information about Siemens PLCs
2. **Web Resources**: Public Siemens documentation (when accessible)
3. **Local PDFs**: Place Siemens manuals in `./siemens_docs/` folder
4. **Scraped Data**: Use the data scraper to collect additional resources

### Adding Custom Documents

1. **PDF Documents**: Place PDF files in the `./siemens_docs/` directory
2. **Scraped Data**: Run the data scraper to collect more resources
   ```bash
   python data_scraper.py
   ```

### Customizing Embeddings

By default, the assistant uses free HuggingFace embeddings. You can customize this in `plc_qa_assistant.py`:

```python
# For OpenAI embeddings (requires API key)
from langchain.embeddings import OpenAIEmbeddings
self.embeddings = OpenAIEmbeddings()

# For different HuggingFace models
self.embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)
```

## 🗂️ Project Structure

```
python_project/
├── web_dashboard.py        # Cross-device web dashboard (Flask)
├── start_dashboard.py      # Dashboard launcher script
├── plc_qa_assistant.py     # Main Streamlit application
├── cli_assistant.py        # Command-line interface
├── data_scraper.py         # Web scraper for additional data
├── test_assistant.py       # Test suite
├── setup.py               # Setup and installation script
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── README.md              # This file
├── templates/
│   └── dashboard.html      # Web dashboard template
├── siemens_docs/          # Place PDF documents here
├── vectorstore/           # Generated vector database
└── scraped_plc_data.json  # Scraped data cache
```

## 📊 Data Sources Used

### Primary Sources
- **Siemens Documentation**: System and programming manuals
- **Built-in Knowledge**: Curated PLC information
- **GitHub Repositories**: Open-source PLC projects and examples

### Secondary Sources (via scraper)
- **Automation Blogs**: Industry articles and tutorials
- **Forums**: Technical discussions and solutions
- **Video Content**: Tutorial descriptions and metadata

## ⚡ Performance Tips

1. **First Run**: Initial setup takes 5-10 minutes to download and process documents
2. **Subsequent Runs**: Vector store is cached for fast startup
3. **Memory Usage**: Requires 2-4GB RAM for optimal performance
4. **Storage**: Vector store and documents require ~500MB disk space

## 🔍 Troubleshooting

### Common Issues

1. **"Vector store not found"**
   - Run initialization: `python cli_assistant.py --init`
   - Or use the web interface initialization button

2. **"Import Error"**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version (3.8+ required)

3. **Slow Performance**
   - Close other applications to free up RAM
   - Consider using a GPU-enabled environment for faster embeddings

4. **No Answers Found**
   - Try rephrasing your question
   - Ensure the topic is related to Siemens PLCs
   - Add more documents to the knowledge base

### Getting Help

- Check the console output for detailed error messages
- Ensure all file paths are correct
- Verify internet connection for initial document downloads

## 🚀 Advanced Usage

### Custom Knowledge Base

Add your own PLC knowledge by editing the `get_plc_knowledge_base()` method in `plc_qa_assistant.py`:

```python
knowledge_base.append({
    "title": "Your Custom Topic",
    "content": "Your detailed explanation here..."
})
```

### Different LLM Models

The assistant uses HuggingFace models by default. You can customize the LLM in the `setup_qa_chain()` method:

```python
# For larger models (requires more RAM)
llm_pipeline = pipeline(
    "text-generation",
    model="microsoft/DialoGPT-large",
    # ... other parameters
)
```

### API Integration

To use OpenAI or other API-based models:

1. Set up your API key in `.env`
2. Modify the LLM initialization:

```python
from langchain.llms import OpenAI
llm = OpenAI(temperature=0.7)
```

## 📝 Contributing

Contributions are welcome! Here are some ways to help:

1. **Add Data Sources**: Contribute new PLC documentation or resources
2. **Improve Accuracy**: Enhance the knowledge base with verified information
3. **Bug Fixes**: Report and fix issues
4. **Features**: Add new capabilities like multi-language support

## 📄 License

This project is open source and available under the MIT License.

## ⚠️ Disclaimer

This assistant is built using publicly available information and is intended for educational and reference purposes. Always verify critical information with official Siemens documentation and qualified professionals for production systems.

## 🙏 Acknowledgments

- Siemens for providing comprehensive public documentation
- LangChain community for the excellent framework
- HuggingFace for free embedding models
- Open source contributors and automation community

---

**Happy PLC Programming! 🔧**
# plc-qa-dashboard
